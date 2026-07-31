#!/usr/bin/env python3
"""
gen_graphic.py — Generate an on-brand Digi graphic with Nano Banana 2.

Why this exists: a slide that is a wall of text is a bad slide, but most
concepts (architecture, flow, relationship, "how it works") have no real
screenshot to show. This generates an on-brand Digi-palette graphic, in the
selected style preset, for exactly those cases — so the deck has a picture
instead of another bullet list, without anyone hand-drawing it.

Model: gemini-3.1-flash-image-preview ("Nano Banana 2" = Gemini 3.1 Flash Image),
called over the stable :generateContent REST endpoint. Costs roughly 6.5
cents per image.
Output carries Google's C2PA / SynthID provenance watermark (marked as
AI-generated) — fine for internal/sales decks; know it's there.

Key: read from $GEMINI_API_KEY, else parsed from a .env in the working
directory (override with --env-file).

Usage:
  python gen_graphic.py --prompt "an edge router sending data up to a cloud" \
      --out graphic.png --aspect 4:3

  # zone shorthand picks the aspect ratio that fills that slide zone cleanly:
  python gen_graphic.py --prompt "..." --out g.png --zone full-band

The locked style preamble is the whole point — it locks the graphic to the
selected preset's look in the Digi palette so graphics look like one brand
family, not random AI clip-art. Pass --raw to send your prompt verbatim with
no preamble (rare).
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = "gemini-3.1-flash-image-preview"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Style presets. The preamble is the whole lever — it makes a deck's graphics
# look like one family. "No text in the image" is in every preset on purpose:
# AI-rendered text is garbled, and the SLIDE supplies the words.
#   illustration (DEFAULT) — house pick (2026-06-25): soft 3D render, the
#                            default look for concept/diagram graphics.
#   photo                  — a realistic depicted scene, for slides that want a
#                            photograph (a technician on site, an ops floor) and
#                            where a diagram would be wrong. Real scene, so the
#                            brand-hex lock relaxes to brand-adjacent tones.
#   lineart                — the original flat iconographic look; kept as an option.
NO_TEXT = ("Do NOT render any words, letters, labels, numbers, logos, or "
           "watermarks inside the image.")
STYLES = {
    "illustration": (
        "Soft 3D rendered illustration, rounded friendly forms, gentle gradients "
        "and soft drop shadows, polished modern tech look, clean composition on a "
        "pure white background. Digi International palette: green #91D46C, navy "
        "#1B4965, teal #1F7FA5, with ice-blue #E2F6FF accents. " + NO_TEXT + " Subject: "
    ),
    "photo": (
        "Professional editorial photograph, realistic scene, natural soft lighting, "
        "shallow depth of field, clean modern corporate look, cool blue and green "
        "tones where natural. " + NO_TEXT + " Subject: "
    ),
    "lineart": (
        "Flat 2D vector line-art illustration, minimal and clean, on a pure white "
        "background (#FFFFFF). Use ONLY the Digi palette: green #91D46C, navy "
        "#1B4965, teal #1F7FA5, dark-gray #3F4245 linework; orange #CC6033 sparingly. "
        "Thin consistent strokes, no gradients, no 3D, no photorealism. " + NO_TEXT
        + " Generous whitespace, iconographic. Subject: "
    ),
}
DEFAULT_STYLE = "illustration"

# Slide zones (see references/visuals.md) → the aspect ratio that fills them
# without distortion, so a generated image drops straight into place_image.py.
ZONE_ASPECT = {
    "right-half": "4:3",
    "left-half": "4:3",
    "full-band": "21:9",
    "hero": "16:9",
    "square": "1:1",
}
# Gemini-accepted aspect ratios (reject typos early rather than get a silent default).
VALID_ASPECTS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}


def load_key(env_file):
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    path = os.path.expanduser(env_file)
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(
        "ERROR: no GEMINI_API_KEY in environment and none found in "
        f"{env_file}. Export it or pass --env-file."
    )


def generate(prompt, aspect, key):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"imageConfig": {"aspectRatio": aspect}},
    }
    req = urllib.request.Request(
        ENDPOINT.format(model=MODEL),
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"ERROR: Gemini API HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: could not reach Gemini API: {e.reason}")

    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob and blob.get("data"):
            return base64.b64decode(blob["data"]), blob.get("mimeType", "image/jpeg")
    # No image came back — surface text/finishReason so the failure is legible.
    sys.exit("ERROR: no image in response:\n" + json.dumps(data, indent=2)[:1500])


def main():
    ap = argparse.ArgumentParser(description="Generate an on-brand Digi graphic (Nano Banana 2).")
    ap.add_argument("--prompt", required=True, help="What to draw (a subject, not a style).")
    ap.add_argument("--out", required=True, help="Output image path (.png or .jpg).")
    ap.add_argument("--aspect", help="Aspect ratio, e.g. 4:3, 16:9, 21:9. Overrides --zone.")
    ap.add_argument("--zone", choices=sorted(ZONE_ASPECT), help="Slide zone → its natural aspect.")
    ap.add_argument("--style", choices=sorted(STYLES), default=DEFAULT_STYLE,
                    help=f"Visual style preset (default: {DEFAULT_STYLE}). "
                         "illustration=soft 3D house look; photo=realistic scene; lineart=flat icons.")
    ap.add_argument("--raw", action="store_true", help="Send prompt verbatim, skip all style presets.")
    ap.add_argument("--env-file", default=".env", help="Where to read GEMINI_API_KEY if unset.")
    args = ap.parse_args()

    aspect = args.aspect or (ZONE_ASPECT[args.zone] if args.zone else "4:3")
    if aspect not in VALID_ASPECTS:
        sys.exit(f"ERROR: aspect {aspect!r} not supported. Pick one of: {sorted(VALID_ASPECTS)}")

    prompt = args.prompt if args.raw else STYLES[args.style] + args.prompt
    key = load_key(args.env_file)
    raw, mime = generate(prompt, aspect, key)

    # The model picks the output format (usually JPEG); make the file extension
    # match the actual bytes so place_image.py keys the content-type correctly.
    want_ext = ".png" if mime == "image/png" else ".jpg"
    base, ext = os.path.splitext(args.out)
    out = args.out if ext.lower() in (".png", ".jpg", ".jpeg") and (
        (ext.lower() == ".png") == (mime == "image/png")) else base + want_ext

    with open(out, "wb") as f:
        f.write(raw)
    print(f"OK: wrote {out} ({len(raw)} bytes, {mime}, {aspect})")
    print("Note: image carries a C2PA/SynthID 'AI-generated' provenance watermark.")


if __name__ == "__main__":
    main()
