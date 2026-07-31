# Deck blueprints

Reusable blueprints for recurring Digi deck genres, abstracted from real decks
shipped for Digi product launches. A blueprint is the **content architecture**
for one audience: the ordered slide archetypes, what each slide does, the
framing move that makes it land, the layout, and the voice. The brand chrome
comes from `digi-template.pptx`; these supply the *thinking*. A blueprint
produces no `.pptx` on its own — it tells you what to build, and `digi-pptx`
builds it.

When you're asked to build a deck that matches one of these genres, read the
matching blueprint and follow its archetype sequence, swapping in the new
product or deal. Don't invent a structure from scratch — these are proven.

## Two families — pick the right one first

Picking the wrong family is the failure mode this structure exists to
prevent, because the two audiences don't just want different content, they
have opposite relationships to Digi:

| Family | Audience | Relationship to Digi | Success looks like |
|---|---|---|---|
| **[internal/](internal/)** | Digi people, or a partner rep who sells on Digi's behalf | Already works here (or works *for* Digi's revenue), has to act on this Monday morning | They can do their job on day one: field the ticket, spot the deal, defend the pitch |
| **[customer-facing/](customer-facing/)** | Someone outside Digi — a prospect, an evaluator, a buyer | Owes Digi nothing and can walk away at any point | They take the next meeting |

If unsure which: **does the reader already work for (or sell for) Digi, or
are they the one being sold to?** The first is internal, always, even if the
deck's *subject* is a sale — a channel partner's rep is trained internally so
they can go sell externally. The second is customer-facing.

## internal/ — teaching Digi people to sell, position, or support something new

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **Support** | CS / support engineers | Field access/config tickets, hold the support boundary | [internal/support-enablement.md](internal/support-enablement.md) |
| **Channel** | Partner sales reps (sell-through) | Spot the deal, pitch from memory, beat competitors | [internal/channel-enablement.md](internal/channel-enablement.md) |
| **Sales** | Direct Digi sellers | Spot it, say it, defend it in front of a customer | [internal/sales-enablement.md](internal/sales-enablement.md) |

If unsure which internal blueprint: **who is in the seat, and what do they do
Monday morning?** A person fixing a customer's broken thing → support. A
reseller's rep → channel. A Digi quota-carrier → sales.

## customer-facing/ — persuading someone outside Digi

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **Sales pitch** | A prospect's technical evaluator and economic buyer, together | Take the next meeting (POC, deep-dive, site survey) | [customer-facing/sales-pitch.md](customer-facing/sales-pitch.md) |

## Shared spine (all blueprints)

- **Open** with the title slide (`slide1` of the template): product, audience,
  org, month, GA date (internal) — or the buyer's problem (customer-facing;
  see that blueprint's guardrails). **Close** with "Thank You" + contact.
- **One idea per slide.** Every content slide is a title + a short left column +
  (usually) a visual + an optional bottom callout that states the takeaway.
- **Lead with the takeaway, not the mechanism.** Each slide earns its place by
  answering a question the reader actually has.
- **Name what is still moving.** These are launch decks; pretending everything is
  finalized is how Support gets a 2 a.m. call. Flag unknowns explicitly
  ("confirm with Product Marketing," "behavior at GA: confirm").

## Cross-audience elements (emphasis differs)

Most decks need these regardless of audience; each blueprint says how to slant
them:
- **What it is, in one breath** — the elevator line.
- **How it works** — only the parts that explain the questions that reader asks.
- **Who buys it** + the **discovery questions** that surface the need.
- **Why it wins** — the differentiators (for Digi: peer-to-peer / serial / built-in).
- **How they get it** — packaging: self-managed versus the managed-service offering.
- **Objection handling** — the 3-4 they will actually hear.
- **Where to go / Resources** — job aids, contacts, what is NDA (internal
  only — a customer-facing deck closes on a next step instead).

## Visuals (use the new capability)

Apply the decision rule in [../visuals.md](../visuals.md) per slide:
- Concept/architecture/relationship slide → **generate an illustration**
  (`gen_graphic.py`, default soft-3D style).
- A real UI the reader will see (a DRM screen, the endpoint dashboard) →
  **screenshot placeholder**.
- A talk-track, checklist, or "say this not that" → **keep as text**, but use the
  left-column + callout layout so it is not a wall.
Each blueprint marks the natural visual per archetype.

## Voice

Follow the brand voice section in
`${CLAUDE_PLUGIN_ROOT}/skills/digi-brand-guidelines/SKILL.md` (plain,
professional, **no dashes**, no codenames in anything customer-adjacent).
Per-audience register notes are in each blueprint. The example lines in these
blueprints are written dash-free on purpose — match them.
