import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from extract_theme import extract, extract_fonts  # noqa: E402

MASTERS = [
    ROOT / "assets" / "2024-Digi-Confidential-PPT-Template.potx",
    ROOT / "assets" / "2024-Digi-Public-PPT-Template.potx",
]

PALETTE = {
    "dk1": "1B4965",
    "lt1": "FFFFFF",
    "dk2": "3F4245",
    "lt2": "F5F7F7",
    "accent1": "91D46C",
    "accent2": "DAD8D8",
    "accent3": "1F7FA5",
    "accent4": "CC6033",
    "accent5": "E2F6FF",
    "accent6": "56565A",
    "hlink": "1F7FA5",
    "folHlink": "00B7FF",
}

ALLOWED_HEXES = set(PALETTE.values()) | {
    "000000",  # pure black, legal for body text in generated documents
}

HEX_IN_TEXT = re.compile(r"#([0-9A-Fa-f]{6})\b")

# "assets" is deliberately NOT skipped: binaries (.pptx, .png) are already
# excluded by TEXT_SUFFIXES below, so skipping the whole directory buys no
# performance and only hides text files (e.g. assets/README.md) from the guard.
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".css", ".html"}


def iter_text_files():
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def test_master_themes_match_declared_palette():
    for master in MASTERS:
        assert extract(master) == PALETTE, master.name


def test_navy_is_1b4965():
    for master in MASTERS:
        assert extract(master)["dk1"] == "1B4965", master.name


def test_fonts_are_source_sans_pro():
    for master in MASTERS:
        fonts = extract_fonts(master)
        assert fonts["majorFont"] == "Source Sans Pro", master.name
        assert fonts["minorFont"] == "Source Sans Pro", master.name


def test_no_off_palette_hex_anywhere_in_repo():
    violations = []
    for path in iter_text_files():
        if path.name == "test_palette.py":
            continue  # declares the palette, including the banned old navy
        for match in HEX_IN_TEXT.finditer(path.read_text(encoding="utf-8", errors="replace")):
            value = match.group(1).upper()
            if value not in ALLOWED_HEXES:
                violations.append(f"{path.relative_to(ROOT)}: #{value}")
    assert not violations, "Off-palette hex values:\n" + "\n".join(violations)


def test_old_navy_never_appears():
    for path in iter_text_files():
        if path.name == "test_palette.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        assert "1B4964" not in text.upper(), f"{path.relative_to(ROOT)} has the old navy"
