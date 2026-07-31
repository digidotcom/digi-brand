---
name: digi-docx
description: Create Digi International branded Word documents, and write the recurring Digi document genres from proven blueprints. Applies Digi's brand styling — Source Sans Pro, navy headings, the official palette — over the standard docx tooling, and carries structural blueprints for Product Change Notices (new product hardware and software, end of life, price change), POC test plans, and decision briefs. Use whenever creating a .docx for Digi, or when writing a PCN, a POC test plan, or a decision brief in any format. Trigger on "write a PCN", "product change notice", "EOL notice", "price change notification", "POC test plan", "decision brief", "Digi Word doc", or any .docx work in a Digi context.
license: MIT
---

# Digi Word Documents

> **Brand values.** Read
> `${CLAUDE_PLUGIN_ROOT}/skills/digi-brand-guidelines/SKILL.md` for the palette,
> type stack, and accessibility rules. If it is not readable, use this fallback:
> navy `#1B4965`, white `#FFFFFF`, dark gray `#3F4245`, light gray `#F5F7F7`,
> green `#91D46C` (fills only, never text), silver `#DAD8D8`, teal `#1F7FA5`,
> orange `#CC6033`, ice blue `#E2F6FF`, medium gray `#56565A`, followed-link
> blue `#00B7FF`. Fonts: Source Sans Pro, falling back to Source Sans 3 or Arial.

This skill is a brand and structure layer. It does not reimplement Word
manipulation — use the standard `docx` skill for reading, editing, and writing
`.docx` files, and apply what follows on top.

## Two jobs

**1. Make a Digi-looking document.** Start from
`${CLAUDE_PLUGIN_ROOT}/assets/digi-doc-template.docx`, which carries the named
styles. Do not hand-format.

| Style | Use |
| --- | --- |
| `Digi Title` | Document title, once |
| `Digi Heading 1` | Top-level sections |
| `Digi Heading 2` | Subsections |
| `Digi Body` | Body text |
| `Digi Table Header` | Table header row, on a teal `#1F7FA5` fill |

Table convention: header row in `Digi Table Header` on teal, alternating body
rows on ice blue `#E2F6FF`, borders in silver `#DAD8D8`.

Regenerate the template by running `python3 tools/build_doc_template.py` from
a clone of this repo if styles need to change. Edit the builder, not the
binary. Regenerating always produces
a byte-different file even with no style change, so verify a regenerated
template by reading its styles back, not by comparing it byte-for-byte against
the committed copy.

**2. Write a known Digi document genre.** When the request matches a genre
below, read its blueprint before drafting. The blueprints encode structure
derived from real Digi documents — following one is faster and more correct than
improvising, and the section order is what the audience expects.

| Ask | Blueprint |
| --- | --- |
| New hardware product to the channel | `${CLAUDE_PLUGIN_ROOT}/document-types/pcn-npi-hardware.md` |
| New software product or subscription | `${CLAUDE_PLUGIN_ROOT}/document-types/pcn-npi-software.md` |
| Discontinuing a product | `${CLAUDE_PLUGIN_ROOT}/document-types/pcn-eol.md` |
| Changing prices | `${CLAUDE_PLUGIN_ROOT}/document-types/pcn-price-change.md` |
| Any PCN — shared grammar and numbering | `${CLAUDE_PLUGIN_ROOT}/document-types/pcn-core.md` |
| Proof-of-concept test plan | `${CLAUDE_PLUGIN_ROOT}/document-types/poc-test-plan.md` |
| Recommendation, handoff, or incident readout | `${CLAUDE_PLUGIN_ROOT}/document-types/decision-brief.md` |

Blueprints define structure, not format. A PCN renders to `.docx` because the
channel expects Word. A decision brief renders wherever its reader is — markdown
is usually right. Each blueprint declares its natural output in frontmatter.

## Rules

- **Never invent a price, part number, or date.** Leave the author's placeholder
  in place and say what is missing. A plausible-looking wrong SKU in a channel
  notice is worse than a visible gap.
- **Check the audience before including pricing.** Distributor pricing goes only
  to distributor audiences. The audience line is not decoration.
- **Never ship an embargo banner with a real date** unless the author supplied
  it and the embargo is real.
- Plain, professional register. No exclamation marks in channel-facing material.
- Green `#91D46C` is a fill. Never set text in it.

## QA checklist

Before declaring a document done:

- [ ] Built from `digi-doc-template.docx`, not hand-formatted
- [ ] Every paragraph uses a `Digi *` style
- [ ] Source Sans Pro throughout
- [ ] Headings navy `#1B4965`, body dark gray `#3F4245`
- [ ] No green text anywhere
- [ ] If it is a known genre, the blueprint's section order is followed
- [ ] Every placeholder either filled or visibly flagged to the author
- [ ] Pricing matches what the stated audience is entitled to see
- [ ] No embargo banner unless a real embargo applies
