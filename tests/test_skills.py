import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

SPINE = "digi-brand-guidelines"
SPINE_REF = "${CLAUDE_PLUGIN_ROOT}/skills/digi-brand-guidelines/SKILL.md"

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def test_every_skill_has_a_skill_md():
    for d in skill_dirs():
        assert (d / "SKILL.md").is_file(), f"{d.name} is missing SKILL.md"


def test_every_skill_has_name_and_description_frontmatter():
    for d in skill_dirs():
        text = (d / "SKILL.md").read_text()
        match = FRONTMATTER.match(text)
        assert match, f"{d.name}: SKILL.md has no YAML frontmatter"
        block = match.group(1)
        assert re.search(r"^name:\s*\S", block, re.M), f"{d.name}: no name in frontmatter"
        assert re.search(r"^description:\s*\S", block, re.M), f"{d.name}: no description"


def test_frontmatter_name_matches_directory():
    for d in skill_dirs():
        block = FRONTMATTER.match((d / "SKILL.md").read_text()).group(1)
        name = re.search(r"^name:\s*(\S+)", block, re.M).group(1)
        assert name == d.name, f"{d.name}: frontmatter name is {name!r}"


def test_deliverable_skills_read_the_spine():
    for d in skill_dirs():
        if d.name == SPINE:
            continue
        text = (d / "SKILL.md").read_text()
        assert SPINE_REF in text, f"{d.name}: does not reference the spine"


def test_deliverable_skills_have_an_inline_fallback_palette():
    for d in skill_dirs():
        if d.name == SPINE:
            continue
        text = (d / "SKILL.md").read_text()
        assert "1B4965" in text and "91D46C" in text, (
            f"{d.name}: missing the inline fallback palette"
        )


def test_spine_declares_every_palette_slot():
    text = (SKILLS / SPINE / "SKILL.md").read_text().upper()
    for hex_value in [
        "1B4965", "FFFFFF", "3F4245", "F5F7F7", "91D46C",
        "DAD8D8", "1F7FA5", "CC6033", "E2F6FF", "56565A", "00B7FF",
    ]:
        assert hex_value in text, f"spine is missing {hex_value}"


def test_spine_states_the_green_text_prohibition():
    text = (SKILLS / SPINE / "SKILL.md").read_text().lower()
    assert "never" in text and "text" in text and "91d46c" in text


def test_doc_template_exists_with_digi_styles():
    from docx import Document  # imported here so the rest of the suite runs without python-docx

    template = ROOT / "assets" / "digi-doc-template.docx"
    assert template.is_file(), "assets/digi-doc-template.docx is missing"
    doc = Document(str(template))
    names = {s.name for s in doc.styles}
    for expected in [
        "Digi Title", "Digi Heading 1", "Digi Heading 2",
        "Digi Body", "Digi Table Header",
    ]:
        assert expected in names, f"template is missing style {expected!r}"


def test_doc_template_uses_source_sans_pro():
    from docx import Document

    doc = Document(str(ROOT / "assets" / "digi-doc-template.docx"))
    assert doc.styles["Normal"].font.name == "Source Sans Pro"
