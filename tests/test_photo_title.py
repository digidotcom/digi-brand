"""Guards for the Photo Deck Title layout and its photograph library.

Two things are easy to break silently here:

1. The layout must carry NO picture placeholder. A filled placeholder renders
   ABOVE the layout's scrim, logo, and triangles (slide shapes always outrank
   layout shapes in OOXML), which destroys the design without erroring. The
   photograph has to arrive as a slide background instead.

2. No photograph may ship inside the masters or the repo. The stock imagery is
   third-party licensed — usable in Digi decks, not ours to redistribute from a
   public repo.
"""
import subprocess
import zipfile
from pathlib import Path

import pytest
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
MASTERS = [
    ROOT / "assets" / "2024-Digi-Confidential-PPT-Template.potx",
    ROOT / "assets" / "2024-Digi-Public-PPT-Template.potx",
]
LAYOUT_NAME = "Photo Deck Title"


def _layouts(potx: Path):
    z = zipfile.ZipFile(potx)
    for name in z.namelist():
        if name.startswith("ppt/slideLayouts/slideLayout") and name.endswith(".xml"):
            yield name, etree.fromstring(z.read(name))


def _photo_layout(potx: Path):
    for name, root in _layouts(potx):
        cSld = root.find(f"{{{P}}}cSld")
        if cSld is not None and cSld.get("name") == LAYOUT_NAME:
            return name, root
    return None, None


def test_both_masters_carry_the_photo_title_layout():
    for potx in MASTERS:
        name, root = _photo_layout(potx)
        assert root is not None, f"{potx.name} is missing the {LAYOUT_NAME!r} layout"


def test_photo_title_has_no_picture_placeholder():
    # A picture placeholder here is worse than useless: filling it draws the
    # image over the scrim and chrome. The photo must go on as a background.
    for potx in MASTERS:
        _, root = _photo_layout(potx)
        kinds = [ph.get("type") for ph in root.iter(f"{{{P}}}ph")]
        assert "pic" not in kinds, (
            f"{potx.name}: {LAYOUT_NAME} must not expose a picture placeholder — "
            "a filled one renders above the layout scrim and hides the design"
        )
        assert "title" in kinds, f"{potx.name}: {LAYOUT_NAME} lost its title placeholder"


def test_masters_ship_no_photographs():
    # docProps/thumbnail.jpeg is Office's own preview and predates our changes;
    # anything else photographic would be third-party imagery we cannot publish.
    for potx in MASTERS:
        z = zipfile.ZipFile(potx)
        photos = [
            n for n in z.namelist()
            if n.lower().endswith((".jpg", ".jpeg"))
            and not n.startswith("docProps/")
        ]
        assert photos == [], f"{potx.name} ships photographic media: {photos}"


def test_photo_library_images_are_not_tracked_by_git():
    tracked = subprocess.run(
        ["git", "ls-files", "assets/photos"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    offenders = [f for f in tracked if not f.endswith(".md")]
    assert offenders == [], (
        f"third-party stock photography must not be committed to this public repo: {offenders}"
    )


def test_photo_library_readme_is_tracked_and_explains_how_to_populate():
    readme = ROOT / "assets" / "photos" / "README.md"
    assert readme.is_file()
    text = readme.read_text()
    assert "set_title_photo.py" in text
    assert "licensed" in text.lower()


def test_set_title_photo_script_runs():
    script = ROOT / "skills" / "digi-pptx" / "scripts" / "set_title_photo.py"
    assert script.is_file()
    out = subprocess.run(
        ["python3", str(script), "--list"],
        capture_output=True, text=True, check=True,
    )
    assert out.returncode == 0


TOOL = ROOT / "tools" / "add_photo_title_layout.py"
# The graft tool reads the earlier-generation template to recover the layout.
# That file is a local Digi asset, absent on CI runners — the tool exits 2 and
# says so, which is correct behaviour, not a failure to assert against.
SOURCE_TEMPLATE = Path.home() / "Downloads" / "Digi template.pptx"


def test_graft_tool_documents_the_zorder_reason():
    assert TOOL.is_file()
    src = TOOL.read_text()
    assert "slide background" in src.lower(), (
        "the tool must record WHY the photo is a background and not a placeholder"
    )


@pytest.mark.skipif(not SOURCE_TEMPLATE.is_file(),
                    reason="source template not available (expected on CI)")
def test_graft_tool_check_does_not_mutate_the_masters():
    before = [p.read_bytes() for p in MASTERS]
    subprocess.run(["python3", str(TOOL), "--check"],
                   cwd=ROOT, capture_output=True, text=True, check=True)
    after = [p.read_bytes() for p in MASTERS]
    assert before == after, "--check must not modify the masters"
