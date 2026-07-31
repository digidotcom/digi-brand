# Building from Scratch with pptxgenjs — DEPRECATED

> **Do not follow this workflow.** The from-scratch path was removed from this skill (see `SKILL.md` → Workflow Decision). It produced slides with no slide master (missing green bar / logo / footer) on the wrong 13.33 × 7.5" geometry instead of the template's true 10 × 5.625", so output never matched a real Digi slide and always needed manual reformatting. **Always edit the template** (`references/template-workflow.md`), including for single one-off slides.
>
> This file is retained only for the **chart-color constants and palette** below, which remain correct. Ignore the build steps.

For the general pptxgenjs workflow, see the base `pptx` skill's `pptxgenjs.md` (in Claude Code CLI: `~/.claude/skills/pptx/`; in Claude Desktop: `/mnt/skills/public/pptx/`). This doc covers the Digi-specific patterns.

## Setup

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

// Use widescreen 13.33 x 7.5 to match the template
pres.defineLayout({ name: "WIDE", width: 13.33, height: 7.5 });
pres.layout = "WIDE";

// Digi brand color constants
const DIGI_GREEN     = "91D46C";
const DIGI_NAVY      = "1B4965";  // Note: 5, not 4
const DIGI_DARK_GRAY = "3F4245";
const DIGI_TEAL      = "1F7FA5";
const DIGI_ORANGE    = "CC6033";
const DIGI_ICE_BLUE  = "E2F6FF";
const DIGI_MED_GRAY  = "56565A";
const DIGI_SILVER    = "DAD8D8";
const WHITE          = "FFFFFF";
```

## Content Slide Skeleton

Every Digi content slide needs three things: white background, thin green top bar, bottom-left footer with logo.

```javascript
const slide = pres.addSlide();
slide.background = { color: WHITE };

// 1. Top green bar (full width, ~0.1" tall)
slide.addShape("rect", {
  x: 0, y: 0, w: 13.33, h: 0.1,
  fill: { color: DIGI_GREEN },
  line: { color: DIGI_GREEN, width: 0 }
});

// 2. Your content goes here (between y=0.4 and y=6.9)

// 3. Footer at bottom-left
// If you have a DIGI logo PNG, add it at x=0.4, y=7.05, h=0.3
slide.addText([
  { text: "2", options: { bold: true, color: DIGI_DARK_GRAY } },
  { text: "  |  CONFIDENTIAL  |  © DIGI INTERNATIONAL INC.", options: { color: DIGI_MED_GRAY } }
], {
  x: 1.2, y: 7.1, w: 9.0, h: 0.25,
  fontFace: "Source Sans Pro", fontSize: 9,
  align: "left", valign: "middle"
});
```

## Layout Patterns

### Two-column (text + visual)

```javascript
// Title
slide.addText("Your Slide Title", {
  x: 0.5, y: 0.5, w: 12.3, h: 0.9,
  fontFace: "Source Sans Pro", fontSize: 36, bold: true,
  color: DIGI_NAVY
});

// Left column (text)
slide.addText("...", {
  x: 0.5, y: 1.7, w: 6.0, h: 5.0,
  fontFace: "Source Sans Pro", fontSize: 14,
  color: DIGI_DARK_GRAY
});

// Right column (visual / callout)
slide.addShape("rect", {
  x: 7.0, y: 1.7, w: 5.8, h: 5.0,
  fill: { color: DIGI_NAVY }
});
```

### Section labels (small green tab)

```javascript
slide.addShape("rect", {
  x: 0.5, y: 0.4, w: 2.5, h: 0.4,
  fill: { color: DIGI_GREEN }
});
slide.addText("SECTION LABEL", {
  x: 0.5, y: 0.4, w: 2.5, h: 0.4,
  fontFace: "Source Sans Pro", fontSize: 12, bold: true,
  color: DIGI_NAVY, align: "center", valign: "middle",
  charSpacing: 3
});
```

### Tables

- **Header row**: Teal (#1F7FA5), white text, bold
- **Alt rows**: Ice Blue (#E2F6FF) for striping
- **Borders**: Silver (#DAD8D8) thin

```javascript
slide.addTable(rows, {
  x: 0.5, y: 1.7, w: 12.3,
  fontFace: "Source Sans Pro", fontSize: 12,
  colW: [3, 3, 3, 3.3],
  border: { type: "solid", pt: 0.5, color: DIGI_SILVER }
});
```

### Charts

```javascript
const digiChartColors = ["91D46C", "1F7FA5", "1B4965", "CC6033", "00B7FF", "56565A"];

slide.addChart("bar", chartData, {
  x: 0.5, y: 1.7, w: 12.3, h: 5.0,
  chartColors: digiChartColors,
  catAxisLabelFontFace: "Source Sans Pro",
  valAxisLabelFontFace: "Source Sans Pro",
  showLegend: true,
  legendFontFace: "Source Sans Pro"
});
```

## Hard Don'ts

- ❌ **Don't add triangles or diagonal accents on content slides.** Save them for title/closing.
- ❌ **Don't use #F5F7F7 as the slide background.** White only.
- ❌ **Don't try to recreate the title-slide binary-wave motif from scratch.** Use the template if you need a title slide.
- ❌ **Don't put accent lines under titles** — whitespace is enough.
- ❌ **Don't add full-width colored ribbons or stripes** unless they're the official thin green top bar.

## QA

Follow the standard pptx QA in the base `pptx` skill's `SKILL.md` (CLI: `~/.claude/skills/pptx/`; Desktop: `/mnt/skills/public/pptx/`) — render to images, visual inspection, fix overflows, then stop. Don't iterate forever on sub-pixel positioning.
