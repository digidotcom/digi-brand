#!/usr/bin/env python3
"""Extract the brand palette and fonts from a Digi PowerPoint master.

The master's theme XML is the single source of truth for Digi's colors. Every
hex value in this repo is checked against it, so the palette can never drift the
way it did when digi-brand-guidelines and digi-pptx disagreed on navy. Both
official 2024 masters (Confidential and Public) carry the identical theme;
default target is the Confidential one.
"""
import re
import sys
import zipfile
from pathlib import Path

SLOT_ORDER = [
    "dk1", "lt1", "dk2", "lt2",
    "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
    "hlink", "folHlink",
]


def extract(pptx_path: Path) -> dict[str, str]:
    """Return {slot: HEX} for every color slot in the template's theme."""
    with zipfile.ZipFile(pptx_path) as zf:
        xml = zf.read("ppt/theme/theme1.xml").decode("utf-8")
    scheme = re.search(r"<a:clrScheme.*?</a:clrScheme>", xml, re.S).group(0)
    colors = {}
    pattern = re.compile(
        r"<a:(\w+)>\s*<a:(?:srgbClr val=\"([0-9A-Fa-f]{6})\""
        r"|sysClr[^>]*lastClr=\"([0-9A-Fa-f]{6})\")"
    )
    for match in pattern.finditer(scheme):
        slot = match.group(1)
        value = (match.group(2) or match.group(3)).upper()
        colors[slot] = value
    return colors


def extract_fonts(pptx_path: Path) -> dict[str, str]:
    """Return {'majorFont': name, 'minorFont': name}."""
    with zipfile.ZipFile(pptx_path) as zf:
        xml = zf.read("ppt/theme/theme1.xml").decode("utf-8")
    scheme = re.search(r"<a:fontScheme.*?</a:fontScheme>", xml, re.S).group(0)
    fonts = {}
    for match in re.finditer(
        r"<a:(majorFont|minorFont)>\s*<a:latin typeface=\"([^\"]*)\"", scheme
    ):
        fonts[match.group(1)] = match.group(2)
    return fonts


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent
        / "assets" / "2024-Digi-Confidential-PPT-Template.potx"
    )
    palette = extract(path)
    for slot in SLOT_ORDER:
        print(f"{slot:10s} #{palette[slot]}")
    for name, value in extract_fonts(path).items():
        print(f"{name:10s} {value}")
