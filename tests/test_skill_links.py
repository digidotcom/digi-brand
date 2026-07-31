"""Guards skills/digi-pptx/SKILL.md against dangling path references.

A `${CLAUDE_PLUGIN_ROOT}`-relative path or a relative markdown-link path that
points at a file that does not exist is invisible in this repo (the token
and the relative path both resolve fine as *text*) and only breaks after a
colleague installs the plugin and Claude tries to read the reference. This
is exactly the breakage class a directory restructure risks — file it once,
guard it forever.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = ROOT / "skills" / "digi-pptx" / "SKILL.md"

# ${CLAUDE_PLUGIN_ROOT}/some/path — captured up to the next backtick, quote,
# whitespace, or markdown/punctuation delimiter that isn't part of a path.
PLUGIN_ROOT_PATH = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s`'\")]+)")

# Markdown links: [text](path) — excludes bare URLs (http/https/mailto).
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")


def _is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def _strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def test_skill_md_exists():
    assert SKILL_MD.is_file(), "skills/digi-pptx/SKILL.md is missing"


def test_plugin_root_paths_resolve():
    text = SKILL_MD.read_text()
    matches = PLUGIN_ROOT_PATH.findall(text)
    assert matches, "expected at least one ${CLAUDE_PLUGIN_ROOT}-relative path"
    missing = []
    for rel in matches:
        rel = rel.rstrip(".,;:")
        if not (ROOT / rel).is_file():
            missing.append(rel)
    assert not missing, (
        "SKILL.md references ${CLAUDE_PLUGIN_ROOT}-relative paths that do "
        f"not resolve to a real file: {missing}"
    )


def test_relative_markdown_links_resolve():
    text = SKILL_MD.read_text()
    matches = MARKDOWN_LINK.findall(text)
    relative = [m for m in matches if not _is_external(m)]
    assert relative, "expected at least one relative markdown link"
    missing = []
    for target in relative:
        target = _strip_anchor(target).rstrip(".,;:")
        if not target:
            # A pure in-page anchor link (e.g. "#section") has nothing left
            # to resolve as a file path.
            continue
        resolved = (SKILL_MD.parent / target).resolve()
        if not resolved.is_file():
            missing.append(target)
    assert not missing, (
        "SKILL.md has relative markdown links that do not resolve to a "
        f"real file: {missing}"
    )
