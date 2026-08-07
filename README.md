# digi-brand

Digi International's brand, applied to the things people actually make — decks,
documents, and the recurring notices the channel depends on.

Companion to [pm-tools](https://github.com/digidotcom/pm-tools), which covers the
PRD pipeline. This one is for everyone, not only product managers.

## Install

### Claude Code (CLI or desktop app)

```
claude plugin marketplace add digidotcom/digi-brand
claude plugin install digi-brand@digi-brand
```

Update later with `claude plugin update digi-brand`.

### Codex CLI, Cursor, Gemini CLI, and other harnesses

The folders in `skills/` are standard [Agent Skills](https://agentskills.io)
(`SKILL.md` directories), the open format read by 30+ tools. Copy a skill folder
into your tool's skills directory. Each carries an inline fallback palette, so a
skill works on its own without the rest of the plugin.

## The skills

- **digi-brand-guidelines** — the brand spine. Palette, typography, logo rules,
  the role map, and a WCAG contrast table. Every value is extracted from the
  official masters' theme XML rather than transcribed, so it cannot drift.
  Every other skill reads this one.
- **digi-pptx** — Digi presentations built on the two official 2024 masters,
  chosen by classification (Public for external audiences, Confidential for
  internal — Confidential when unclear). The slide master supplies the green
  bar, logo, classification footer, fonts, and correct geometry.
  Includes blueprints for the recurring launch-training genre (support, channel,
  sales) and a generator for on-brand graphics (requires a `GEMINI_API_KEY`
  environment variable).
- **digi-docx** — Digi Word documents, plus the document blueprints below.

## Document blueprints

In `document-types/`. They define structure, not format — a PCN renders to Word
because the channel expects Word; a brief renders wherever its reader is.

- **Product Change Notices** — `pcn-core` holds the shared grammar and
  numbering; `pcn-npi-hardware`, `pcn-npi-software`, `pcn-eol`, and
  `pcn-price-change` carry the four flavors. Structures derived from real Digi
  notices.
- **poc-test-plan** — defines success before the equipment is powered on.
- **decision-brief** — punchline first, audience-segmented disclosure, explicit
  internal markers.

## What is deliberately not here

Sales agreements and statements of work — legal instruments, owned by legal, and
not appropriate for a public repo. Release notes, support KB articles, and
security advisories — each already has an owner and a platform at Digi; a
blueprint would be a second, worse copy. Product datasheets — marketing owns
that template. PRDs and positioning documents — already in `pm-tools`.

## Contributing

The test suite is a guard, not a formality. It fails the build if any file
contains a price, a real part number, a channel tier name, a credential-shaped
string, or a color outside the official palette. Run it before you push:

```
pip install pytest python-docx
python3 -m pytest tests/ -v
```

The currency check is deliberately strict — it matches any dollar figure, not
only Digi's, because a regex cannot tell the difference and the expensive
mistake is one-directional. Write non-Digi costs in words ("roughly 6.5 cents
per image") rather than symbols. Never loosen a pattern to make a legitimate
figure pass.

To change a brand value, edit `skills/digi-brand-guidelines/SKILL.md` first,
then the inline fallbacks. `tests/test_palette.py` fails if any file disagrees
with the template's theme XML.

## Maintainers

Owner: Josh Flinn (joshua.flinn@digi.com). Edit in place, bump `version` in
`.claude-plugin/plugin.json` (CalVer `YYYY.MM.DD-N`), validate with
`claude plugin validate .`, run the tests, commit. Installed copies pick up
changes via `claude plugin update digi-brand`.
