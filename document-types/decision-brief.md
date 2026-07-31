---
type: blueprint
genre: Decision brief
output: markdown
---

# Decision Brief

A brief exists so a busy reader can act without reading all of it. That is the
entire design constraint, and it produces two rules: the punchline goes first,
and every section is written for a named reader.

This is not the generic executive one-pager. It carries two moves that generic
templates omit and that Digi work requires: **audience-segmented disclosure**
and **explicit internal markers**.

Use it for a recommendation to leadership, a coverage handoff, an incident
readout, or a pre-meeting profile. The spine is the same; the middle sections
change with the subject.

## Section order

### One-line summary

The first thing on the page, before any context. One sentence stating the
situation and the ask. If the reader stops here, they should still know what you
want from them.

Label it `One-line summary`, `TL;DR`, or `Punchline` — pick one and use it
consistently. It is a heading, not a preamble.

For an incident brief, this is what broke and whether it is fixed. For a
recommendation, it is what you recommend and what decision you need.

### Recommendation

What you think should happen, stated as a decision someone can approve or
reject. Not "we should consider" — "we should do {{ACTION}} by {{DATE}}."

If you are not recommending anything, say what the brief is for instead. A brief
without an ask should say so in its first line rather than leaving the reader
hunting for one.

### Context

Only what the reader needs to evaluate the recommendation. Assume they share the
background they actually share — do not narrate your reasoning to people who
already have the context. Cut every qualifier that exists to show your work.

### Options

Where a real choice exists. One block per option:

**Option {{N}}: {{NAME}}**
- **What it is:** one sentence
- **Cost:** time, money, or opportunity
- **Risk:** what could go wrong
- **Why not chosen** — or, for the recommended option, why chosen

Two or three options. A single option is a recommendation, not a choice, and
padding it with straw alternatives insults the reader.

### Risks

What could still go wrong, and what would signal it early. Each risk gets a
severity and an owner. State risks you have not mitigated — a brief that lists
only solved problems is not trusted twice.

| Risk | Severity | Early signal | Owner |
| --- | --- | --- | --- |
| {{RISK}} | {{SEVERITY}} | {{SIGNAL}} | {{OWNER}} |

### Audience-segmented disclosure

**The move that makes this blueprint Digi-specific.** When a situation touches
more than one audience, do not write one message and let readers sort out what
applies to them. Write a section per audience, named:

**What we tell {{EXTERNAL_AUDIENCE}}**
The customer-safe account. Accurate, complete for their purposes, and free of
internal detail they have no need for and no context to interpret.

**What we tell {{INTERNAL_AUDIENCE}}**
The internal account. Root cause, what we got wrong, what it cost.

Segmenting explicitly is what prevents an internal detail from reaching a
customer in a forwarded email. The boundary is a section heading, not a habit.

### INTERNAL ONLY sections

Mark any section that must not leave the company, at the section level, in the
heading itself:

```
## {{SECTION_TITLE}} (INTERNAL ONLY — do not disclose to customers)
```

Use it for: model and vendor detail, margin and cost structure, root causes that
imply fault, unreleased roadmap, and anything about a named customer's
environment.

The marker goes in the heading rather than a footnote because briefs get
excerpted. A heading survives a copy-paste; a footer does not.

### Disambiguation

Include when the subject is routinely confused with something else — two
products with similar names, a codename and its shipping name, a feature and the
platform it runs on.

**{{THING_A}} vs {{THING_B}}** — one paragraph stating what each is and the
single distinction that matters. Cheaper here than in the meeting.

### Owners

Who owns what, by name. A brief that names no owners produces no action.

| Area | Owner |
| --- | --- |
| {{AREA}} | {{NAME}} |

### Open actions

What is outstanding, who has it, and by when. Distinguish blocked from
in-progress — "blocked on {{WHO}}" is different information from "in progress"
and the reader may be the unblocker.

| Action | Owner | Due | Status |
| --- | --- | --- | --- |
| {{ACTION}} | {{OWNER}} | {{DATE}} | {{STATUS}} |

### Source material

Where the underlying material lives, when the brief summarizes a body of work.
A path or a link, so the reader can go deeper without asking.
