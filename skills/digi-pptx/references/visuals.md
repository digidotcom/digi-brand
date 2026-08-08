# Visuals — screenshots, placeholders, and generated graphics

A slide that is a wall of text is a failed slide. Every content slide should
earn its space with **one** visual element where it helps — a screenshot, a
placeholder for one, or a generated graphic — not five bullets and white space.
This file is the how. Brand colors, type sizes, and the content-band geometry
are in `SKILL.md` and `template-workflow.md`; don't restate them, use them.

## The decision: screenshot vs placeholder vs generate vs text

Pick per slide. The wrong move is reflexively doing the same thing every time —
a deck of generated clip-art is as bad as a deck of bullets.

| The content is… | Do this |
|---|---|
| A real UI, dashboard, report, or live data | **Screenshot placeholder** — leave a labeled box for the real screen; the deck author fills it in later. Don't fake a UI with a generated image. |
| A concept: architecture, data flow, how-it-works, a relationship, a before/after | **Generate an illustration** (`gen_graphic.py`, default `illustration` style) — there's nothing to screenshot, and a diagram beats prose. |
| A real-world scene a photo would carry: a technician on site, an ops floor, a person using the product | **Generate a photo** (`gen_graphic.py --style photo`) — when a depicted scene lands better than a diagram. |
| A genuinely short list (≤3 items) or a quote/number that IS the point | **Keep it as text** — but make it big and give it room. Not everything needs a picture. |
| A long list (>4 bullets) | **Split the slide or restructure** — never shrink type to fit. A visual on a second slide usually beats a crowded one. |

## Style presets (`--style`)

`gen_graphic.py` has three style presets. **`illustration` (soft 3D) is the
house look**, settled on 2026-06-25 after comparing rendered samples — an
earlier flat line-art default was rejected on sight. Lesson baked in: **never
lock a visual style from a description; generate a small spread and pick from
the pixels**, not from a worded menu.

| `--style` | Look | Use for |
|---|---|---|
| `illustration` (default) | Soft 3D render, rounded forms, gentle gradients, brand palette on white | Concepts, diagrams, the default for generated graphics |
| `photo` | Realistic editorial photograph, natural light, cool brand-adjacent tones | A slide that wants a depicted real-world scene |
| `lineart` | Flat 2D iconographic line-art | When a deck specifically wants minimal line icons |

When NOT to generate: don't generate a graphic to decorate a slide that's
already clear, and don't generate a fake screenshot, chart, or logo. Generated
images are for *concepts*, and they carry a C2PA/SynthID "AI-generated"
provenance watermark (fine internally — just know it's there).

## Image zones

**Zones are for layouts with no picture placeholder** (bullets 3, tab-labelled
7/13, generic 21). If the slide's layout has a native picture placeholder —
product slide **23**, gray panel **31** — fill THAT at its own geometry instead
(`5.62, 0.38, 3.91 × 4.69`; inventory in `template-workflow.md`); the design
already placed the image, and a zone on top of it fights the layout.

The **Photo Deck Title (35)** is a separate case again: its photograph is a
slide *background*, applied with `scripts/set_title_photo.py`. Never place a
title photo as a picture or a zone — slide shapes draw above the layout's scrim
and chrome and hide the whole design.

Geometry in inches on the 10 × 5.625" canvas. Every zone sits below the title
(title band ends 0.80"; body starts 0.85") and above the footer (5.44"). `place_image.py --zone <name>`
knows these; `gen_graphic.py --zone <name>` generates at the matching aspect so
the image fills the box with no distortion or letterbox.

| Zone | x, y | w, h | Aspect | Use |
|---|---|---|---|---|
| `left-half` | 0.38, 1.30 | 4.30, 3.45 | 4:3 | Image left, text right |
| `right-half` | 5.15, 1.30 | 4.30, 3.45 | 4:3 | Image right, text left |
| `hero` | 1.50, 1.15 | 7.00, 3.94 | 16:9 | One centered visual, little/no text |
| `full-band` | 0.38, 1.15 | 9.15, 3.92 | 21:9 | Wide band under the title |
| `square` | 3.25, 1.30 | 3.50, 3.50 | 1:1 | A single centered icon/diagram |

**There is no default zone. Pick from the image, not from habit.** The table is
not ranked, and an image on the right is not the house style — a deck where
every visual sits in the same box reads as one slide repeated. Choose by what
the visual actually is:

- **Wide or landscape** (dashboards, topology diagrams, timelines, wide tables)
  → `full-band`. Squeezing these into a half kills the detail.
- **Tall or portrait** (a phone screen, a stacked list, a single UI panel)
  → `left-half` or `right-half`.
- **The slide's whole point, with little text** → `hero`.
- **A single icon or small diagram** → `square`.
- **Anything else** → `left-half` and `right-half` are equally correct; alternate
  them across consecutive slides so a run of half-image slides has rhythm
  instead of a fixed gutter.

For anything off-grid, pass explicit `--x --y --w --h` (inches) instead of `--zone`.

## Generate a graphic — `scripts/gen_graphic.py`

```bash
python scripts/gen_graphic.py \
  --prompt "an edge router at a remote site sending telemetry up to a cloud, a laptop reaching securely back down" \
  --out work/graphic.png --zone left-half           # default --style illustration

python scripts/gen_graphic.py --style photo \
  --prompt "a field technician at a remote cell-tower site using a laptop" \
  --out work/scene.png --zone hero
```

- Model: `gemini-3.1-flash-image-preview` (Nano Banana 2), roughly 6.5 cents
  per image.
- The **`--prompt` is a subject, not a style** — describe *what* to draw. The
  script prepends the `--style` preset's preamble (palette, finish, **no text
  inside the image**); that preamble is what makes a deck's graphics look like
  one family. Don't add your own style words; they fight the preset. Pick the
  look with `--style` (see table above), not by editing the prompt. `--raw`
  bypasses all presets (rare).
- Key comes from `$GEMINI_API_KEY`, else a `.env` in the working directory
  (override `--env-file`).
- The model picks the format (usually JPEG); the script writes the extension to
  match the real bytes, so the output drops straight into `place_image.py`.
- **Prompt for the picture, let the slide carry the words.** Don't ask the model
  to render labels — it garbles text. Add callouts as PowerPoint text shapes on
  top if needed.

Good prompts are concrete and name the relationship: "three IoT sensors feeding
one gateway, gateway feeding a cloud" beats "IoT diagram." If the first image
misses, regenerate (it's cheap) or sharpen the subject — don't fight it with
style adjectives.

## Place an image — `scripts/place_image.py`

Run on an **unpacked** template dir (after `unpack.py`, before `pack.py`).
Handles all four fiddly steps: copy into `ppt/media`, register the content-type,
add the relationship, inject the `<p:pic>`.

```bash
# generated graphic — made at the zone's aspect, so it fills the box exactly:
python scripts/place_image.py --unpacked unpacked/ --slide 2 --image work/graphic.jpg --zone left-half

# a real screenshot whose aspect differs — --fit preserves aspect, centers it:
python scripts/place_image.py --unpacked unpacked/ --slide 4 --image work/shot.png --zone full-band --fit
```

Use `--fit` for real screenshots (so they aren't stretched). Generated graphics
match the zone aspect already, so they don't need it.

## Screenshot placeholder (filled in later)

A placeholder is just a styled rectangle with a centered label — the same custom
`<p:sp>` mechanic as any other shape (see `template-workflow.md` → "Injecting
styled content"). The brand recipe: **Ice-Blue `E2F6FF` fill, Silver `DAD8D8`
dashed border, centered italic Medium-Gray `56565A` label** naming exactly what
goes there.

```xml
<p:sp><p:nvSpPr><p:cNvPr id="103" name="ScreenshotPlaceholder"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="347472" y="1188720"/><a:ext cx="8366760" cy="3291840"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="E2F6FF"/></a:solidFill>
<a:ln w="19050"><a:solidFill><a:srgbClr val="DAD8D8"/></a:solidFill><a:prstDash val="dash"/></a:ln></p:spPr>
<p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle/>
<a:p><a:pPr algn="ctr"><a:buNone/></a:pPr><a:r>
<a:rPr lang="en-US" sz="1400" i="1"><a:solidFill><a:srgbClr val="56565A"/></a:solidFill>
<a:latin typeface="Source Sans Pro"/></a:rPr>
<a:t>[ Screenshot: DRM device dashboard — live device list + health ]</a:t></a:r></a:p></p:txBody></p:sp>
```

EMU = inches × 914400. The label is load-bearing: say **what** screenshot and
**what it should show**, so the deck author (or a reviewer) knows exactly what to drop in.
Size the box to a zone from the table above.

## QA additions for visual slides

On top of the standard `SKILL.md` QA checklist, after the PDF→PNG render verify:

- [ ] Generated graphics match the chosen `--style` preset (illustration,
      photo, or lineart — see Style presets above), stay in the Digi palette,
      and contain **no rendered text**.
- [ ] Images sit inside the content band — clear of the title and the footer,
      not overlapping the green bar.
- [ ] Real screenshots placed with `--fit` aren't stretched.
- [ ] Every placeholder box has a specific label (what + what it shows).
- [ ] No slide is still a wall of text where a visual was the right call.
