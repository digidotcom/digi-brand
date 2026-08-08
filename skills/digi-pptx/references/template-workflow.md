# Template-Edit Workflow (Preferred)

The bundled official masters have a proper PowerPoint slide master that automatically provides the green top bar, DIGI logo, and the classification footer on every content slide. Editing a master is **significantly easier** than rebuilding the chrome from scratch with pptxgenjs.

## When to use this workflow

**Always.** Every Digi slide — a full deck, a closing slide, or a single one-off — is built by editing a master. There is no from-scratch path (see `SKILL.md` → Workflow Decision for why). The master carries the green bar, logo, footer, fonts, and the correct **10 × 5.625"** geometry; rebuilding any of that by hand is more work and never matches.

## The Workflow

### 1. Choose the master by classification, copy it to a working location

Pick per `SKILL.md` → Template location: **PUBLIC** for anything leaving Digi, **CONFIDENTIAL** for anything internal. **If it is unclear, ask** — do not guess; only fall back to CONFIDENTIAL when there is no one to ask (headless or scheduled run), and say so in the result. The footer classification comes from this choice — it is never typed by hand.

```bash
cp ${CLAUDE_PLUGIN_ROOT}/assets/2024-Digi-Confidential-PPT-Template.potx /home/claude/working-deck.pptx
# or 2024-Digi-Public-PPT-Template.potx for an external deck
```

The masters are `.potx` (template) files. When you unpack, edit, and repack to a `.pptx`, also flip the content type in `[Content_Types].xml`: the `/ppt/presentation.xml` override must change from `...presentationml.template.main+xml` to `...presentationml.presentation.main+xml`, or PowerPoint treats the output as a template.

### 2. Inspect what's in the master

```bash
extract-text /home/claude/working-deck.pptx
```

Each master ships with **35 layouts**, of which **nine are in scope** (inventory below — the rest are a human's menu, not ours), plus two starter slides:
- **Slide 1**: Title slide (layout "1_Generic Deck Title" — placeholder title, name/date)
- **Slide 2**: Content slide (layout "1_Bullets (1-line head)" — header + bullet body)

There is no bundled Thank You slide; build a closing slide from the title layout if the deck needs one.

### 3. Pick a layout per slide — then edit

**Pick the layout from the inventory below before writing any XML.** slideLayout3 ("1_Bullets") is not "the content layout" — it is one of nine, and a deck that uses only it looks like one slide repeated with different words. Every slide's content shape should choose its layout.

> **Locating the base `pptx` skill.** This workflow leans on the sibling `pptx` skill for the unpack/edit/repack scripts. Its path depends on the environment: in Claude Code CLI it's `~/.claude/skills/pptx/`, in Claude Desktop it's `/mnt/skills/public/pptx/`. Below, `<pptx>` means whichever applies. Invoke/read the `pptx` skill first.

For text edits and adding content slides, follow the workflow in `<pptx>/editing.md` — that's the canonical guide. The high-level pattern:
1. Unpack the .pptx → `python <pptx>/scripts/office/unpack.py working-deck.pptx unpacked/`
2. Duplicate `ppt/slides/slide2.xml` (+ its `.rels`) once per new slide, register each in `presentation.xml` / `.rels` / `[Content_Types].xml`
3. **Re-point each new slide's `.rels` at the chosen layout** — change the `slideLayout` relationship target to `../slideLayouts/slideLayoutN.xml`
4. **Match the slide's placeholders to that layout**: each `<p:sp>` you keep must carry a `<p:ph type="..." idx="..."/>` that exists on the layout (idx values are in the inventory). A placeholder `<p:sp>` with no `<a:xfrm>` inherits the layout's position and styling — that is what you want; only add explicit geometry for extra non-placeholder shapes.
5. Repack → `python <pptx>/scripts/office/pack.py unpacked/ output.pptx`

### 4. Standard QA

Follow the QA flow in `<pptx>/SKILL.md` — convert to images and verify:
- Content fits in placeholders
- Footer renders correctly
- Green top bar is present (comparison-table layouts are the one deliberate exception — see inventory)
- No overflow or cut-off text

## Layout inventory — the nine you use

The masters carry 35 layouts. **Nine are in scope; the rest are deliberately not documented.** They are not broken — they are a menu built for a person dragging boxes in PowerPoint, and most differ from one another only by a small green nub and a placeholder arrangement you can produce at any coordinate. Every layout listed here earns its place either by drawing brand artwork that cannot be recreated, or by being one a Digi colleague expects to see when they open the deck and edit it themselves. Selected by Josh Flinn, 2026-08-07, from rendered pixels.

Verified facts, so you don't re-derive them:
- Layout **names, numbering, and all content-placeholder geometry are identical in BOTH masters**. The only difference is footer chrome: the Confidential master's slide-number/footer placeholders are `idx="10"`/`idx="11"`, the Public master's are `idx="2"`/`idx="3"`, shifted 0.10" right. You never touch those, so nothing to handle — just don't hardcode footer idx if you copy footer `<p:sp>` elements between masters.
- Each potx contains **five slide masters** internally. All layouts live in one flat `slideLayouts/` directory, so for XML editing the split doesn't matter; it matters only if you iterate `slide_layouts` via python-pptx (iterate all `slide_masters`).
- Geometry is inches on the 10 × 5.625" canvas, from the layout XML, as `x, y, w × h`. The footer band (logo, page number, classification) sits at y ≈ 5.44 on content layouts and is master chrome — never touched.

### Decision rule: content → layout

| The slide is… | Use | Layout |
|---|---|---|
| Deck opening / closing | Generic Deck Title | 1 |
| Deck opening that wants a photograph | **Photo Deck Title** | 35 |
| A topic change | Section Divider | 2 |
| Plain prose points | Bullets | 3 |
| Text under a category/eyebrow label (left) | Left tab + left text | 7 |
| Same, without pushing the title right | Right tab | 13 |
| Free-form: diagrams, cards, stat callouts, image zones | Generic slide | 21 |
| A product/feature shot with text beside it | Product slide (native picture) | 23 |
| An image or screenshot on a styled panel | Gray panel (native picture) | 31 |

**Only the `(1-line head)` variants are in scope.** Each of these has a `(2-line head)` twin whose sole difference is a taller title box — 0.73" instead of 0.42", body pushed from y 0.85 to y 1.17. That is two numbers, not a design. If a title wraps past one line (roughly 55+ characters at 36pt), **widen the title box and drop the body yourself** on the 1-line layout rather than switching files.

**Native picture placeholders (23, 31): fill them; do not reach for a zone.** These layouts already put the image where the design wants it, with panel chrome behind it. Place the image AT the placeholder geometry below — `place_image.py --x --y --w --h` with those exact values, `--fit` for screenshots. The named zones in `visuals.md` (`right-half`, `hero`, …) exist for layouts with **no** picture placeholder (Bullets, Generic). Using a zone on 23 or 31 is what makes every image land in the same hand-computed box instead of the designed one.

### 1 — `1_Generic Deck Title`

Light gray diagonal panel over white, DIGI logo top-left, layered green triangle motif bottom-right. All decoration is layout chrome — edit only the two placeholders.
- title: 0.47, 1.40, 7.00 × 2.70 · name/date body `idx="10"`: 0.47, 4.11, 7.00 × 1.00

### 35 — `Photo Deck Title` (photograph behind the title)

The same diagonal as layout 1, filled instead as a **translucent dark scrim** (`202123` at 62% opacity) over a full-bleed photograph: the image reads dimmed on the left where the title sits and at full strength on the right. Logo, green triangles, and title sit on top. Same placeholder geometry as layout 1 (body is `idx="1"` here).

**The photograph is a slide BACKGROUND, never a picture on the slide.** OOXML renders slide background → master → layout → slide, so anything placed on the slide draws *above* the scrim and chrome and destroys the design. Use the dedicated script:

```bash
# one of the four library photographs
python3 scripts/set_title_photo.py --unpacked unpacked/ --slide 1 --photo night-city-connections
python3 scripts/set_title_photo.py --list          # what's available

# or any custom image
python3 scripts/set_title_photo.py --unpacked unpacked/ --slide 1 --image work/site.jpg
```

Pick a photograph whose subject sits on the **right** — the scrim covers the left, and a busy left side fights the title. With no photo set the layout renders as scrim-over-white, which is a valid if plain fallback. The library is `assets/photos/` and is **not in git** (third-party licensed stock; see `assets/photos/README.md` to populate it).

### 2 — `1_Generic Section Divider`

Large light-gray diagonal panels fill the slide (denser than the title look), big title mid-left, optional one-line subhead below, logo bottom-left, green triangle bottom-right. Use at every topic change in a deck of any length — it is the visual breather that stops the bullets-blur.
- title (inherited): 0.50, 1.23, 6.66 × 2.30 · subhead body `idx="12"`: 0.50, 3.70, 6.66 × 1.10

### 3 — `1_Bullets (1-line head)`

The plain content slide: standard chrome, body styled as a bullet list, green corner triangle bottom-right. The workhorse — but a deck built only from this reads as one slide repeated, which is the reason the rest of this list exists.
- title 0.38, 0.38, 9.15 × 0.42 · body `idx="12"` 0.38, 0.85, 9.15 × 4.22

### 7 — `1_Left tab + left text (1-line head)`

A **green ribbon tab over the top-left edge** carrying a short category/eyebrow label in white. Use when slides belong to a labeled track ("SECURITY", "ROADMAP") and the deck should show it. Title and body are indented right to clear the tab.
- tab `idx="13"` 0.71, 0.05, 2.84 × 0.22 · title 1.00, 0.62, 8.54 × 0.42 · body `idx="14"` 1.00, 1.10, 8.54 × 3.97

### 13 — `1_Right tab (1-line head)`

Same eyebrow-label idea with the tab at top-**right**, so the title keeps its normal full-width position. Use when the label should not push the title inward.
- tab `idx="13"` 6.31, 0.03, 2.84 × 0.22 · title 0.38, 0.38, 9.15 × 0.42 · body `idx="14"` 0.38, 0.85, 9.15 × 4.22

### 21 — `1_Generic slide (1-line head)`

The free-form canvas: standard chrome, plain body, no corner triangle. Shape-built diagrams, stat callouts, card grids, and the named image zones from `visuals.md` belong **here** — never on a picture-placeholder layout.
- title 0.38, 0.38, 9.15 × 0.42 · body `idx="12"` 0.38, 0.85, 9.15 × 4.22

### 23 — `1_Generic product slide (1-line head)` — native picture, right

White slide with a **picture placeholder filling the right column**, green triangle tucked behind its bottom corner. Made for a product or feature shot with text beside it.
- title 0.38, 0.38, 9.15 × 0.42 · body `idx="12"` 0.38, 0.85, 9.15 × 4.22 · **pic `idx="13"` 5.62, 0.38, 3.91 × 4.69**
- ⚠ The body placeholder is full-width and runs **under** the picture — keep body text inside x ≤ 5.4 (about 5.0" usable) or it disappears behind the image.

### 31 — `9_Gray panel (1-line head)` — native picture on a styled panel

The right ~40% is a **light-gray panel** with a full-height picture placeholder on it, green triangle bottom-right. The text column is properly narrowed to 5.12", so unlike layout 23 there is no under-image overlap. Use for screenshots or images that deserve a framed presentation.
- title 0.38, 0.38, 5.12 × 0.42 · body `idx="12"` 0.38, 0.85, 5.12 × 4.22 · **pic `idx="13"` 5.62, 0.38, 3.91 × 4.70**

### Not in scope — and one worth knowing about

The undocumented layouts include bullets/subhead variants, further tab permutations, two-content sidebars, sliced-panel variants, comparison tables, and every `(2-line head)` twin. Compose what they'd give you on **21 (Generic)** instead.

One deserves a specific warning, because it looks the most appealing and is the most misleading: **`Gray panel + tab + icons` (layouts 27–30) carries three fixed teal icons — padlock, link, wi-fi — drawn into the layout as embedded `<p:pic>` chrome.** They cannot be swapped or removed per slide, and they assert security/connectivity/wireless whatever the slide actually says. Don't reach for it because it looks rich; build a stat or icon row on 21 instead.

## Important: Don't Touch the Slide Master

The slide master provides the green bar, logo, and classification-footer chrome. Don't try to "improve" these — they're the brand standard. The footer in particular is **never retyped**: if it shows the wrong classification, switch to the other master. If you need a slide without the master decoration (rare), create a new slide that doesn't reference the master, but this is almost never what you want.

## Single one-off slide

When the ask is one content slide to drop into another deck, still start from the classification-correct master, then trim:

1. Copy the master, unpack it (`unpack.py working-deck.pptx unpacked/`).
2. Edit the content slide (`ppt/slides/slide2.xml`) — re-point its layout first if the content wants a different family (step 3 above), then see "Injecting styled content" below.
3. Trim the deck to that one slide by editing `ppt/presentation.xml`'s `<p:sldIdLst>` to keep only the content slide's `<p:sldId>` (the one whose `r:id` maps to `slides/slide2.xml` in `ppt/_rels/presentation.xml.rels`). Leaving the other slide parts on disk is harmless; PowerPoint shows only what's in `sldIdLst`.
4. Repack (`pack.py unpacked/ out.pptx`) and QA-render.

The recipient pastes the single slide into their deck and the master chrome travels with it.

## Injecting styled content

Placeholder geometry for every layout is in the inventory above. Either fill the layout's placeholders (preferred — they carry position and styling for free), or add your own `<p:sp>` shapes inside `<p:spTree>` (insert before `</p:spTree>`) with explicit geometry in EMU (`inches × 914400`). Custom shapes don't inherit fonts, so set them explicitly: `Source Sans Pro` for text, `Consolas` for code/prompts, and brand colors from the `SKILL.md` palette (Navy `1B4965`, Green `91D46C`, Dark Gray `3F4245`, Ice Blue `E2F6FF` for callout fills, Silver `DAD8D8` for borders). A reusable Python shape-emitter (off/ext in EMU, `solidFill`, runs with `<a:latin typeface=...>`) is the fastest way to lay out cards, eyebrows, and callouts — keep it in the working dir, not the skill. Custom composition belongs on the Generic layouts (21/22); don't fight a picture-placeholder layout with overlapping shapes.

QA every slide by converting to PDF then PNG (`soffice.py --headless --convert-to pdf` → `pdftoppm -png`) and visually inspecting before declaring done.

## Title and Closing Slides

The title slide (layout "1_Generic Deck Title") includes:
- Light gray diagonal panel over white — no photo, no gradient
- DIGI logo top-left
- Title placeholder (navy/dark from the theme), name/date placeholder below in Medium Gray
- Layered green triangle motif bottom-right (layout chrome)

Just edit the placeholder text — all decoration is layout chrome and stays untouched. There is no bundled Thank You slide; reuse the title layout for a closing slide.
