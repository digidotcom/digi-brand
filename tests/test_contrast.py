import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from contrast import contrast_ratio, table  # noqa: E402

SPINE = ROOT / "skills" / "digi-brand-guidelines" / "SKILL.md"

# Matches a table row like: | `#1B4965` navy | 9.60:1 | Yes | Yes |
ROW = re.compile(r"\|\s*`#([0-9A-Fa-f]{6})`[^|]*\|\s*([0-9.]+):1\s*\|")


def test_known_ratios():
    """Anchor the formula itself against values computed independently."""
    assert round(contrast_ratio("91D46C", "FFFFFF"), 2) == 1.77
    assert round(contrast_ratio("1B4965", "FFFFFF"), 2) == 9.60
    assert round(contrast_ratio("FFFFFF", "FFFFFF"), 2) == 1.0
    assert round(contrast_ratio("000000", "FFFFFF"), 2) == 21.0


def test_spine_table_matches_computed_ratios():
    """Every ratio printed in the spine must match the formula."""
    computed = {hex_color: ratio for hex_color, _, ratio, _, _ in table()}
    text = SPINE.read_text()
    found = {}
    for match in ROW.finditer(text):
        found[match.group(1).upper()] = float(match.group(2))
    assert found, "no contrast rows parsed from the spine — did the table format change?"
    for hex_color, stated in found.items():
        assert hex_color in computed, f"#{hex_color} in the table is not in the palette"
        assert stated == computed[hex_color], (
            f"#{hex_color}: spine says {stated}:1, formula says {computed[hex_color]}:1"
        )


def test_every_palette_color_appears_in_the_table():
    text = SPINE.read_text().upper()
    for hex_color, _, _, _, _ in table():
        assert hex_color in text, f"#{hex_color} missing from the accessibility table"


def test_green_never_passes():
    ratio = contrast_ratio("91D46C", "FFFFFF")
    assert ratio < 3.0, "green must fail even the large-text threshold"


def test_no_role_recommends_a_color_that_fails_as_text():
    """The role map must not assign a text role to a color the table fails.

    The spine previously listed #00B7FF (2.28:1) under "Followed links", which
    is a text role, while its own table rated that color unreadable.
    """
    failing = {
        hex_color for hex_color, _, _, passes_body, _ in table() if not passes_body
    }
    text = SPINE.read_text()
    role_map = text.split("### Role map", 1)[1].split("###", 1)[0]
    for line in role_map.splitlines():
        if not line.strip().startswith("-"):
            continue
        lowered = line.lower()
        names_text_role = any(
            word in lowered for word in ("text:", "headings:", "link text:")
        )
        if not names_text_role:
            continue
        for hex_color in failing:
            assert hex_color.lower() not in lowered, (
                f"role line recommends #{hex_color} for a text role, "
                f"but it fails AA for body text: {line.strip()}"
            )
