# Assets

## digi-template.pptx

The official Digi PowerPoint template. Its slide master supplies the green top
bar, footer, brand fonts, and the correct 10 x 5.625" slide geometry. It is also
the source of truth for the palette — `tools/extract_theme.py` (run from a
clone of this repo) reads the color values straight out of its theme XML, so
the palette in `skills/digi-brand-guidelines/SKILL.md` can never drift from it.

## Logo — `logo/`

The official Digi logo set, as supplied by Digi brand assets, unmodified and
carrying its own filenames. Decks do not need it — `digi-template.pptx`'s slide
master already draws the logo — but any other artifact that needs a standalone
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
