import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_marketplace_manifest_is_valid():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert data["name"] == "digi-brand"
    assert data["owner"]["name"]
    assert data["owner"]["email"]
    assert len(data["plugins"]) == 1
    assert data["plugins"][0]["name"] == "digi-brand"
    assert data["plugins"][0]["source"] == "./"


def test_plugin_manifest_is_valid():
    data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert data["name"] == "digi-brand"
    assert data["description"]
    assert data["author"]["name"]


def test_version_is_calver():
    data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert re.fullmatch(r"\d{4}\.\d{2}\.\d{2}-\d+", data["version"]), (
        f"version {data['version']!r} must be CalVer YYYY.MM.DD-N"
    )


def test_both_masters_ship_and_old_template_is_gone():
    assets = ROOT / "assets"
    assert (assets / "2024-Digi-Confidential-PPT-Template.potx").is_file()
    assert (assets / "2024-Digi-Public-PPT-Template.potx").is_file()
    assert not (assets / "digi-template.pptx").exists(), "old merged template must not ship"


def test_vendored_fonts_carry_the_ofl():
    fonts = ROOT / "assets" / "fonts"
    ofl = (fonts / "OFL.txt").read_text()
    assert "SIL OPEN FONT LICENSE Version 1.1" in ofl
    # both naming generations, so decks resolve whichever family the master XML names
    for stem in ["SourceSansPro", "SourceSans3"]:
        for weight in ["Regular", "Bold", "Semibold", "Black"]:
            assert (fonts / f"{stem}-{weight}.otf").is_file(), f"{stem}-{weight}.otf missing"
