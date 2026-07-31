"""Guards this public repo against Digi International's confidential
commercial content: MSRP, distributor pricing, channel tier names, part
numbers, credentials.

Deliberately strict about currency literals
-------------------------------------------
The currency check matches ANY dollar figure, not only Digi's. That is
intentional: a regex cannot tell Digi's distributor pricing from a third
party's public list price, and the failure that matters — Digi commercial
data reaching a public repo — is far more costly than the inconvenience of
rephrasing an unrelated number.

The convention that follows from it: costs that are NOT Digi pricing (a
third-party API rate, a cloud charge) are written in words rather than
symbols — "roughly 6.5 cents per image", not "$0.065/image". The fact
survives, the guard stays maximally strict, and no exception list has to be
maintained and audited.

Do NOT loosen a pattern or add an allowlist entry to make a legitimate
non-Digi cost pass. Rephrase the prose instead, and if a case ever arises
where that is genuinely impossible, raise it rather than widening the guard.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt", ".css", ".html"}

# "assets" is deliberately NOT skipped: binaries (.pptx, .png) are already
# excluded by TEXT_SUFFIXES above, so skipping the whole directory buys no
# performance and only hides text files (e.g. assets/README.md) from the guard.
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}

# A currency amount: comma-grouped, with cents, or a bare 3+ digit figure.
# The 3-digit floor deliberately avoids matching shell positional args ($1, $2).
PRICE = re.compile(
    r"\$\s?\d{1,3}(?:,\d{3})+(?:\.\d{2})?"
    r"|\$\s?\d+\.\d{2}"
    r"|\$\s?\d{3,}"
)

# Part-number shapes: two letters + two digits + suffix groups (AB99-1X2Y-3Z),
# four-digit prefix forms (1234-AB5C-XYZ), and bare 8-digit accessory SKUs
# (76000000-style).
PART_NUMBER = re.compile(
    r"\b(?:[A-Z]{2}\d{2}[A-Z0-9]*-[A-Z0-9]{2,6}-[A-Z0-9]{2,4}"
    r"|\d{4}-[A-Z]{2}[A-Z0-9]{2}-[A-Z]{3}"
    r"|76\d{6})\b",
    re.IGNORECASE,
)

# Josh's private fleet path — meaningless to a colleague, must not ship.
FLEET_PATH = re.compile(r"~?/Users/jflinn|~/agents/maven")

# Credential shapes.
SECRET = re.compile(r"AIza[0-9A-Za-z_-]{10,}|sk-[0-9A-Za-z]{20,}")

# Channel program tier names. Matched by SHAPE, not by enumeration — listing
# the real tier names here would publish them, which is exactly what this
# check exists to prevent.
TIER_NAME = re.compile(r"\b[A-Z][a-zA-Z]+\s+Deal\s+Reg\b|\bSPA[12]\b")

CHECKS = [
    (PRICE, "currency amount"),
    (PART_NUMBER, "Digi part number"),
    (FLEET_PATH, "private fleet path"),
    (SECRET, "credential-shaped string"),
    (TIER_NAME, "channel program tier name"),
]


def scan_text(text: str) -> list[str]:
    """Return a list of violation descriptions found in text."""
    found = []
    for pattern, label in CHECKS:
        for match in pattern.finditer(text):
            found.append(f"{label}: {match.group(0)!r}")
    return found


DOTFILES = {".env", ".envrc", ".netrc"}


def iter_text_files():
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and (path.suffix in TEXT_SUFFIXES or path.name in DOTFILES):
            yield path


def test_scanner_catches_a_real_price():
    assert scan_text("MSRP is $1,234 per unit")
    assert scan_text("Tier-A $567.89")


def test_scanner_catches_a_real_part_number():
    assert scan_text("AB99-1X2Y-3Z ships next quarter")
    assert scan_text("SKU# 76000000 is discontinued")
    assert scan_text("1234-AB5C-XYZ")


def test_scanner_catches_fleet_paths_and_secrets():
    assert scan_text("default='~/agents/maven/.env'")
    assert scan_text("key = AIzaSyD1234567890abcdef")


def test_scanner_catches_tier_names():
    assert scan_text("Example Deal Reg | SPA1")


def test_scanner_allows_placeholders():
    clean = "| {{PART_NUMBER}} | {{DESCRIPTION}} | {{REGION}} | {{MSRP}} | {{TIER_1}} |"
    assert scan_text(clean) == []


def test_scanner_allows_brand_hexes():
    assert scan_text("Digi green is #91D46C and navy is #1B4965") == []


def test_scanner_catches_round_dollar_amounts():
    assert scan_text("$500 per unit")
    assert scan_text("costs $1500 today")


def test_scanner_ignores_shell_positional_args():
    assert scan_text('echo "$1 and $2"') == []


def test_scanner_catches_lowercase_part_numbers():
    assert scan_text("the ab99-1x2y-3z ships")
    assert scan_text("the AB99-1x2y-3Z ships")


def test_dotfiles_are_walked():
    """A dotfile with no suffix must be reachable by the walker.

    Asserted behaviorally: removing the DOTFILES clause from iter_text_files
    must break this test. A set-membership check would not catch that.
    """
    probe = ROOT / ".env"
    assert not probe.exists(), "refusing to clobber an existing .env"
    probe.write_text("GEMINI_API_KEY=AIzaSyExampleNotARealKey123\n")
    try:
        walked = {p.resolve() for p in iter_text_files()}
        assert probe.resolve() in walked, ".env was not walked"
        assert scan_text(probe.read_text()), "walked but the secret was not flagged"
    finally:
        probe.unlink()


def test_no_sensitive_content_in_repo():
    violations = []
    self_path = Path(__file__).resolve()
    for path in iter_text_files():
        if path == self_path:
            # This file necessarily contains the patterns it hunts, so it must
            # exempt itself. That is inherent to a detection-fixture file, not
            # a defect — the defect would be real Digi data here. The
            # fixtures above are therefore required to be invented shapes,
            # never real prices, part numbers, or tier names.
            continue
        for hit in scan_text(path.read_text(encoding="utf-8", errors="replace")):
            violations.append(f"{path.relative_to(ROOT)}: {hit}")
    assert not violations, "Sensitive content found:\n" + "\n".join(violations)
