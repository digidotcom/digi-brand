#!/usr/bin/env python3
"""Graft the 'Photo Deck Title' layout into the official 2024 Digi masters.

WHY THIS EXISTS
---------------
The official 2024 masters ship one title layout: an OPAQUE white diagonal
(`Freeform 8`, fill `schemeClr bg1` @ 100%) over white. An earlier Digi
template generation had a photo title that is the SAME freeform — identical
bbox and identical four path points (0,0)/(4.38,0)/(10.00,5.63)/(0,5.63) —
filled instead as a translucent dark scrim (`srgbClr 202123` @ 62%) sitting
over a full-bleed photograph. One fill value is the entire difference.

The layout is a first-class asset of this repo: `assets/photo-title-layout/`
holds its `slideLayout.xml` and the DIGI logo it draws. **Nothing here reads
from anyone's personal filesystem** — this plugin is distributed across Digi,
so every input it needs is versioned alongside it and any clone can rebuild
the masters identically.

The photograph is NOT part of the layout. It arrives per deck as a slide
background via `skills/digi-pptx/scripts/set_title_photo.py`, which means:

  * no photograph is baked into the .potx, so one template serves every deck;
  * any image works — one of the four in `assets/photos/`, or a custom one;
  * with no photo set, the layout renders as scrim-over-white. Nothing breaks.

WHY BACKGROUND AND NOT A PICTURE PLACEHOLDER
--------------------------------------------
A picture placeholder was tried first and does not work. In OOXML the render
order is slide background -> master shapes -> layout shapes -> slide shapes.
A placeholder filled on the SLIDE therefore draws ABOVE the layout's scrim,
logo, and green triangles, hiding all of them — verified by render. Placeholder
inheritance supplies geometry, never z-order. The slide background is the only
surface that sits BENEATH layout chrome, which is exactly where the photograph
has to be for the translucent scrim to read over it.

So the layout deliberately carries NO picture placeholder: one would invite a
fill that silently destroys the design. `tests/test_photo_title.py` pins that.

USAGE
-----
    python3 tools/add_photo_title_layout.py            # both masters, in place
    python3 tools/add_photo_title_layout.py --check    # report, change nothing

Run it after replacing the masters with fresh files from Digi marketing; the
layout is re-applied from the versioned asset. Idempotent: re-running on a
master that already carries the layout is a no-op.
"""
from __future__ import annotations

import argparse
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
# The layout and its logo, versioned in this repo. No external inputs.
LAYOUT_SRC = ASSETS / "photo-title-layout" / "slideLayout.xml"
LOGO_SRC = ASSETS / "photo-title-layout" / "logo.png"
LAYOUT_NAME = "Photo Deck Title"

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"

LAYOUT_CT = ("application/vnd.openxmlformats-officedocument."
             "presentationml.slideLayout+xml")
# The logo relationship id inside the versioned slideLayout.xml.
LOGO_RID = "rId2"


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


def already_present(work: Path) -> bool:
    for lay in (work / "ppt" / "slideLayouts").glob("slideLayout*.xml"):
        cSld = etree.parse(str(lay)).getroot().find(q(P, "cSld"))
        if cSld is not None and cSld.get("name") == LAYOUT_NAME:
            return True
    return False


def graft(master: Path, check: bool) -> str:
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

        logo_name = next_free(media, "image", "png")
        shutil.copy(LOGO_SRC, media / logo_name)

        layout_name = next_free(layouts, "slideLayout", "xml")
        shutil.copy(LAYOUT_SRC, layouts / layout_name)

        # Relationships for the new layout: its master + the logo.
        rels = etree.Element(f"{{{PR}}}Relationships", nsmap={None: PR})
        r1 = etree.SubElement(rels, f"{{{PR}}}Relationship")
        r1.set("Id", "rId1")
        r1.set("Type", f"{R}/slideMaster")
        r1.set("Target", "../slideMasters/slideMaster1.xml")
        r2 = etree.SubElement(rels, f"{{{PR}}}Relationship")
        r2.set("Id", LOGO_RID)
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
        defaults = {d.get("Extension") for d in ct.getroot()
                    if etree.QName(d).localname == "Default"}
        if "png" not in defaults:
            d = etree.SubElement(ct.getroot(), f"{{{CT}}}Default")
            d.set("Extension", "png")
            d.set("ContentType", "image/png")
        ct.write(str(ctpath), xml_declaration=True, encoding="UTF-8",
                 standalone=True)

        repack(work, master)
        return f"{master.name}: added '{LAYOUT_NAME}' as {layout_name}"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report what would change; write nothing")
    args = ap.parse_args()

    for asset in (LAYOUT_SRC, LOGO_SRC):
        if not asset.is_file():
            print(f"missing versioned asset: {asset}", file=sys.stderr)
            return 2

    for m in MASTERS:
        if not m.exists():
            print(f"missing master: {m}", file=sys.stderr)
            return 2
        print(graft(m, args.check))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
