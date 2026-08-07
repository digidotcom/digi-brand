# Customer quarterly business review blueprint

**Reader:** an existing customer's operational owner and their executive
sponsor. **Their job after the deck:** renew, expand, or tell you what is in
the way. This audience already bought and already deployed — the deck is not
earning a first yes, it is protecting one that was already given.

**The spine of a QBR is that you already won this customer, so the deck is
about proving the decision was right and finding the next one.** This is the
inverse of [sales-pitch.md](sales-pitch.md): there is no displacement
argument here, because Digi is no longer the challenger. Digi is now the
incumbent someone else is quietly pitching against. The failure mode this
blueprint exists to prevent is a status update that surfaces no problems —
a deck of green checkmarks lets a dissatisfied customer stay silent until
the day they don't renew, which is the one outcome a QBR is supposed to
catch early.

## Archetype sequence

| # | Slide | Purpose | Layout / visual | Voice |
|---|---|---|---|---|
| 1 | **Title** | Customer name, "Quarterly Business Review," period covered, date — no Digi overview | template title | — |
| 2 | **This quarter, in your numbers** | Open with outcomes in the customer's own metrics: uptime, sites deployed, incidents avoided, hours saved | stat callouts, text | their numbers, not our activity |
| 3 | **Where we did not deliver** | Every open issue, missed commitment, and unresolved escalation, each with an owner and a date | issue + owner + date table, text | direct, no minimizing language |
| 4 | **Usage and adoption** | How the deployed capability is actually being used day to day, not just that it was installed | stat callouts + **illustration** | factual, "here's what's actually running" |
| 5 | **Support and reliability** | Tickets closed, resolution time, health trend over the quarter | stat callouts, text | factual, verifiable |
| 6 | **Risk and roadmap exposure** | End-of-life dates, firmware currency, security posture — what needs attention before it becomes an incident | bullets + **illustration** | plain, names the risk without alarm |
| 7 | **Value realized** | What the deployment is worth against what it costs, in the sponsor's terms | stat callout, text | plain numbers, no adjectives |
| 8 | **What's changing next quarter** | The plan for every open item from slide 3: what happens, by when, who owns it | action list, text | "here's what we're doing about it" |
| 9 | **A capability you're not using yet** | Introduce one new capability, only after the value slides have landed — see cross-reference below | short line + **screenshot placeholder** | plain, no pitch energy |
| 10 | **What that would mean for you** | The new capability translated into this customer's outcomes, same as slide 2's frame | bullets + stat callout | same numbers language as slide 2 |
| 11 | **Commitments, both directions** | What Digi will do by when, and what the customer owes to unblock it | two-column action list, text | "here's what each of us owes the other" |
| 12 | **Open discussion** | Space for the questions this deck did not anticipate | prompt, text | "what did we miss" |
| — | **Thank You** | contact | template closing | — |

## Two readers, one review

Name where each is served rather than writing one generic update and hoping
it lands for both:
- **Operational owner** — served directly by slides 3 (open issues), 4
  (usage), 5 (support), and 8 (the fix plan). This reader wants tickets
  closed and a straight answer on what happens next.
- **Executive sponsor** — served directly by slides 2 (outcomes), 6 (risk),
  7 (value realized), and 9-10 (expansion). This reader wants to know the
  spend was justified and what risk they're still carrying.
- Slide 11 closes for both — it is the one slide where operator-level
  follow-through and sponsor-level commitment sit on the same page.

## What to swap per account

The outcome numbers (slide 2), the open issues and their owners (slide 3),
the usage detail (slide 4), the support metrics (slide 5), the risk items
(slide 6), the value calculation (slide 7), the remediation plan (slide 8),
the new capability and its translation (slides 9-10), and the two-way
commitment list (slide 11). The value-before-expansion ordering and the
two-reader service pattern are constant.

## Cadence and what to cut

Default is the full 12-slide sequence for a quarterly review (45 minutes).
For a shorter mid-quarter check-in (20 minutes) or an account with no
open issues to escalate, cut in this order:
1. **Cut slides 9-10 (new capability) first** if there is nothing genuinely
   new to introduce this cycle — a filler expansion slide with no real
   capability behind it reads as a sales reflex, not an update.
2. **Merge slides 4 and 5** into one operations slide when usage and support
   data are both light.
3. **Merge slides 6 and 7** into one risk-and-value slide for a sponsor-only
   check-in with no operator in the room.
4. **Never cut slides 2, 3, 8, or 11.** Outcomes, problems named up front,
   the fix plan, and the two-way commitment list are what make this a review
   instead of a status email — everything else is supporting detail.

## Layout notes

Same template mechanics as the other blueprints (`2024-Digi-Public-PPT-Template.potx`, zones
from [../../visuals.md](../../visuals.md)): title + short left column + one
visual per slide, callout band for the takeaway. One difference from
`sales-pitch.md`: **slide 3 (where we did not deliver) is a table, not a
bullet list** — an issue, its owner, and its date read as three columns a
customer can hold Digi to, where a bullet list reads as prose that can be
walked back later.

## Voice

Direct and unhedged, especially on slide 3 — a QBR that softens its own
problems with passive language ("some delays were experienced") reads as
evasive to a customer who already knows about the delay. State what
happened, who owns the fix, and when. Slides 2 and 7 stay in plain numbers,
no adjectives standing in for proof. Same brand voice rules as every
blueprint (plain, professional, no dashes) — see
[../README.md](../README.md#voice) — with one addition specific to this
audience: **never open with the new pitch.** Slides 9-10 exist only after
slides 2 through 8 have made the case; a QBR that opens with new products
reads as a sales call wearing a status-update disguise, and it burns the
goodwill the meeting exists to build.

## Guardrails — this repo is public

- **No real Digi customer names, logos, or account-identifying detail** in
  this blueprint's own example language — use `[Customer]` or
  `[Sponsor Name]` placeholders. The actual deck this blueprint produces
  will of course name the real customer on slide 1; the guardrail is on the
  reusable blueprint document, not on the deck it generates.
- **No prices, discounts, or part numbers.** Slide 7's value calculation
  describes the shape of the ROI story (uptime recovered, truck rolls
  avoided, hours saved) without a real dollar figure or SKU.
- **No channel program tier names.**
- **No unreleased product names or roadmap promises on slides 9-10.** A
  capability promised inside a QBR is the single most binding promise Digi
  makes all quarter — this is a customer already relying on Digi in
  production, and an unshipped feature named here becomes an expectation
  the account team is held to at the next review.

## Introducing something new inside a QBR

Slide 9's "a capability you're not using yet" is the one place this
blueprint and [sales-pitch.md](sales-pitch.md) do the same job for different
readers: sales-pitch.md's slide 4 ("Introducing [Product], in one breath")
is the pattern for stating a new capability in one line, no jargon, before
going deeper. Use that same one-breath framing here — the difference is
audience, not technique: sales-pitch.md is introducing Digi itself to a
stranger, this slide is introducing one new capability to someone who
already trusts Digi enough to be worth the pitch.
