# Deck blueprints

Reusable blueprints for the decks Digi actually ships, across every function.
A blueprint is the **content architecture** for one audience: the ordered
slide archetypes, what each slide does, the framing move that makes it land,
the layout, and the voice. The brand chrome comes from `digi-template.pptx`;
these supply the *thinking*. A blueprint produces no `.pptx` on its own — it
tells you what to build, and `digi-pptx` builds it.

When you're asked to build a deck that matches one of these genres, read the
matching blueprint and follow its archetype sequence, swapping in your own
subject. Don't invent a structure from scratch — these are proven.

## Find yours by role

| You are in | You are probably building | Read |
|---|---|---|
| **Sales** | A pitch to a prospect | [customer-facing/sales-pitch.md](customer-facing/sales-pitch.md) |
| **Sales** | A quarterly review with a customer you already have | [customer-facing/customer-qbr.md](customer-facing/customer-qbr.md) |
| **Marketing** | A webinar or a conference session | [customer-facing/webinar.md](customer-facing/webinar.md) |
| **Marketing / Product** | Enablement so Sales, Channel, or Support can carry a launch | [internal/](internal/) — the three enablement blueprints below |
| **Executive / leadership** | A board or senior-leadership review | [internal/leadership-review.md](internal/leadership-review.md) |
| **Executive / people lead** | An all-hands or town hall | [internal/all-hands.md](internal/all-hands.md) |
| **Anyone asking for money or headcount** | A funding request | [internal/business-case.md](internal/business-case.md) |
| **Anyone starting cross-functional work** | A kickoff | [internal/project-kickoff.md](internal/project-kickoff.md) |

## Two families — pick the right one first

Picking the wrong family is the failure mode this structure exists to
prevent, because the two audiences don't just want different content, they
have opposite relationships to Digi:

| Family | Audience | Relationship to Digi | Success looks like |
|---|---|---|---|
| **[internal/](internal/)** | Digi people, or a partner rep who sells on Digi's behalf | Already works here (or works *for* Digi's revenue), has to act on this Monday morning | They can do their job: field the ticket, spot the deal, make the call, own the workstream |
| **[customer-facing/](customer-facing/)** | Someone outside Digi — a prospect, a customer, a webinar attendee | Owes Digi nothing and can walk away at any point | They take the next meeting |

If unsure which: **does the reader already work for (or sell for) Digi, or
are they on the other side of the table?** The first is internal, always, even
if the deck's *subject* is a sale — a channel partner's rep is trained
internally so they can go sell externally. The second is customer-facing.

## internal/ — Digi people who have to act on this

**Launch enablement** — teaching Digi people to sell, position, or support
something new:

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **Support enablement** | CS / support engineers | Field access/config tickets, hold the support boundary | [internal/support-enablement.md](internal/support-enablement.md) |
| **Channel enablement** | Partner sales reps (sell-through) | Spot the deal, pitch from memory, beat competitors | [internal/channel-enablement.md](internal/channel-enablement.md) |
| **Sales enablement** | Direct Digi sellers | Spot it, say it, defend it in front of a customer | [internal/sales-enablement.md](internal/sales-enablement.md) |

If unsure which enablement blueprint: **who is in the seat, and what do they
do Monday morning?** A person fixing a customer's broken thing → support. A
reseller's rep → channel. A Digi quota-carrier → sales.

**Decision and governance** — someone in the room has to decide or fund:

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **Leadership review** | Board members or senior executives | Decide, or know exactly what they're being asked to fund or unblock | [internal/leadership-review.md](internal/leadership-review.md) |
| **Business case** | Budget or headcount owner, plus the finance partner | Fund it, decline it, or say what would make it fundable | [internal/business-case.md](internal/business-case.md) |

**Company and team** — aligning people rather than selling or deciding:

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **All-hands** | A whole company or business unit, every function and level | Know what changed, what it means for them, and what leadership is actually worried about | [internal/all-hands.md](internal/all-hands.md) |
| **Project kickoff** | The cross-functional group about to do the work | Know what they own, what "done" means, and who breaks a tie | [internal/project-kickoff.md](internal/project-kickoff.md) |

## customer-facing/ — persuading someone outside Digi

| Blueprint | Reader | Their job after the deck | Read |
|---|---|---|---|
| **Sales pitch** | A prospect's technical evaluator and economic buyer, together | Take the next meeting (POC, deep-dive, site survey) | [customer-facing/sales-pitch.md](customer-facing/sales-pitch.md) |
| **Customer QBR** | An existing customer's operational owner and executive sponsor | Renew, expand, or say what's in the way | [customer-facing/customer-qbr.md](customer-facing/customer-qbr.md) |
| **Webinar / conference** | A self-selected audience of prospects, customers, and competitors — live and on the recording | Understand something new, and want the follow-up | [customer-facing/webinar.md](customer-facing/webinar.md) |

**Prospect or customer?** That's the split that decides between the first two.
A pitch argues *displacement* — you're trying to unseat whatever they run
today. A QBR is the inverse: you already won, so now *you* are the incumbent
someone else is pitching against, and the argument is demonstrated value.

## Shared spine (all blueprints)

- **Open** with the title slide (`slide1` of the template) and **close** with
  "Thank You" + contact. What goes on the opener differs by family: internal
  decks lead with the subject; customer-facing decks lead with the audience's
  problem, never a Digi overview. See each blueprint.
- **One idea per slide.** Every content slide is a title + a short left column +
  (usually) a visual + an optional bottom callout that states the takeaway.
- **Lead with the takeaway, not the mechanism.** Each slide earns its place by
  answering a question the reader actually has.
- **Name what is still moving.** Pretending everything is settled is how
  Support gets a 2 a.m. call and how a leadership review loses its credibility.
  Flag unknowns explicitly ("confirm with Product Marketing," "behavior at GA:
  confirm") rather than smoothing them over.

## Cross-audience elements (launch-genre decks)

The three enablement blueprints and the customer-facing pitch all need these;
each blueprint says how to slant them. The governance and company blueprints
have their own spines and don't use this list.

- **What it is, in one breath** — the elevator line.
- **How it works** — only the parts that explain the questions that reader asks.
- **Who buys it** + the **discovery questions** that surface the need.
- **Why it wins** — the differentiators (for Digi: peer-to-peer / serial / built-in).
- **How they get it** — packaging: self-managed versus the managed-service offering.
- **Objection handling** — the 3-4 they will actually hear.
- **Where to go / Resources** — job aids, contacts, what is NDA (internal
  only — a customer-facing deck closes on a next step instead).

## Visuals

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
