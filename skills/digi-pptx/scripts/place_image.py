#!/usr/bin/env python3
"""
place_image.py — Drop an image into an unpacked slide at a named zone.

Why this exists: putting a picture into a .pptx by hand means copying the file
into ppt/media, registering a content-type, adding a relationship, AND hand-
writing a <p:pic> with EMU geometry — four fiddly steps every deck reinvents
and gets subtly wrong. This does all four. Works for BOTH a generated graphic
(from gen_graphic.py) and a real screenshot you provide.

Run it on an UNPACKED template dir (after pptx unpack.py, before pack.py).

Usage:
  python place_image.py --unpacked unpacked/ --slide 2 --image g.png --zone right-half
  python place_image.py --unpacked unpacked/ --slide 2 --image shot.png \
      --x 5.15 --y 1.30 --w 4.30 --h 3.60 --fit

Zones (inches, on the 10 x 5.625" canvas; all sit below the title and above the
footer). Generated graphics should be made at the zone's aspect (see
gen_graphic.py --zone) so they FILL the box. For a real screenshot whose aspect
differs, pass --fit to preserve aspect and center it inside the box.

  right-half  x5.15 y1.30 w4.30 h3.45   (text lives on the left)   ~4:3
  left-half   x0.38 y1.30 w4.30 h3.45   (text lives on the right)  ~4:3
  hero        x1.50 y1.15 w7.00 h3.94   (centered, text above/below) 16:9
  full-band   x0.38 y1.15 w9.15 h3.92   (wide band under the title)  21:9
  square      x3.25 y1.30 w3.50 h3.50   (centered)                   1:1
"""
import argparse
import os
import re
import shutil
import struct
import sys

EMU = 914400  # EMU per inch

ZONES = {
    "right-half": (5.15, 1.30, 4.30, 3.45),
    "left-half": (0.38, 1.30, 4.30, 3.45),
    "hero": (1.50, 1.15, 7.00, 3.94),
    "full-band": (0.38, 1.15, 9.15, 3.92),
    "square": (3.25, 1.30, 3.50, 3.50),
}
CONTENT_TYPE = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def image_size(path):
    """Return (w_px, h_px) for PNG/JPEG without external deps. None if unknown."""
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        f.seek(0)
        if f.read(2) == b"\xff\xd8":  # JPEG
            while True:
                b = f.read(1)
                if not b:
                    return None
                if b != b"\xff":
                    continue
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                if marker[0] in (0xD8, 0xD9) or 0xD0 <= marker[0] <= 0xD7:
                    continue
                seglen = struct.unpack(">H", f.read(2))[0]
                if 0xC0 <= marker[0] <= 0xCF and marker[0] not in (0xC4, 0xC8, 0xCC):
                    f.read(1)  # precision
                    h, w = struct.unpack(">HH", f.read(4))
                    return (w, h)
                f.seek(seglen - 2, 1)
    return None


def next_media_name(media_dir, ext):
    os.makedirs(media_dir, exist_ok=True)
    nums = [int(m.group(1)) for fn in os.listdir(media_dir)
            for m in [re.match(r"image(\d+)\.", fn)] if m]
    return f"image{(max(nums) + 1) if nums else 1}{ext}"


def ensure_content_type(unpacked, ext):
    ct_path = os.path.join(unpacked, "[Content_Types].xml")
    with open(ct_path, encoding="utf-8") as f:
        ct = f.read()
    key = ext.lstrip(".")
    if f'Extension="{key}"' in ct:
        return
    entry = f'<Default Extension="{key}" ContentType="{CONTENT_TYPE[ext]}"/>'
    ct = ct.replace("</Types>", entry + "</Types>")
    with open(ct_path, "w", encoding="utf-8") as f:
        f.write(ct)


def add_relationship(unpacked, slide, media_name):
    rels_path = os.path.join(unpacked, "ppt", "slides", "_rels", f"slide{slide}.xml.rels")
    with open(rels_path, encoding="utf-8") as f:
        rels = f.read()
    used = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
    rid = f"rId{(max(used) + 1) if used else 1}"
    rel = (f'<Relationship Id="{rid}" '
           'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
           f'Target="../media/{media_name}"/>')
    rels = rels.replace("</Relationships>", rel + "</Relationships>")
    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(rels)
    return rid


def inject_pic(unpacked, slide, rid, name, x, y, w, h):
    slide_path = os.path.join(unpacked, "ppt", "slides", f"slide{slide}.xml")
    with open(slide_path, encoding="utf-8") as f:
        xml = f.read()
    used_ids = [int(m) for m in re.findall(r'id="(\d+)"', xml)]
    sid = (max(used_ids) + 1) if used_ids else 100
    ox, oy, cx, cy = (round(v * EMU) for v in (x, y, w, h))
    pic = (
        '<p:pic>'
        f'<p:nvPicPr><p:cNvPr id="{sid}" name="{name}"/>'
        '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
        '<p:nvPr/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="{ox}" y="{oy}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'
    )
    xml = xml.replace("</p:spTree>", pic + "</p:spTree>", 1)
    with open(slide_path, "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    ap = argparse.ArgumentParser(description="Place an image into an unpacked slide.")
    ap.add_argument("--unpacked", required=True, help="Unpacked .pptx dir (from unpack.py).")
    ap.add_argument("--slide", required=True, type=int, help="Slide number, e.g. 2.")
    ap.add_argument("--image", required=True, help="Image file (.png/.jpg/.jpeg).")
    ap.add_argument("--zone", choices=sorted(ZONES), help="Named slide zone.")
    ap.add_argument("--x", type=float, help="Left (in). Use with --y/--w/--h instead of --zone.")
    ap.add_argument("--y", type=float)
    ap.add_argument("--w", type=float)
    ap.add_argument("--h", type=float)
    ap.add_argument("--fit", action="store_true",
                    help="Preserve image aspect, center inside the box (for real screenshots).")
    args = ap.parse_args()

    if args.zone:
        x, y, w, h = ZONES[args.zone]
    elif None not in (args.x, args.y, args.w, args.h):
        x, y, w, h = args.x, args.y, args.w, args.h
    else:
        sys.exit("ERROR: pass --zone OR all of --x --y --w --h.")

    ext = os.path.splitext(args.image)[1].lower()
    if ext not in CONTENT_TYPE:
        sys.exit(f"ERROR: unsupported image type {ext!r}; use .png/.jpg/.jpeg.")

    if args.fit:
        size = image_size(args.image)
        if size:
            iw, ih = size
            scale = min(w / iw, h / ih)
            nw, nh = iw * scale, ih * scale
            x, y = x + (w - nw) / 2, y + (h - nh) / 2
            w, h = nw, nh

    media_dir = os.path.join(args.unpacked, "ppt", "media")
    name = next_media_name(media_dir, ext)
    shutil.copyfile(args.image, os.path.join(media_dir, name))
    ensure_content_type(args.unpacked, ext)
    rid = add_relationship(args.unpacked, args.slide, name)
    inject_pic(args.unpacked, args.slide, rid, name, x, y, w, h)
    print(f"OK: placed {args.image} as media/{name} ({rid}) on slide{args.slide} "
          f"at x{x:.2f} y{y:.2f} w{w:.2f} h{h:.2f} in.")


if __name__ == "__main__":
    main()
