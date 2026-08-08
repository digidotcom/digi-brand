#!/usr/bin/env python3
"""Graft a 'Photo Deck Title' layout into the official 2024 Digi masters.

WHY THIS EXISTS
---------------
The official 2024 masters ship one title layout: an OPAQUE white diagonal
(`Freeform 8`, fill `schemeClr bg1` @ 100%) over white. An earlier Digi
template generation had a photo title that is the SAME freeform — identical
bbox and identical four path points (0,0)/(4.38,0)/(10.00,5.63)/(0,5.63) —
filled instead as a translucent dark scrim (`srgbClr 202123` @ 62%) sitting
over a full-bleed photograph. One fill value is the entire difference.

This script rebuilds that layout on the official masters, with one change that
matters: the old layout EMBEDDED its photograph as a fixed `<p:pic>`, locking
every deck to one stock image. Here the photograph is REMOVED entirely and the
deck supplies it as a **slide background** (`tools/set_title_photo.py`), so:

  * no photograph ships inside the .potx — the title imagery is of unverified
    provenance and this repo is public (see assets/photos/README.md);
  * any image works — one of the four library photos, or a custom one;
  * with no photo set, the layout renders as the scrim over white. Nothing breaks.

WHY BACKGROUND AND NOT A PICTURE PLACEHOLDER
--------------------------------------------
A picture placeholder was tried first and does not work. In OOXML the render
order is slide background -> master shapes -> layout shapes -> slide shapes.
A placeholder filled on the SLIDE therefore draws ABOVE the layout's scrim,
logo, and green triangles, hiding all of them — verified by render. Placeholder
inheritance supplies geometry, never z-order. The slide background is the only
surface that sits BENEATH layout chrome, which is exactly where the photograph
has to be for the translucent scrim to read over it.

So this script deliberately leaves NO picture placeholder on the layout: one
would invite a fill that silently destroys the design.

USAGE
-----
    python3 tools/add_photo_title_layout.py            # both masters, in place
    python3 tools/add_photo_title_layout.py --check    # report, change nothing

Idempotent: re-running on a master that already carries the layout is a no-op.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MASTERS = [
    ASSETS / "2024-Digi-Confidential-PPT-Template.potx",
    ASSETS / "2024-Digi-Public-PPT-Template.potx",
]
# The earlier-generation template the photo title is recovered from.
SOURCE_TEMPLATE = Path.home() / "Downloads" / "Digi template.pptx"
SOURCE_LAYOUT = "slideLayout36.xml"          # "7_Deck Title"
LAYOUT_NAME = "Photo Deck Title"


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"p": P, "a": A, "r": R}

LAYOUT_CT = ("application/vnd.openxmlformats-officedocument."
             "presentationml.slideLayout+xml")


def q(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def unpack(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(["unzip", "-q", "-o", str(src), "-d", str(dest)], check=True)


def repack(srcdir: Path, dest: Path) -> None:
    if dest.exists():
        dest.unlink()
    subprocess.run(["zip", "-qr", str(dest), ".", "-x", ".*"],
                   cwd=srcdir, check=True)


def next_free(dirpath: Path, stem: str, ext: str) -> str:
    """First unused '<stem>N.<ext>' in dirpath, N starting at 1."""
    n = 1
    while (dirpath / f"{stem}{n}.{ext}").exists():
        n += 1
    return f"{stem}{n}.{ext}"


def build_layout(src_xml: Path, logo_rid: str) -> tuple[etree._ElementTree, dict]:
    """Transform the source photo-title layout into our placeholder version."""
    tree = etree.parse(str(src_xml))
    root = tree.getroot()
    spTree = root.find(f".//{q(P, 'spTree')}")
    info: dict = {}

    # Name the layout.
    cSld = root.find(q(P, "cSld"))
    cSld.set("name", LAYOUT_NAME)

    photo_pic = logo_pic = None
    for pic in spTree.findall(q(P, "pic")):
        blip = pic.find(f".//{q(A, 'blip')}")
        rid = blip.get(q(R, "embed")) if blip is not None else None
        # Scope to a:xfrm/a:ext — a bare .//a:ext also matches <a:ext uri="…">
        # inside extLst, which carries no cx/cy.
        ext = pic.find(f".//{q(A, 'xfrm')}/{q(A, 'ext')}")
        cx = int(ext.get("cx")) if ext is not None else 0
        # The full-bleed photograph is the one spanning the whole slide.
        if cx > 8_000_000:
            photo_pic, info["photo_rid"] = pic, rid
        else:
            logo_pic, info["logo_rid"] = pic, rid

    if photo_pic is None:
        raise SystemExit("could not find the full-bleed photograph in the source layout")

    # Drop the embedded photograph outright. The deck supplies it as a slide
    # background instead (see the module docstring for why a placeholder here
    # would be actively harmful).
    xfrm = photo_pic.find(f".//{q(A, 'xfrm')}")
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    info["pic_zone"] = (int(off.get("x")), int(off.get("y")),
                        int(ext.get("cx")), int(ext.get("cy")))
    spTree.remove(photo_pic)

    # Re-point the logo at its new relationship id in the destination package.
    if logo_pic is not None:
        blip = logo_pic.find(f".//{q(A, 'blip')}")
        blip.set(q(R, "embed"), logo_rid)

    # Title slides in the 2024 masters carry no classification footer; drop the
    # source layout's slide-number placeholder so this one matches.
    for sp in list(spTree.findall(q(P, "sp"))):
        ph = sp.find(f".//{q(P, 'ph')}")
        if ph is not None and ph.get("type") in ("sldNum", "ftr", "dt"):
            spTree.remove(sp)

    return tree, info


def already_present(work: Path) -> bool:
    for lay in (work / "ppt" / "slideLayouts").glob("slideLayout*.xml"):
        cSld = etree.parse(str(lay)).getroot().find(q(P, "cSld"))
        if cSld is not None and cSld.get("name") == LAYOUT_NAME:
            return True
    return False


def graft(master: Path, src_dir: Path, check: bool) -> str:
    work = Path(tempfile.mkdtemp(prefix="digibrand-"))
    try:
        unpack(master, work)
        if already_present(work):
            return f"{master.name}: already has '{LAYOUT_NAME}' — no change"
        if check:
            return f"{master.name}: WOULD add '{LAYOUT_NAME}'"

        layouts = work / "ppt" / "slideLayouts"
        media = work / "ppt" / "media"
        media.mkdir(exist_ok=True)

        # Bring the logo bitmap across (Digi's own artwork).
        src_rels = etree.parse(str(src_dir / "ppt" / "slideLayouts" / "_rels"
                                   / f"{SOURCE_LAYOUT}.rels"))
        src_imgs = {r.get("Id"): r.get("Target") for r in src_rels.getroot()
                    if "image" in r.get("Type")}
        # The logo is the smaller of the two images in the source layout.
        by_size = sorted(
            src_imgs.items(),
            key=lambda kv: (src_dir / "ppt" / "slideLayouts" / kv[1]).resolve().stat().st_size,
        )
        logo_src = (src_dir / "ppt" / "slideLayouts" / by_size[0][1]).resolve()
        logo_name = next_free(media, "image", logo_src.suffix.lstrip("."))
        shutil.copy(logo_src, media / logo_name)

        layout_name = next_free(layouts, "slideLayout", "xml")
        tree, info = build_layout(
            src_dir / "ppt" / "slideLayouts" / SOURCE_LAYOUT, "rId2")
        tree.write(str(layouts / layout_name), xml_declaration=True,
                   encoding="UTF-8", standalone=True)

        # Relationships for the new layout: its master + the logo.
        rels = etree.Element(f"{{{PR}}}Relationships", nsmap={None: PR})
        r1 = etree.SubElement(rels, f"{{{PR}}}Relationship")
        r1.set("Id", "rId1")
        r1.set("Type", f"{R}/slideMaster")
        r1.set("Target", "../slideMasters/slideMaster1.xml")
        r2 = etree.SubElement(rels, f"{{{PR}}}Relationship")
        r2.set("Id", "rId2")
        r2.set("Type", f"{R}/image")
        r2.set("Target", f"../media/{logo_name}")
        (layouts / "_rels").mkdir(exist_ok=True)
        etree.ElementTree(rels).write(
            str(layouts / "_rels" / f"{layout_name}.rels"),
            xml_declaration=True, encoding="UTF-8", standalone=True)

        # Register on slideMaster1 (the title master): rels + sldLayoutIdLst.
        mrels_path = work / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
        mrels = etree.parse(str(mrels_path))
        used = {r.get("Id") for r in mrels.getroot()}
        n = 1
        while f"rId{n}" in used:
            n += 1
        new_rid = f"rId{n}"
        rel = etree.SubElement(mrels.getroot(), f"{{{PR}}}Relationship")
        rel.set("Id", new_rid)
        rel.set("Type", f"{R}/slideLayout")
        rel.set("Target", f"../slideLayouts/{layout_name}")
        mrels.write(str(mrels_path), xml_declaration=True, encoding="UTF-8",
                    standalone=True)

        mpath = work / "ppt" / "slideMasters" / "slideMaster1.xml"
        mtree = etree.parse(str(mpath))
        lst = mtree.getroot().find(f".//{q(P, 'sldLayoutIdLst')}")
        ids = [int(c.get("id")) for c in lst]
        new = etree.SubElement(lst, q(P, "sldLayoutId"))
        new.set("id", str(max(ids) + 1))
        new.set(q(R, "id"), new_rid)
        mtree.write(str(mpath), xml_declaration=True, encoding="UTF-8",
                    standalone=True)

        # Content type override for the new layout part.
        ctpath = work / "[Content_Types].xml"
        ct = etree.parse(str(ctpath))
        ov = etree.SubElement(ct.getroot(), f"{{{CT}}}Override")
        ov.set("PartName", f"/ppt/slideLayouts/{layout_name}")
        ov.set("ContentType", LAYOUT_CT)
        # Ensure the logo's extension has a default.
        ext = logo_src.suffix.lstrip(".").lower()
        defaults = {d.get("Extension") for d in ct.getroot()
                    if etree.QName(d).localname == "Default"}
        if ext not in defaults:
            d = etree.SubElement(ct.getroot(), f"{{{CT}}}Default")
            d.set("Extension", ext)
            d.set("ContentType", f"image/{'jpeg' if ext in ('jpg', 'jpeg') else ext}")
        ct.write(str(ctpath), xml_declaration=True, encoding="UTF-8",
                 standalone=True)

        repack(work, master)
        x, y, cx, cy = info["pic_zone"]
        return (f"{master.name}: added '{LAYOUT_NAME}' as {layout_name} "
                f"(photo removed; deck supplies it as slide background; scrim zone "
                f"{x/914400:.2f},{y/914400:.2f} {cx/914400:.2f}x{cy/914400:.2f}in)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report what would change; write nothing")
    ap.add_argument("--source", type=Path, default=SOURCE_TEMPLATE,
                    help="template to recover the photo title layout from")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"source template not found: {args.source}", file=sys.stderr)
        return 2

    src_dir = Path(tempfile.mkdtemp(prefix="digibrand-src-"))
    try:
        unpack(args.source, src_dir)
        for m in MASTERS:
            if not m.exists():
                print(f"missing master: {m}", file=sys.stderr)
                return 2
            print(graft(m, src_dir, args.check))
    finally:
        shutil.rmtree(src_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
