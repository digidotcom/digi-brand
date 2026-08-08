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

Each master ships with **34 layouts** (`ppt/slideLayouts/slideLayout1..34.xml` — full inventory below) and two starter slides:
- **Slide 1**: Title slide (layout "1_Generic Deck Title" — placeholder title, name/date)
- **Slide 2**: Content slide (layout "1_Bullets (1-line head)" — header + bullet body)

There is no bundled Thank You slide; build a closing slide from the title layout if the deck needs one.

### 3. Pick a layout per slide — then edit

**Pick the layout from the inventory below before writing any XML.** slideLayout3 ("1_Bullets") is not "the content layout" — it is one of 34, and a deck that uses only it looks like one slide repeated with different words. Every slide's content shape should choose its layout.

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

## Layout inventory — the 34 layouts, verified from the potx and from renders

Verified facts, so you don't have to re-derive them:
- Layout **names, numbering, and all content-placeholder geometry are identical in BOTH masters** (extracted from each potx's XML). The only difference is footer chrome: the Confidential master's slide-number/footer placeholders are `idx="10"`/`idx="11"`, the Public master's are `idx="2"`/`idx="3"`, shifted 0.10" right. You never touch those placeholders, so nothing to handle — just don't hardcode footer idx if you ever copy footer `<p:sp>` elements between masters.
- Each potx contains **five slide masters** internally: title (L1), divider (L2), general content (L3–L22), picture/panel content (L23–L32), comparison table (L33–L34). All 34 layouts live in one flat `slideLayouts/` directory, so for XML editing the split doesn't matter; it only matters if you iterate `slide_layouts` via python-pptx (iterate all `slide_masters`).
- Geometry below is inches on the 10 × 5.625" canvas, from the layout XML, as `x, y, w × h`. The footer band (logo, page number, classification) sits at y ≈ 5.44 on every content layout and is master chrome — never touched.

### Decision rule: content → layout family

Pick by what the slide's content IS:

| The slide is… | Use family | Layouts |
|---|---|---|
| Deck opening / closing | Title | 1 |
| A topic change | Section divider | 2 |
| Plain prose points | Bullets | 3/4 |
| A one-line takeaway + supporting points | Subhead + bullets | 5/6 |
| Text under a category/eyebrow label | Left-tab or right-tab text | 7–12, 13/14 |
| A narrow sidebar + a wide main area | Left tab + 2 content | 15–20 |
| Free-form or custom-composed (diagrams, cards, stat callouts, image zones) | Generic slide | 21/22 |
| A product/feature shot with text beside it | Product slide (native picture) | 23/24 |
| An image or screenshot presented on a styled panel | Gray panel (native picture) | 25/26, 31/32 |
| A small image + caption with IoT-flavored icon accents | Gray panel + tab + icons (native picture) | 27–30 |
| Side-by-side / vs. / feature-matrix content | Comparison table | 33/34 |

**1-line vs 2-line head — pick by title length, every time.** Every content family comes in a pair: the "(1-line head)" layout has a 0.42"-tall title band with the body starting at y 0.85; the "(2-line head)" layout has a 0.73" band with the body at y 1.17. A long title on a 1-line layout overflows the band; a short title on a 2-line layout wastes a 0.32" strip of content space. Estimate: a title over ~55 characters at 36pt needs the 2-line layout.

**Native picture placeholders (layouts 23–32): fill them, don't re-invent them.** These layouts already position the image where the design wants it, with panel chrome behind it. Put the image AT the picture placeholder's geometry (from the tables below) — `place_image.py --x --y --w --h` with those exact values, `--fit` for screenshots. Do **not** reach for the named zones (`right-half`, `hero`, …) on these layouts; the zones in `visuals.md` exist for layouts with **no** picture placeholder (bullets, generic). This is the difference between "the image keeps ending up in the same right-hand box" and using the design.

### Title / divider (layouts 1–2)

**1 — `1_Generic Deck Title`.** Light gray diagonal panel over white, DIGI logo top-left, layered green triangle motif bottom-right. All decoration is layout chrome — edit only the two placeholders.
- title: 0.47, 1.40, 7.00 × 2.70 · name/date body `idx="10"`: 0.47, 4.11, 7.00 × 1.00

**2 — `1_Generic Section Divider`.** Large light-gray diagonal panels fill the slide (denser than the title look), big title mid-left, optional one-line subhead below, logo bottom-left, green triangle bottom-right. Use at every topic change in a deck of any length — it is the visual breather that stops the bullets-blur.
- title (inherited): 0.50, 1.23, 6.66 × 2.30 · subhead body `idx="12"`: 0.50, 3.70, 6.66 × 1.10

### Text layouts (3/4 Bullets · 5/6 Subhead + bullets · 21/22 Generic) — styling, not capability

Pure text arrangements, no branded decoration beyond the standard chrome. A text box can be placed at any coordinate on any layout, so these buy **inherited text styling**, not placement capability: 3/4 style the body as a bullet list (the workhorse every deck previously over-used); 5/6 style the first outline level as an **unbulleted subhead** (lead with the takeaway, bullets from level 2); 21/22 leave the body plain, drop the corner triangle, and are the **free-form canvas** — shape-built diagrams, stat callouts, card grids, and the named image zones from `visuals.md` belong here (or on Bullets), never on a picture-placeholder layout.
- All six share one geometry: title 0.38, 0.38, 9.15 × 0.42|0.73 · body `idx="12"` 0.38, 0.85, 9.15 × 4.22 (2-line: 0.38, 1.17, 9.15 × 3.90). One quirk: layout 6 narrows title and body to **9.00** wide — the template's own inconsistency, not a typo.

### Tab-labeled text (layouts 7–12 left tab · 13/14 right tab)

A **green ribbon tab over the top edge** carries a short category/eyebrow label (white text on green). Use when slides belong to a labeled track ("SECURITY", "ROADMAP") and the deck should show it. Left-tab variants add **teal trapezoid tabs on the bottom edge** for secondary labels (source, product line, section marker).
- **7/8 (left tab):** tab `idx="13"` 0.71, 0.05, 2.84 × 0.22 · title indented to 1.00, 0.62, 8.54 × 0.42|0.73 · body `idx="14"` 1.00, 1.10, 8.54 × 3.97 | 1.00, 1.40, 8.54 × 3.66
- **9/10:** adds bottom-right teal tab `idx="15"` 7.12, 5.40, 2.31 × 0.22 · **11/12:** adds a second bottom tab `idx="16"` 4.02, 5.39, 2.31 × 0.22
- **13/14 (right tab):** tab sits top-**right** `idx="13"` 6.31, 0.03, 2.84 × 0.22; title/body stay at the normal full-width position (title 0.38, 0.38, 9.15 × 0.42|0.73 · body `idx="14"` 0.38, 0.85, 9.15 × 4.22 | 0.38, 1.17, 9.15 × 3.90). Use when the label should not push the title right.

### Left tab + 2 content (layouts 15–20) — sidebar + main

Green top-left tab, then **two content areas**: a narrow left column (2.5" wide — a product image, spec list, or nav-style rail) and a 6"-wide main area; the title sits over the main area (x 3.80). Variants add bottom teal tabs. This is the right family for "small thing on the left, big thing on the right" — not an image zone bolted onto a bullets slide.
- **15/16:** tab `idx="13"` 0.41, 0.04, 2.84 × 0.22 · left `idx="14"` 0.60, 0.78, 2.50 × 3.50 · title 3.80, 0.38, 6.00 × 0.42|0.73 · main `idx="15"` 3.80, 0.85, 6.00 × 4.22 | 3.80, 1.17, 6.00 × 3.90
- **17/18:** same slots renumbered — left `idx="15"`, main `idx="16"`, plus bottom-right tab `idx="17"` 7.12, 5.39, 2.31 × 0.22
- **19/20:** left `idx="16"`, main `idx="17"`, bottom tabs `idx="19"` 4.02, 5.39 and `idx="20"` 7.12, 5.39 (each 2.31 × 0.22)

### Product slide (layouts 23–24) — native full-height picture, right

White slide with a **picture placeholder filling the right column** (green triangle tucked behind its bottom corner). Made for a product/feature shot with text beside it — the image position is designed in; fill it.
- **23/24:** title 0.38, 0.38, 9.15 × 0.42|0.73 · body `idx="12"` 0.38, 0.85|1.17, 9.15 × 4.22|3.90 · **pic `idx="13"` 5.62, 0.38, 3.91 × 4.69**
- ⚠ The body placeholder is full-width and runs **under** the picture — keep body text inside x ≤ 5.4 (about 5.0" of usable width) or it disappears behind the image.

### Gray panel (layouts 25–26 "Sliced", 31–32 plain) — picture on a styled panel

The right ~40% of the slide is a **light-gray panel** (25/26 with an angled "sliced" top edge; 31/32 straight) with a full-height picture placeholder on it, green triangle bottom-right. Text column is properly narrowed to 5.12" — no under-image overlap here. Use for screenshots or images that deserve a framed presentation.
- **25/26:** title 0.38, 0.38, 5.12 × 0.42|0.73 · body `idx="12"` 0.38, 0.85|1.17, 5.12 × 4.22|3.90 · **pic `idx="13"` 5.62, 0.38, 3.91 × 4.66**
- **31/32:** same text geometry · **pic `idx="13"` 5.62, 0.38, 3.91 × 4.70|4.69**
- (Layout 26's template name is `4_Slided gray panel` — the "Slided" typo is in the potx itself; match it exactly when matching by name.)

### Gray panel + tab + icons (layouts 27–30) — image + caption + fixed icon chrome

Gray right panel with a green tab top-right, a **smaller picture placeholder** at the panel top, a **caption text placeholder** under it, and **three fixed decorative teal icons** (padlock, link, wi-fi) drawn on the panel's left edge as layout chrome. The icons are baked into the layout — they cannot be swapped per-slide, and they read as security/connectivity. Use only when that IoT flavor fits; there is **no true generic stat/icon-row layout** in this template — compose stat rows on a Generic slide (21/22) instead.
- **27/28:** tab `idx="13"` 6.31, 0.03, 2.84 × 0.22 · title 0.38, 0.38, 5.12 × 0.42|0.73 · body `idx="12"` 0.38, 0.85|1.17, 5.12 × 4.22|3.90 · **pic `idx="15"` 6.13, 0.79, 3.65 × 2.36** · caption `idx="14"` 6.12, 3.27, 3.65 × 2.27
- **29/30 ("deep tab"):** same, but the tab is a taller two-line green block `idx="16"` 6.34, 0.00, 2.84 × 0.55 (replaces `idx="13"`)

### Comparison table (layouts 33–34) — side-by-side / vs.

A silver tab top-right, title, and a full-width body whose first level is styled small and bold (11.5pt) — built as the backdrop for an inserted table. **Quirk, verified from renders: these two layouts have no green top bar** — that is the design, not a bug; don't hand-draw one. There is no native table placeholder; insert a `<a:tbl>` graphic frame at the body's geometry (brand it per `SKILL.md`: Ice-Blue alternating rows, Silver borders).
- **33 (1-line):** title 0.38, 0.38, 9.15 × 0.42 · body `idx="12"` 0.38, 0.85, 9.15 × 4.22 · tab `idx="13"` 6.50, 0.06, 2.83 × 0.21
- **34 (2-line):** title (inherited) 0.38, 0.38, 9.15 × 0.73 · body `idx="12"` 0.38, 1.17, 9.15 × 3.75 · tab `idx="13"` 6.50, 0.06, 2.83 × 0.21

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
