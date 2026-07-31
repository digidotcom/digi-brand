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
