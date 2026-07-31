import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "document-types"

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

REQUIRED_SECTIONS = {
    "pcn-core.md": ["Numbering", "Audience", "Shared elements"],
    "pcn-npi-hardware.md": [
        "Audience", "Product Overview", "Key Capabilities", "Key Dates",
        "Product Variants", "Technical Specifications",
        "Customer Impact and Action Required", "SKU Table", "Authorization",
    ],
    "pcn-npi-software.md": [
        "Audience", "Product Overview", "Key Dates", "Product Tiers",
        "Packaging and Commercial Terms",
        "Customer Impact and Action Required", "SKU Table", "Authorization",
    ],
    "pcn-eol.md": [
        "Audience", "Product Notice", "Replacement Mapping",
        "Timing of Change", "EOL Terms and Conditions", "Action Required",
        "Authorization",
    ],
    "pcn-price-change.md": [
        "PCN Date", "Effective Date", "Products Affected", "Audience",
        "Description of Change", "Updated Pricing", "Timing of Change",
        "Frequently Asked Questions",
    ],
    "poc-test-plan.md": [
        "Objective", "Success Criteria", "Scope", "Environment",
        "Test Cases", "Schedule", "Roles", "Exit Criteria",
    ],
    "decision-brief.md": [
        "One-line summary", "Recommendation", "Options", "Risks",
        "Audience-segmented disclosure", "Owners", "Open actions",
    ],
}


def blueprint_files():
    return sorted(DOCS.glob("*.md"))


def test_every_blueprint_has_frontmatter_with_genre_and_output():
    for path in blueprint_files():
        match = FRONTMATTER.match(path.read_text())
        assert match, f"{path.name}: no frontmatter"
        block = match.group(1)
        assert re.search(r"^type:\s*blueprint\s*$", block, re.M), f"{path.name}: type"
        assert re.search(r"^genre:\s*\S", block, re.M), f"{path.name}: genre"
        assert re.search(r"^output:\s*\S", block, re.M), f"{path.name}: output"


def test_required_sections_present():
    for name, sections in REQUIRED_SECTIONS.items():
        text = (DOCS / name).read_text()
        for section in sections:
            assert section in text, f"{name}: missing section {section!r}"


def test_price_change_covers_both_pricing_forms():
    text = (DOCS / "pcn-price-change.md").read_text().lower()
    assert "distributor" in text, "must describe the distributor pricing form"
    assert "msrp" in text, "must describe the MSRP form"
    assert "tier" in text, "must explain when tier columns apply"


def test_blueprints_use_placeholders_not_real_values():
    for path in blueprint_files():
        text = path.read_text()
        if "|" in text and "SKU" in text:
            assert "{{" in text, f"{path.name}: table without placeholders"


def test_pcn_variants_reference_the_core():
    for name in ["pcn-npi-hardware.md", "pcn-npi-software.md",
                 "pcn-eol.md", "pcn-price-change.md"]:
        assert "pcn-core.md" in (DOCS / name).read_text(), f"{name}: no core reference"


def test_decision_brief_leads_with_the_punchline():
    text = (DOCS / "decision-brief.md").read_text()
    summary_at = text.index("One-line summary")
    for later in ["Options", "Risks", "Owners"]:
        assert summary_at < text.index(later), (
            f"'One-line summary' must come before {later!r}"
        )


def test_decision_brief_covers_internal_markers():
    text = (DOCS / "decision-brief.md").read_text().upper()
    assert "INTERNAL ONLY" in text
