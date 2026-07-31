# Template-Edit Workflow (Preferred)

The bundled template (`${CLAUDE_PLUGIN_ROOT}/assets/digi-template.pptx`) has a proper PowerPoint slide master that automatically provides the green top bar, DIGI logo, and footer on every content slide. Editing this template is **significantly easier** than rebuilding the chrome from scratch with pptxgenjs.

## When to use this workflow

**Always.** Every Digi slide — a full deck, a closing slide, or a single one-off — is built by editing this template. There is no from-scratch path (see `SKILL.md` → Workflow Decision for why). The master carries the green bar, logo, footer, fonts, and the correct **10 × 5.625"** geometry; rebuilding any of that by hand is more work and never matches.

## The Workflow

### 1. Copy the template to a working location

```bash
cp ${CLAUDE_PLUGIN_ROOT}/assets/digi-template.pptx /home/claude/working-deck.pptx
```

### 2. Inspect what's in the template

```bash
extract-text /home/claude/working-deck.pptx
```

The template ships with:
- **Slide 1**: Title slide (with placeholder "Title" / "Sub-title" / "Name or Team" / "Month year")
- **Slide 2**: Generic content slide (mostly empty — your content goes here)
- **Slide 3**: Thank You / closing slide

### 3. Choose your edit approach

> **Locating the base `pptx` skill.** This workflow leans on the sibling `pptx` skill for the unpack/edit/repack scripts. Its path depends on the environment: in Claude Code CLI it's `~/.claude/skills/pptx/`, in Claude Desktop it's `/mnt/skills/public/pptx/`. Below, `<pptx>` means whichever applies. Invoke/read the `pptx` skill first.

For text-only edits and adding standard content slides, follow the workflow in `<pptx>/editing.md` — that's the canonical guide. Read it before doing structural edits.

The high-level pattern:
1. Unpack the .pptx → `python <pptx>/scripts/office/unpack.py working-deck.pptx unpacked/`
2. Duplicate slide2.xml as the basis for additional content slides
3. Edit slide XML to insert your content into the placeholders
4. Repack → `python <pptx>/scripts/office/pack.py unpacked/ output.pptx`

### 4. Standard QA

Follow the QA flow in `<pptx>/SKILL.md` — convert to images and verify:
- Content fits in placeholders
- Footer renders correctly
- Green top bar is present
- No overflow or cut-off text

## Important: Don't Touch the Slide Master

The slide master provides the green bar, logo, and footer chrome. Don't try to "improve" these — they're the brand standard. If you need a slide without the master decoration (rare), create a new slide that doesn't reference the master, but this is almost never what you want.

## Single one-off slide

When the ask is one content slide to drop into another deck, still start from the template, then trim:

1. Copy the template, unpack it (`unpack.py working-deck.pptx unpacked/`).
2. Edit the content slide (`ppt/slides/slide2.xml`) — see "Injecting styled content" below.
3. Trim the deck to that one slide by editing `ppt/presentation.xml`'s `<p:sldIdLst>` to keep only the content slide's `<p:sldId>` (the one whose `r:id` maps to `slides/slide2.xml` in `ppt/_rels/presentation.xml.rels`). Leaving the other slide parts on disk is harmless; PowerPoint shows only what's in `sldIdLst`.
4. Repack (`pack.py unpacked/ out.pptx`) and QA-render.

The recipient pastes the single slide into their deck and the master chrome travels with it.

## Injecting styled content (content slide geometry)

The content layout (`slideLayout30.xml`, used by `slide2.xml`) defines these placeholders, in inches on the 10 × 5.625" canvas:

| Placeholder | Offset (x, y) | Size (w, h) |
|-------------|---------------|-------------|
| Title (`type="title"`) | 0.38, 0.38 | 9.15 × 0.73 |
| Body (`type="body"` idx 12) | 0.38, 1.17 | 9.15 × 3.90 |
| Footer + slide number | bottom-left | (master chrome) |

So the usable content band is **x 0.38 → 9.53, y ≈ 0.30 → 5.07**, footer sits at y 5.44. Either fill the title/body placeholders, or add your own `<p:sp>` shapes inside `<p:spTree>` (insert before `</p:spTree>`) with explicit geometry in EMU (`inches × 914400`). Custom shapes don't inherit fonts, so set them explicitly: `Source Sans Pro` for text, `Consolas` for code/prompts, and brand colors from the `SKILL.md` palette (Navy `1B4965`, Green `91D46C`, Dark Gray `3F4245`, Ice Blue `E2F6FF` for callout fills, Silver `DAD8D8` for borders). A reusable Python shape-emitter (off/ext in EMU, `solidFill`, runs with `<a:latin typeface=...>`) is the fastest way to lay out cards, eyebrows, and callouts — keep it in the working dir, not the skill.

QA every slide by converting to PDF then PNG (`soffice.py --headless --convert-to pdf` → `pdftoppm -png`) and visually inspecting before declaring done.

## Title and Closing Slides

The title slide includes:
- Full-bleed urban skyline photo
- Dark gradient overlay
- Binary/network wave motif at top
- Title in Digi Green, subtitle in white, byline in teal
- Solid green parallelogram bottom-right

If you're keeping these slides, just edit the placeholder text. If you're swapping the imagery, replace the picture in slide1.xml's `<p:pic>` element — see the standard pptx editing guide for details.
