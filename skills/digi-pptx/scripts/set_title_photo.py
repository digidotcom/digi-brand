#!/usr/bin/env python3
"""Set a slide's background photograph — for the 'Photo Deck Title' layout.

The photo goes on as the SLIDE BACKGROUND, not as a picture on the slide.
That is not a stylistic choice. OOXML renders in the order

    slide background -> master shapes -> layout shapes -> slide shapes

so anything placed ON the slide draws ABOVE the layout's translucent scrim,
its logo, and its green triangles, hiding the whole design. The background is
the only surface beneath layout chrome, which is where the photograph must sit
for the scrim to read over it. Use `place_image.py` for ordinary content
images; use this only for the title photograph.

Run on an UNPACKED deck (after unpack.py, before pack.py), same as
place_image.py.

    # one of the four library photos
    python3 set_title_photo.py --unpacked unpacked/ --slide 1 \
        --photo night-city-connections

    # any custom image
    python3 set_title_photo.py --unpacked unpacked/ --slide 1 \
        --image work/customer-site.jpg

    python3 set_title_photo.py --list        # show the library

The library lives in `assets/photos/` and is NOT in git — those are
third-party licensed stock images, fine to use in Digi decks, not ours to
redistribute from a public repo. See `assets/photos/README.md` to populate it.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from lxml import etree

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"

PHOTO_DIR = Path(__file__).resolve().parents[3] / "assets" / "photos"
CONTENT_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def q(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def library() -> dict[str, Path]:
    if not PHOTO_DIR.is_dir():
        return {}
    return {p.stem: p for p in sorted(PHOTO_DIR.iterdir())
            if p.suffix.lower() in CONTENT_TYPES}


def resolve(args) -> Path:
    if args.image:
        p = Path(args.image)
        if not p.is_file():
            sys.exit(f"no such image: {p}")
        if p.suffix.lower() not in CONTENT_TYPES:
            sys.exit(f"unsupported image type {p.suffix} (use jpg/jpeg/png)")
        return p
    lib = library()
    if args.photo not in lib:
        names = ", ".join(lib) or "(library empty — see assets/photos/README.md)"
        sys.exit(f"unknown library photo {args.photo!r}. Available: {names}")
    return lib[args.photo]


def set_background(unpacked: Path, slide_no: int, image: Path) -> str:
    slide = unpacked / "ppt" / "slides" / f"slide{slide_no}.xml"
    if not slide.is_file():
        sys.exit(f"no such slide: {slide}")
    rels_path = slide.parent / "_rels" / f"{slide.name}.rels"
    if not rels_path.is_file():
        sys.exit(f"missing relationships for slide {slide_no}: {rels_path}")

    media = unpacked / "ppt" / "media"
    media.mkdir(parents=True, exist_ok=True)
    dest_name = f"titlephoto{slide_no}{image.suffix.lower()}"
    shutil.copy(image, media / dest_name)

    # Relationship (reuse ours if this slide already has a background photo).
    rels = etree.parse(str(rels_path))
    rid = None
    for rel in rels.getroot():
        if rel.get("Id") == "rIdTitlePhoto":
            rel.set("Target", f"../media/{dest_name}")
            rid = "rIdTitlePhoto"
    if rid is None:
        rid = "rIdTitlePhoto"
        rel = etree.SubElement(rels.getroot(), f"{{{PR}}}Relationship")
        rel.set("Id", rid)
        rel.set("Type", f"{R}/image")
        rel.set("Target", f"../media/{dest_name}")
    rels.write(str(rels_path), xml_declaration=True, encoding="UTF-8",
               standalone=True)

    # <p:bg> must be the FIRST child of <p:cSld>; replace any existing one.
    tree = etree.parse(str(slide))
    cSld = tree.getroot().find(q(P, "cSld"))
    for old in cSld.findall(q(P, "bg")):
        cSld.remove(old)
    bg = etree.Element(q(P, "bg"))
    bgPr = etree.SubElement(bg, q(P, "bgPr"))
    blipFill = etree.SubElement(bgPr, q(A, "blipFill"))
    etree.SubElement(blipFill, q(A, "blip")).set(q(R, "embed"), rid)
    etree.SubElement(etree.SubElement(blipFill, q(A, "stretch")), q(A, "fillRect"))
    etree.SubElement(bgPr, q(A, "effectLst"))
    cSld.insert(0, bg)
    tree.write(str(slide), xml_declaration=True, encoding="UTF-8",
               standalone=True)

    # Make sure the extension has a content-type default.
    ct_path = unpacked / "[Content_Types].xml"
    ct = etree.parse(str(ct_path))
    ext = image.suffix.lower().lstrip(".")
    have = {d.get("Extension") for d in ct.getroot()
            if etree.QName(d).localname == "Default"}
    if ext not in have:
        d = etree.SubElement(ct.getroot(), f"{{{CT}}}Default")
        d.set("Extension", ext)
        d.set("ContentType", CONTENT_TYPES[image.suffix.lower()])
        ct.write(str(ct_path), xml_declaration=True, encoding="UTF-8",
                 standalone=True)

    return f"slide {slide_no}: background set to {image.name}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unpacked", type=Path, help="unpacked deck directory")
    ap.add_argument("--slide", type=int, default=1, help="slide number (default 1)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--photo", help="name from the assets/photos library")
    g.add_argument("--image", help="path to any custom image")
    ap.add_argument("--list", action="store_true", help="list the photo library")
    args = ap.parse_args()

    if args.list:
        lib = library()
        if not lib:
            print("photo library is empty — see assets/photos/README.md")
            return 0
        for name, path in lib.items():
            print(f"  {name:<28} {path.stat().st_size // 1024:>5} KB")
        return 0

    if not args.unpacked:
        ap.error("--unpacked is required (or use --list)")
    if not args.photo and not args.image:
        ap.error("give --photo <library-name> or --image <path>")

    print(set_background(args.unpacked, args.slide, resolve(args)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
