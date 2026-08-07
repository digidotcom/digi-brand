# Assets

## The official 2024 PowerPoint masters

Two masters, identical except for the classification footer their layouts
stamp. The deck's audience picks the file — see `skills/digi-pptx/SKILL.md`
(default when unclear: Confidential):

- `2024-Digi-Public-PPT-Template.potx` — footer `PUBLIC`; anything leaving Digi.
- `2024-Digi-Confidential-PPT-Template.potx` — footer `CONFIDENTIAL`; anything internal.

Each slide master supplies the green top bar, logo, classification footer,
brand fonts, and the correct 10 x 5.625" slide geometry. The Confidential
master is also the source of truth for the palette — `tools/extract_theme.py`
(run from a clone of this repo) reads the color values straight out of its
theme XML, so the palette in `skills/digi-brand-guidelines/SKILL.md` can never
drift from it (both masters carry the identical theme; the palette test checks
both).

## Fonts — `fonts/`

**Neither master embeds its fonts** (checked: zero `fntdata` parts). On a
machine without them installed, PowerPoint silently substitutes a fallback
face — every deck renders off-brand with no warning. Install them.

Vendored from Adobe's official repo
([github.com/adobe-fonts/source-sans](https://github.com/adobe-fonts/source-sans)),
license SIL OFL 1.1 — `fonts/OFL.txt` is the upstream license verbatim and
must travel with the font files. Both naming generations ship because the
masters' XML references both:

- **Source Sans Pro** (legacy 2.045R) — `SourceSansPro-*.otf`: Regular,
  Italic, Bold, Bold Italic, Semibold, Black. Families: `Source Sans Pro`,
  `Source Sans Pro Semibold`, `Source Sans Pro Black`.
- **Source Sans 3** (current 3.052R) — `SourceSans3-*.otf`: same weights.
  Families: `Source Sans 3`, `Source Sans 3 Semibold`, `Source Sans 3 Black`.

Install — **macOS**: select all `.otf` files in Finder, open, click "Install"
in Font Book (or copy them to `~/Library/Fonts/`). **Windows**: select all
`.otf` files, right-click → "Install for all users". Then restart PowerPoint.

## Logo — `logo/`

The official Digi logo set, as supplied by Digi brand assets, unmodified and
carrying its own filenames. Decks do not need it — the PowerPoint masters
already draw the logo — but any other artifact that needs a standalone
mark (a document cover, a web page, a one-off graphic) should place a file from
here rather than recreate the mark.

### Variants — which one to use

| Variant | When |
| --- | --- |
| `2c` | Default. Full color (green triangle + gray wordmark). Use unless one of the cases below applies. |
| `1c` | Single-color reproduction — printing constraints, one-color stamps, embroidery, etc. |
| `Rev` | Dark backgrounds. Reversed so the mark stays legible. |
| `Blk` | Black-only output — fax, thermal print, photocopy-safe documents. |

### Formats — which file to use

- **EPS** — vector. Use for print and anywhere the logo will be scaled; it
  never loses resolution.
- **PNG** — screen and documents. Transparent background.
- **JPG** — only where PNG is not accepted. It has no transparency (solid
  background), so prefer PNG whenever the destination supports it.

Color-space suffixes (`CMYK`, `PMS`, `RGB`) pick the reproduction method:
`CMYK` and `PMS` for print, `RGB` for anything on screen.

### The logo's color spec is fixed and separate from the theme palette

The logo carries its own color specification, supplied by Digi brand assets,
independent of the `digi-brand-guidelines` theme palette (`accent1`, `dk2`,
etc.). Both are legitimate — they answer different questions. The theme
palette governs everything you *design*: fills, text, charts, UI. The logo is
a fixed asset, reproduced exactly as supplied, never redesigned.

That means:

- **Never recolor the logo to match the theme palette.** Place the file as
  given; do not retint the mark toward `accent1` or `dk2`.
- **Never sample colors out of the logo for use in design elements.** A color
  picked off the logo file is not a verified theme value. Use the palette in
  `skills/digi-brand-guidelines/SKILL.md` for anything you design.
- **You never need the logo's hex values.** You never redraw the logo; you
  place the file. Its exact color values are not documented here or anywhere
  else in this repo — that omission is deliberate, not a gap, and keeps
  `tests/test_palette.py`'s off-palette-hex guard absolute rather than
  growing exceptions.
