---
name: digi-brand-guidelines
description: Digi International's official brand — the verified color palette, typography stack, logo rules, accessibility constraints, and brand voice. This is the single source of truth every other Digi skill reads. Use it whenever brand colors, fonts, visual formatting, or company design standards apply to an artifact, and read it before choosing any color for a Digi deliverable.
license: MIT
---

# Digi International Brand

The normative source for Digi's visual identity. Every value here is extracted
from the official PowerPoint template's theme XML
(`assets/2024-Digi-Confidential-PPT-Template.potx` → `ppt/theme/theme1.xml`;
the Public master carries the identical theme), not transcribed by hand.
Regenerate by running `python3 tools/extract_theme.py` from a clone of this repo.

## Palette

| Slot | Hex | Role |
| --- | --- | --- |
| dk1 | `#1B4965` | Navy. Title backgrounds, dark accents, headings on light |
| lt1 | `#FFFFFF` | White. Content backgrounds, text on dark |
| dk2 | `#3F4245` | Dark gray. Primary body text |
| lt2 | `#F5F7F7` | Light gray. Subtle backgrounds, table zebra rows |
| accent1 | `#91D46C` | Digi green. Fills, bullets, icons, rules — never on light backgrounds as text; see Accessibility |
| accent2 | `#DAD8D8` | Silver. Borders, dividers |
| accent3 | `#1F7FA5` | Teal. Table headers, secondary accent |
| accent4 | `#CC6033` | Orange. Warnings, call-to-action, NDA badge |
| accent5 | `#E2F6FF` | Ice blue. Highlight backgrounds, alternating table rows |
| accent6 | `#56565A` | Medium gray. Secondary and muted text |
| hlink | `#1F7FA5` | Links |
| folHlink | `#00B7FF` | Followed links (theme value) — fails AA as text; see Accessibility |

### Role map

Pick by role, not by taste.

- **Primary text:** `#3F4245` on white or `#F5F7F7`
- **Secondary text:** `#56565A`
- **Headings:** `#1B4965`
- **Text on dark:** `#FFFFFF` on `#1B4965`
- **Primary fill / brand moment:** `#91D46C`
- **Secondary fill / structure:** `#1F7FA5`
- **Link text:** `#1F7FA5` — the only link color that clears AA for body text
- **Followed links / interactive accents:** `#00B7FF` is the theme's `folHlink`
  value, but at 2.28:1 it fails AA even for large text. Use it for non-text
  interactive accents — focus rings, active-state fills, hover indicators —
  never for link text on a light background. When a followed-link state must be
  conveyed in text, use `#1F7FA5` with an underline or weight change instead.
- **Warning, deadline, or CTA:** `#CC6033`
- **Borders and rules:** `#DAD8D8`
- **Highlight or alternating rows:** `#E2F6FF`
- **Categorical chart series, in order:** `#1F7FA5`, `#91D46C`, `#CC6033`,
  `#56565A`, `#00B7FF`, `#1B4965`

### Accessibility

Contrast against white (`#FFFFFF`). WCAG AA needs 4.5:1 for body text and
3:1 for large text (18pt+, or 14pt+ bold).

| Foreground | Ratio vs white | Body text | Large text |
| --- | --- | --- | --- |
| `#1B4965` navy | 9.60:1 | Yes | Yes |
| `#3F4245` dark gray | 10.11:1 | Yes | Yes |
| `#56565A` medium gray | 7.31:1 | Yes | Yes |
| `#1F7FA5` teal | 4.53:1 | Yes, barely | Yes |
| `#CC6033` orange | 3.97:1 | No | Yes |
| `#00B7FF` bright blue | 2.28:1 | No | No |
| `#91D46C` green | 1.77:1 | Never on light | Never on light |

**Teal is the one to watch.** At 4.53:1 it clears the 4.5:1 body-text threshold by
0.03. It passes, but it has no margin — any darkening of the background or use of
a lighter teal breaks it. Prefer `#1B4965` or `#3F4245` for sustained reading.

**The green rule.** `#91D46C` is a fill color, not a text color, on white or any
light background — 1.77:1 fails even the large-text floor, so never set text in
it and never put text on it there. It is permitted for large display text
(18pt+, or 14pt+ bold) on `#1B4965` navy, where it measures 5.41:1 and clears
AA — a title-slide headline, for instance. Dark text (`#1B4965` or `#3F4245`)
on a green fill is fine on any background. When a chart or diagram needs green
to carry meaning, pair it with a label or a shape difference — color alone is
not an accessible signal.

Ratios use the WCAG 2.1 relative-luminance formula against white, rounded to two
decimals. They are **computed, not transcribed** — `python3 tools/contrast.py`
(run from a clone of this repo) regenerates them, and `tests/test_contrast.py`
fails if this table drifts from what the formula produces. Treat any pair not
in this table as unverified until measured.

## Typography

- **Primary:** Source Sans Pro. Both `majorFont` and `minorFont` in the theme.
- **Fallbacks, in order:** Source Sans 3, Arial, sans-serif.
- **Headings:** Source Sans Pro Semibold or Bold.
- **Body:** Source Sans Pro Regular.
- **Code:** Consolas.
- Source Sans 3 is the current Google Fonts name for the same typeface:
  https://fonts.google.com/specimen/Source+Sans+3

CSS stack:

```css
font-family: "Source Sans Pro", "Source Sans 3", Arial, sans-serif;
```

## Logo

Official files live at `${CLAUDE_PLUGIN_ROOT}/assets/logo/`. See that
directory's `README.md` for the full variant/format table; the essentials:

- The mark is the DIGI wordmark with a green triangle set at 45°.
- The triangle points up and out — forward movement and radio transmission.
- **2c** (full color) is the default. **1c** for single-color reproduction.
  **Rev** on dark backgrounds. **Blk** for black-only output.
- **EPS** is vector — use for print and any scaling. **PNG** for screen and
  documents. **JPG** only where PNG is not accepted (no transparency).
- Never distort, re-color, rotate, or separate the triangle from the wordmark.
- Never place the logo on a background that reduces the triangle's contrast
  below legibility. On dark backgrounds use the reversed (`Rev`) version.
- **Never recolor the logo to match the theme palette, and never sample
  colors out of the logo for design elements.** The logo carries its own
  fixed color spec, separate from the theme palette above — reproduce the
  file as supplied; use the theme palette for anything you design.

## Brand voice

Digi communicates:

- **Precision** — clean, technical, exact. Numbers over adjectives.
- **Connection** — IoT connectivity, networking, the link between things.
- **Forward movement** — progress, the next generation, the upgrade path.
- **Modern technology** — bright, fresh, current without being faddish.

In prose: plain and professional. Lead with what the reader must do or know.
No exclamation marks in technical or channel-facing material.

## For skill authors

Other skills in this plugin read this file rather than restating it:

> Read `${CLAUDE_PLUGIN_ROOT}/skills/digi-brand-guidelines/SKILL.md` for the
> palette, type stack, and accessibility rules.

Each also carries an inline fallback palette so a single skill folder copied
into another harness still works. When the brand changes, edit this file first,
then update the fallbacks — `python3 -m pytest tests/test_palette.py` fails if
any file disagrees.
