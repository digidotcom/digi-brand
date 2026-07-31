---
name: digi-pptx
description: Create Digi International branded PowerPoint presentations. Applies Digi's official 2024 brand — pure white content slides with a thin green top bar and bottom-left logo footer, Source Sans Pro typography, and the official color palette (Green #91D46C, Navy #1B4965, Teal #1F7FA5, Orange #CC6033). Slides earn their space with visuals, not walls of text: drop labeled screenshot placeholders where real UI belongs, and generate on-brand graphics in the chosen style preset (via Nano Banana 2 / Gemini) for concepts where no screenshot exists. Includes reusable blueprints for the recurring launch-training genre (support, channel, and sales enablement decks) so that structure is followed, not reinvented. Use whenever creating slides, decks, pitch materials, internal presentations, sales enablement, training decks, or any .pptx output for Digi. Trigger on phrases like "build a slide", "make a deck", "presentation for", "Digi slide", "AI tip of the week slide", "support/channel/sales training deck", "add a graphic/diagram to this slide", "this slide is too text-heavy", or when working with .pptx files in a Digi context.
license: MIT
---

> **Brand values.** Read
> `${CLAUDE_PLUGIN_ROOT}/skills/digi-brand-guidelines/SKILL.md` for the palette,
> type stack, and accessibility rules. If it is not readable, use this fallback:
> navy `#1B4965`, white `#FFFFFF`, dark gray `#3F4245`, light gray `#F5F7F7`,
> green `#91D46C` (fills only, never text), silver `#DAD8D8`, teal `#1F7FA5`,
> orange `#CC6033`, ice blue `#E2F6FF`, medium gray `#56565A`, followed-link
> blue `#00B7FF`. Fonts: Source Sans Pro, falling back to Source Sans 3 or Arial.
>
> **Template location.** The official template is at
> `${CLAUDE_PLUGIN_ROOT}/assets/digi-template.pptx`.

# Digi International PowerPoint Skill

Creates on-brand Digi presentations. **Always edit the bundled official template.** Its slide master provides the green top bar, DIGI logo, footer, brand fonts, and the correct 10 × 5.625" slide geometry for free. This is the only supported path, including for single one-off slides.

---

## Workflow Decision

There is one path: **edit the template.** See [references/template-workflow.md](references/template-workflow.md).

**Why there is no "build from scratch" option.** Building a deck from a blank pptxgenjs canvas was previously offered for one-off slides. It was removed because the output never matched a real Digi slide and always needed manual reformatting into the template afterward. Two reasons it can't match:
- A blank pptxgenjs deck has **no slide master**, so the green bar, logo, and footer are absent (or hand-drawn inconsistently).
- The slide master's true geometry is **10 × 5.625"**, not the 13.33 × 7.5" a from-scratch build defaults to, so every coordinate is off.

The template gives all of that for free. Editing it is strictly less work than rebuilding the chrome and getting it wrong.

**Single one-off slide?** Still use the template — edit the content slide and trim the deck to that one slide. The recipe is in [references/template-workflow.md](references/template-workflow.md) ("Single one-off slide").

---

## Building a launch training deck, or a customer-facing pitch? Start from a blueprint

For any recurring Digi deck genre, don't invent the structure — follow the proven archetype in **[references/deck-blueprints/](references/deck-blueprints/README.md)**, which has a find-yours-by-role table up top. Each blueprint gives the ordered slide sequence, what each slide does, the per-audience voice, and which visual fits each slide.

Pick the family by audience first. **internal/** is for Digi people (or partner reps) who have to act on it: launch enablement (`internal/support-enablement.md`, `internal/channel-enablement.md`, `internal/sales-enablement.md`), decisions and funding (`internal/leadership-review.md`, `internal/business-case.md`), and company or team alignment (`internal/all-hands.md`, `internal/project-kickoff.md`). **customer-facing/** is for people outside Digi: `customer-facing/sales-pitch.md` for a prospect, `customer-facing/customer-qbr.md` for a customer you already have, `customer-facing/webinar.md` for a webinar or conference session. Swap in your own subject; keep the moves.

---

## Visuals — every slide earns its space (no walls of text)

A content slide that is just a title and bullets is a weak slide. Before filling one with text, decide what visual carries it. Full mechanics, zones, and scripts are in **[references/visuals.md](references/visuals.md)** — read it whenever a slide needs more than text. The rule in one table:

| The content is… | Do this |
|---|---|
| Real UI, a dashboard, a report, live data | **Screenshot placeholder** — a labeled Ice-Blue dashed box you fill in with the real screen. Never fake a UI with a generated image. |
| A concept: architecture, data flow, how-it-works, a relationship | **Generate an illustration** — `scripts/gen_graphic.py` (default `--style illustration`, soft 3D) makes an on-brand image (Nano Banana 2). There's nothing to screenshot, and a diagram beats prose. |
| A real-world scene a photo would carry | **Generate a photo** — `scripts/gen_graphic.py --style photo`. When a depicted scene lands better than a diagram. |
| A short list (≤3) or a number/quote that IS the point | **Keep as text** — but large, with room. Not everything needs a picture. |
| A long list (>4 bullets) | **Split or restructure** — never shrink type to fit. |

Two bundled scripts do the heavy lifting (details + zone geometry in `references/visuals.md`):
- `scripts/gen_graphic.py` — generate a Digi-styled graphic. The prompt is a **subject**; `--style` picks the look (`illustration` = soft 3D, the default house style; `photo` = real scene; `lineart` = flat icons), always with **no text in the image**, so graphics look like one family. Generation costs roughly 6.5 cents per image, and output carries a C2PA/SynthID "AI-generated" watermark. (Style is chosen from rendered samples, not a description — see `references/visuals.md`.)
- `scripts/place_image.py` — drop any image (generated or a real screenshot) into an unpacked slide at a named zone (`right-half`, `left-half`, `hero`, `full-band`, `square`) or explicit geometry. Handles media + content-type + relationship + `<p:pic>`. Use `--fit` for real screenshots so they aren't stretched.

**Don't generate to decorate, and don't generate fakes** (no fake screenshots, charts, or logos). Generated images are for concepts only.

---

## Official Brand Colors (2024 Theme)

These are pulled directly from the official template's theme XML. Use them exactly.

| Role | Name | Hex | Use |
|------|------|-----|-----|
| Primary | Digi Green | `#91D46C` | Top bar, accents, bullets, CTAs, headline color on dark backgrounds |
| Dark | Dark Navy | `#1B4965` | Title slide overlays, headline color on light backgrounds, dark callout boxes |
| Body | Dark Gray | `#3F4245` | Body text, headings on light backgrounds |
| Background | White | `#FFFFFF` | **Default content slide background** |
| Accent | Teal Blue | `#1F7FA5` | Section labels, secondary headlines, links |
| Warning | Orange | `#CC6033` | NDA badges, warnings, "attack" content in battlecards |
| Highlight | Ice Blue | `#E2F6FF` | Alt table rows, callout backgrounds |
| Muted | Medium Gray | `#56565A` | Footer text, captions, secondary copy |
| Divider | Silver | `#DAD8D8` | Borders, dividers |
| Link | Bright Blue | `#00B7FF` | Followed links |

### For pptxgenjs charts (no `#` prefix):
```javascript
const digiChartColors = ["91D46C", "1F7FA5", "1B4965", "CC6033", "00B7FF", "56565A"];
```

---

## Typography

- **Primary**: Source Sans Pro
- **Fallback**: Source Sans 3 (Google Fonts), then Arial
- **Headings**: Source Sans Pro Bold or Semibold
- **Body**: Source Sans Pro Regular
- **Monospace (for code/prompts)**: Consolas

### Type sizes
| Element | Size |
|---------|------|
| Slide title | 36–44pt bold |
| Section header | 18–22pt bold |
| Body | 14–16pt |
| Captions/footer | 8–10pt |

---

## Slide Anatomy (Content Slide — the most common)

```
┌─────────────────────────────────────────────────────┐
│ ████████████████ THIN GREEN BAR ███████████████████ │  ← Green #91D46C, ~0.1" tall
│                                                     │
│                                                     │
│            WHITE BACKGROUND (#FFFFFF)               │
│                                                     │
│            Title in #1B4965 or #3F4245              │
│                                                     │
│            Body content goes here.                  │
│            NO triangles. NO ribbons. Just space.    │
│                                                     │
│                                                     │
│ ▌DIGI▌                                              │
│  logo   2  |  CONFIDENTIAL  |  © DIGI INTERNATIONAL │  ← Bottom-left
└─────────────────────────────────────────────────────┘
```

**Critical rules:**
- **Background is white.** Not light gray.
- **No diagonal triangles or ribbons on content slides.** They appear only on title/closing slides.
- **Top green bar runs the full width** at the very top edge (~0.1" tall).
- **DIGI logo sits bottom-left**, with footer text immediately to its right.
- **Footer format**: `{slideNum}  |  CONFIDENTIAL  |  © DIGI INTERNATIONAL INC.` — page number bold, separators are pipes with double-space padding.

---

## Slide Anatomy (Title & Closing Slides)

Title and "Thank You" slides use a more dramatic treatment:

- **Full-bleed photo background** (urban skyline or industry-relevant imagery)
- **Dark gradient overlay** on the left ~60% of the slide for text legibility
- **White DIGI logo** top-left
- **Title** in Digi Green (#91D46C), large (60pt+)
- **Subtitle** in white bold
- **Name/team/date** in Teal (#1F7FA5)
- **Bottom-right**: solid green parallelogram/diagonal cut (NOT layered triangles — it's one clean angled shape)
- **Optional top motif**: flowing wave of green and teal binary digits ("0"s and "1"s) — the Digi "data flow" signature

This is hard to build from scratch with pptxgenjs. **Use the template.**

---

## What NOT to Do (Common Mistakes)

These are mistakes a prior version of this skill made — don't repeat them:

- ❌ **Don't use light gray (#F5F7F7) as a slide background.** Content slides are white.
- ❌ **Don't add triangles or diagonal accents to content slides.** Save them for title/closing.
- ❌ **Don't stack "layered triangles."** The actual brand mark is a single solid green parallelogram on title slides only.
- ❌ **Don't manually draw the green top bar and logo if you can use the template** — the slide master does it automatically and consistently.
- ❌ **Don't default to the older navy ending in 64.** It's `#1B4965`.
- ❌ **Don't use Arial or Calibri as the primary font.** It's Source Sans Pro.
- ❌ **Don't fill the slide with decoration.** Digi's actual brand is restrained — most of the slide is whitespace for content.

---

## Quick Reference: Adding Content to a Slide

Unpack the template, inject brand-styled shapes into the content slide (`slide2.xml`), repack. Full mechanics — placeholder geometry, the shape-injection helper, trimming to one slide, and the PDF/PNG QA render — are in [references/template-workflow.md](references/template-workflow.md). Brand colors and type sizes are in the tables above; use them verbatim.

---

## Reference Files

- `${CLAUDE_PLUGIN_ROOT}/assets/digi-template.pptx` — Official Digi brand template. **Start here for every slide, one or many.**
- `references/template-workflow.md` — How to edit the bundled template (unpack/edit/repack), including the single one-off slide recipe
- `references/visuals.md` — Screenshots, placeholders, and generated graphics: the decision rule, image zones, and the two scripts. Read when a slide needs more than text.
- `references/deck-blueprints/` — Blueprints for the decks Digi ships across every function: `internal/` (launch enablement, leadership review, business case, all-hands, project kickoff) and `customer-facing/` (sales pitch, customer QBR, webinar/conference). Slide archetypes + voice + visuals per audience. Start at its README for the find-yours-by-role table.
- `scripts/gen_graphic.py` — Generate an on-brand Digi graphic (Nano Banana 2 / Gemini). `--prompt <subject> --out <file> --zone <name>`.
- `scripts/place_image.py` — Place an image into an unpacked slide at a named zone or explicit geometry.
- `references/from-scratch.md` — **DEPRECATED.** Retained only for the chart-color and palette constants; do not follow its build workflow. The from-scratch path was removed (see Workflow Decision).

---

## QA Checklist

Before declaring a slide done, verify:

- [ ] Background is white (not light gray)
- [ ] Green top bar is present and full-width
- [ ] No triangles on content slides
- [ ] Footer follows the `{#}  |  CONFIDENTIAL  |  © DIGI INTERNATIONAL INC.` format
- [ ] DIGI logo is bottom-left (or the master is providing it)
- [ ] Source Sans Pro everywhere except code blocks (Consolas)
- [ ] Navy is `#1B4965` — check the last digit, the older value ended in 64
- [ ] No text overflow — run `extract-text` and visual QA per the pptx skill's standard QA flow
- [ ] No slide is a wall of text where a visual was the right call (see Visuals)
- [ ] Generated graphics match the chosen `--style` preset and stay in the Digi palette, with no rendered text; images sit inside the content band, clear of the green bar and footer; real screenshots placed with `--fit` aren't stretched; every placeholder box has a specific label
