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

Each master ships with 34 layouts and two starter slides:
- **Slide 1**: Title slide (layout "1_Generic Deck Title" — placeholder title, name/date)
- **Slide 2**: Content slide (layout "1_Bullets (1-line head)" — header + bullet body; your content goes here)

There is no bundled Thank You slide; build a closing slide from the title layout if the deck needs one.

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

The slide master provides the green bar, logo, and classification-footer chrome. Don't try to "improve" these — they're the brand standard. The footer in particular is **never retyped**: if it shows the wrong classification, switch to the other master. If you need a slide without the master decoration (rare), create a new slide that doesn't reference the master, but this is almost never what you want.

## Single one-off slide

When the ask is one content slide to drop into another deck, still start from the classification-correct master, then trim:

1. Copy the master, unpack it (`unpack.py working-deck.pptx unpacked/`).
2. Edit the content slide (`ppt/slides/slide2.xml`) — see "Injecting styled content" below.
3. Trim the deck to that one slide by editing `ppt/presentation.xml`'s `<p:sldIdLst>` to keep only the content slide's `<p:sldId>` (the one whose `r:id` maps to `slides/slide2.xml` in `ppt/_rels/presentation.xml.rels`). Leaving the other slide parts on disk is harmless; PowerPoint shows only what's in `sldIdLst`.
4. Repack (`pack.py unpacked/ out.pptx`) and QA-render.

The recipient pastes the single slide into their deck and the master chrome travels with it.

## Injecting styled content (content slide geometry)

The content layout (`slideLayout3.xml`, "1_Bullets (1-line head)", used by `slide2.xml` — identical geometry in both masters) defines these placeholders, in inches on the 10 × 5.625" canvas:

| Placeholder | Offset (x, y) | Size (w, h) |
|-------------|---------------|-------------|
| Title (`type="title"`) | 0.38, 0.38 | 9.15 × 0.42 |
| Body (`type="body"`) | 0.38, 0.85 | 9.15 × 4.22 |
| Slide number + classification footer | bottom-left, y 5.44 | (layout chrome) |

So the usable content band is **x 0.38 → 9.53, y 0.38 → 5.07**, footer sits at y 5.44. Either fill the title/body placeholders, or add your own `<p:sp>` shapes inside `<p:spTree>` (insert before `</p:spTree>`) with explicit geometry in EMU (`inches × 914400`). Custom shapes don't inherit fonts, so set them explicitly: `Source Sans Pro` for text, `Consolas` for code/prompts, and brand colors from the `SKILL.md` palette (Navy `1B4965`, Green `91D46C`, Dark Gray `3F4245`, Ice Blue `E2F6FF` for callout fills, Silver `DAD8D8` for borders). A reusable Python shape-emitter (off/ext in EMU, `solidFill`, runs with `<a:latin typeface=...>`) is the fastest way to lay out cards, eyebrows, and callouts — keep it in the working dir, not the skill.

QA every slide by converting to PDF then PNG (`soffice.py --headless --convert-to pdf` → `pdftoppm -png`) and visually inspecting before declaring done.

## Title and Closing Slides

The title slide (layout "1_Generic Deck Title") includes:
- Light gray diagonal panel over white — no photo, no gradient
- DIGI logo top-left
- Title placeholder (navy/dark from the theme), name/date placeholder below in Medium Gray
- Layered green triangle motif bottom-right (layout chrome)

Just edit the placeholder text — all decoration is layout chrome and stays untouched. There is no bundled Thank You slide; reuse the title layout for a closing slide.
