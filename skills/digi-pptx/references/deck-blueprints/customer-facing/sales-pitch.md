# Customer-facing sales pitch blueprint

**Reader:** a prospect's technical evaluator and economic buyer, usually in
the same room. **Their job after the deck:** take the next meeting. This
audience owes Digi nothing, has an incumbent solution already installed, and
can walk away at any point — every slide has to re-earn the right to the next
one.

**The spine of a pitch deck is displacement, not introduction.** Digi is
almost never walking into a greenfield room. There is an incumbent already
installed, already working well enough, and already sunk into the buyer's
budget and their technicians' habits. The deck is not "here is what we do,"
it is "here is why what you have is costing you more than switching would."
Everything serves getting to a next step sized to where this buyer actually
is.

## Archetype sequence

| # | Slide | Purpose | Layout / visual | Voice |
|---|---|---|---|---|
| 1 | **Title** | Customer/topic name, "[Digi solution] for [buyer's environment]," date — no Digi overview | template title | — |
| 2 | **The problem, in their words** | Open on the buyer's status quo pain, not on Digi. Name the operational reality they already live with | short scene text + **illustration** | concrete, their language not ours |
| 3 | **What the status quo is costing** | Quantify it: downtime, truck rolls, exposure, compliance risk. This is the slide that earns the right to talk about Digi next | stat callouts + **illustration** | numbers, not adjectives |
| 4 | **Introducing [Product], in one breath** | The 15-second line, now that the audience has a reason to care | short line + tags + **screenshot placeholder** (product-slide layout 23/24 — fill its picture placeholder) | plain, no jargon |
| 5 | **How it works** | Architecture and data path — enough for the technical evaluator to trust it, not a spec dump | bullets + **illustration** (the path) | precise, "serves the evaluator" |
| 6 | **What it means for the business** | Same capability, translated to uptime, headcount, and total cost — what the economic buyer takes to their own leadership | bullets + stat callout | plain, "serves the economic buyer" |
| 7 | **Proof, not claims** | Deployment scale, reference counts, third-party validation or certifications. Credible because it is specific and checkable, not because it is impressive-sounding | **illustration** or logo/stat band (no named customers in this public repo — see Guardrails) | factual, verifiable |
| 8 | **Why switch from what you have** | Name the incumbent as "what you have today," not a competitor by name. Address switching cost directly instead of pretending it is zero, then show why the total cost of staying still loses | reframe pairs, text | direct, respectful of the incumbent's real strengths |
| 9 | **One platform, not two purchases** | Hardware and software as a single story — the software is what makes the hardware worth the switch, and vice versa. Never split into two line items the buyer could shop separately | **illustration** (stack, not two boxes) | "one system," never "and also" |
| 10 | **Fit for your environment** | Ground it in the buyer's actual vertical (transit, retail, energy and utilities, government) with the specific constraints that vertical cares about | segment bullets + **illustration** | named to their world, not generic |
| 11 | **Objections you're already thinking** | The 3-4 objections this room will actually raise (security, integration effort, switching cost, vendor risk), each with a direct reframe | objection + reframe pairs, text | confident, no defensiveness |
| 12 | **Your next step** | One next step, sized to where this buyer is: a proof of concept, a technical deep-dive, or a site survey — never a generic "Questions?" slide. If the next step is a POC, hand them the shape of it | single clear ask, text | "here is exactly what happens next" |
| — | **Thank You** | contact | template closing | — |

## Two audiences, one room

Name where each is served rather than writing one generic deck and hoping it
lands for both:
- **Technical evaluator** — served directly by slides 5 (how it works), 7
  (proof), and 9 (platform architecture). This reader is silently deciding
  whether the thing works; give them enough substance that they don't have to
  ask.
- **Economic buyer** — served directly by slides 3 (cost of status quo), 6
  (business translation), and 8 (switch vs. stay economics). This reader is
  deciding whether it pays; give them a number, not a feature.
- A deck that only serves one loses the other's vote. If a slide seems to
  serve neither, cut it.

## What to swap per opportunity

The problem scene and cost quantification (slides 2-3), the one-breath line
and tags (slide 4), the architecture detail level (slide 5), the business
translation numbers (slide 6), the proof points available for this buyer
(slide 7), the specific incumbent-switching argument (slide 8), the vertical
grounding (slide 10), the objections this buyer will actually raise (slide
11), and the sized next step (slide 12). The displacement spine and the
two-audience service pattern are constant.

## Meeting length and what to cut

Default is the full 12-slide sequence for a first substantive meeting
(30-45 minutes). When the meeting is shorter, cut in this order — each cut
degrades the deck gracefully rather than breaking it:
1. **Cut slide 10 (fit for your environment) first** — fold one vertical
   detail into slide 6 instead of giving it a dedicated slide.
2. **Cut slide 9 (one platform)** next if the audience already buys Digi
   hardware and software together — state it as a line in slide 6 instead.
3. **Merge slides 2 and 3** into one problem-and-cost slide for a 15-minute
   intro meeting.
4. **Never cut slides 7, 8, 11, or 12.** Proof, the displacement argument,
   objection handling, and the close are what turn a meeting into a next
   meeting — everything else is in service of getting the room to trust
   those four.

## Layout notes

Same template mechanics as the internal blueprints (`2024-Digi-Public-PPT-Template.potx`,
zones from [../../visuals.md](../../visuals.md)): title + short left column +
one visual per slide, callout band for the takeaway. Two differences from the
internal decks:
- **Slide 1 carries no Digi company-overview content.** If a template slide
  variant exists for "about Digi," skip it here — that content, if needed at
  all, belongs after slide 7 (proof), never before slide 2 (their problem).
- **Proof slides (7) favor a stat band or logo-wall layout** (`full-band` or
  `hero` zone) over bullets — the visual weight should read as evidence, not
  as another claim in a list.

## Voice

Persuasive, not evangelical: state the cost of the status quo and the result
of switching in plain numbers and let them carry the argument. No hype
adjectives standing in for proof. Same brand voice rules as every blueprint
(plain, professional, no dashes) — see
[../README.md](../README.md#voice) — with one addition specific to this
audience: **never disparage the incumbent.** Name what it costs to keep, not
what is wrong with it; a room with a technical evaluator who respects their
current vendor will tune out a cheap shot.

## Guardrails — this repo is public

- **No customer names, logos, or identifying deployment details.** Proof
  points (slide 7) use shapes like "deployed across thousands of sites in
  [vertical]" or "independently certified to [standard]," filled in by the
  user with their own real, specific evidence — never a placeholder that
  reads as an actual account.
- **No prices, discounts, or part numbers anywhere in the deck**, including
  in the platform slide (9) and the next-step slide (12). Commercial terms
  are a follow-up conversation, not a pitch-deck line.
- **No channel program tier names.** This blueprint is for a direct or
  partner-led customer conversation, not a partner-training deck — if
  channel mechanics come up, that is the [internal/channel-enablement.md](../internal/channel-enablement.md)
  genre, not this one.
- **No unreleased product names or roadmap promises.** Pitch what ships
  today; a future capability promised in a sales deck becomes a commitment
  the buyer holds Digi to.
- **No win rates, and no named competitors in a disparaging frame.** Slide 8
  addresses "the incumbent" or "what you have today" by category and by
  cost, never by vendor name — the moment the deck names a real competitor,
  it stops being reusable across every deal this blueprint is meant to serve.

## Where the close goes next

When slide 12's next step is a proof of concept, hand the buyer the actual
shape of it instead of a vague promise: use
`${CLAUDE_PLUGIN_ROOT}/document-types/poc-test-plan.md` to write the
objective and success criteria for that POC. It is the natural next artifact
after a pitch that lands, because it makes the same "success and failure
defined in advance" move for the POC that this deck just made for the
meeting.
