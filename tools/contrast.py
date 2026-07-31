#!/usr/bin/env python3
"""Compute WCAG 2.1 contrast ratios for the Digi palette against white.

The accessibility table in digi-brand-guidelines is generated from this, not
hand-written. Hand-written ratios drift and are never re-checked; a wrong
accessibility claim in a brand skill is worse than no claim at all.
"""
WHITE = "FFFFFF"

PALETTE = {
    "1B4965": "navy",
    "3F4245": "dark gray",
    "56565A": "medium gray",
    "1F7FA5": "teal",
    "CC6033": "orange",
    "00B7FF": "bright blue",
    "91D46C": "green",
}


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        for c in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def table():
    """Return [(hex, name, ratio, passes_body, passes_large)]."""
    rows = []
    for hex_color, name in PALETTE.items():
        ratio = contrast_ratio(hex_color, WHITE)
        rows.append((hex_color, name, round(ratio, 2), ratio >= 4.5, ratio >= 3.0))
    return rows


if __name__ == "__main__":
    for hex_color, name, ratio, body, large in table():
        print(f"#{hex_color}  {name:14s} {ratio:6.2f}:1  body={body!s:5s} large={large}")
