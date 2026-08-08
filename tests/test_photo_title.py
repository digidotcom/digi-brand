"""Guards for the Photo Deck Title layout and its photograph library.

Two things are easy to break silently here:

1. The layout must carry NO picture placeholder. A filled placeholder renders
   ABOVE the layout's scrim, logo, and triangles (slide shapes always outrank
   layout shapes in OOXML), which destroys the design without erroring. The
   photograph has to arrive as a slide background instead.

2. The four title photographs must SHIP. Digi owns them outright (confirmed by
   Taylor Salentine, 2026-08-07), and a plugin that makes every employee
   recover images by hand is not a plugin. They are files in assets/photos/,
   not embedded in the masters — the masters stay photograph-free because the
   photo is applied per deck as a slide background.
"""
import subprocess
import zipfile
from pathlib import Path

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


EXPECTED_PHOTOS = {
    "city-skyline-network",
    "night-city-connections",
    "offshore-platform",
    "transit-traveler",
}


def test_the_four_title_photographs_ship():
    # A plugin whose photo library has to be reassembled by hand on every
    # machine is not a plugin. Digi owns these outright, so they ship.
    tracked = subprocess.run(
        ["git", "ls-files", "assets/photos"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    stems = {Path(f).stem for f in tracked if not f.endswith(".md")}
    missing = EXPECTED_PHOTOS - stems
    assert not missing, f"title photographs missing from the repo: {sorted(missing)}"
    for name in EXPECTED_PHOTOS:
        matches = list((ROOT / "assets" / "photos").glob(f"{name}.*"))
        assert matches, f"{name} is tracked but not on disk"
        assert matches[0].stat().st_size > 10_000, f"{name} looks truncated"


def test_photo_library_readme_documents_each_photograph():
    readme = ROOT / "assets" / "photos" / "README.md"
    assert readme.is_file()
    text = readme.read_text()
    assert "set_title_photo.py" in text
    for name in EXPECTED_PHOTOS:
        assert name in text, f"{name} is undocumented in the photo library README"


def test_set_title_photo_script_runs():
    script = ROOT / "skills" / "digi-pptx" / "scripts" / "set_title_photo.py"
    assert script.is_file()
    out = subprocess.run(
        ["python3", str(script), "--list"],
        capture_output=True, text=True, check=True,
    )
    assert out.returncode == 0


TOOL = ROOT / "tools" / "add_photo_title_layout.py"


def test_graft_tool_documents_the_zorder_reason():
    assert TOOL.is_file()
    src = TOOL.read_text()
    assert "slide background" in src.lower(), (
        "the tool must record WHY the photo is a background and not a placeholder"
    )


def test_graft_tool_reads_nothing_outside_the_repo():
    # This plugin is distributed across Digi. A build step that reads someone's
    # home directory is not reproducible by anyone else, so every input the
    # graft needs is versioned in assets/photo-title-layout/.
    src = TOOL.read_text()
    for smell in ["Path.home()", "~/Downloads", "os.path.expanduser"]:
        assert smell not in src, f"graft tool must not reference {smell}"
    assert (ROOT / "assets" / "photo-title-layout" / "slideLayout.xml").is_file()
    assert (ROOT / "assets" / "photo-title-layout" / "logo.png").is_file()


def test_graft_tool_check_runs_anywhere_and_does_not_mutate():
    # No skipif: with the layout versioned in-repo this must work on any clone,
    # including a CI runner that has never seen a Digi template.
    before = [p.read_bytes() for p in MASTERS]
    out = subprocess.run(["python3", str(TOOL), "--check"],
                         cwd=ROOT, capture_output=True, text=True, check=True)
    after = [p.read_bytes() for p in MASTERS]
    assert before == after, "--check must not modify the masters"
    assert "already has" in out.stdout, (
        "shipped masters should already carry the layout"
    )
