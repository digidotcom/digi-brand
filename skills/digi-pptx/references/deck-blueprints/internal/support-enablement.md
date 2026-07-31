# Support training blueprint

**Reader:** customer success / support engineers. **Their job after the deck:**
field the tickets this launch will generate, resolve what is theirs, and cleanly
hand off what is not. Abstracted from real Digi support-enablement decks
(including Remote Reach), which share this structure almost slide-for-slide.

**The spine of a support deck is the boundary.** Support does not need to master
the product; they need to know exactly which questions are theirs (access,
config, the commercial/credit conversation) and which belong to product. Build
every slide toward drawing that line.

## Archetype sequence

| # | Slide | Purpose | Layout / visual | Voice |
|---|---|---|---|---|
| 1 | **Title** | Product, "What Support Needs to Know," org, date | template title slide | — |
| 2 | **What X Is** | One-paragraph definition + the one structural fact that drives the tickets (e.g. "a capability of a DRM account, not a separate product") | bullets left + **illustration** (the thing-inside-the-platform) | plain, factual |
| 3 | **How It Works (the parts that explain the questions/failures)** | Only the internals that explain what Support will be asked. Skip the rest. | bullets left + **illustration** (data flow / metering) | "mental model:" framing |
| 4 | **Setting It Up / Enabling in DRM — This Part Is Yours** | The config/access path Support owns, step-checkable | bullets left + **screenshot placeholder** (the real DRM screen) | "this part is yours" |
| 5 | **The Support Boundary** | The load-bearing slide: owns vs does-not-own, and the one-line test | bullets left + **illustration** (the boundary/handoff) | crisp, declarative |
| 6 | **Pre-Flight Checklist / Before You Escalate** | The 3-thing check that resolves most tickets before escalation | numbered list, text (give it room) | imperative |
| 7 | **Common Failures / Questions + First Response** | The actual tickets with the first thing to say/check for each | Q + first-response pairs, text | "like RR, the most common cause is enablement" |
| 8 | **Known Gaps + What's Still Moving** | Honest list of unconfirmed behavior and where to pin it down | text | candid; name the contradiction |
| 9 | **Where to Go** | Job aids, escalation destination, who owns pricing/trial answers | text | directory |
| 10 | **(Appendix) Debug Logging / Support Report** | Optional: how to capture diagnostics for escalation | text + **screenshot placeholder** | reference |
| — | **Thank You** | contact | template closing | — |

Some launches add two product-specific archetypes between 3 and 5 — keep these
when the product has a consumption/commercial model or a sibling it gets
confused with:
- **The Commercial Model** — what Support fields about cost. A customer who
  runs out of quota files a ticket that reads like a bug, not a billing
  question, so Support has to recognize the shape of it before they can route
  it. Cover: how usage is metered (consumption-based, seat-based, etc.), the
  replenishment cadence, whether an unused balance carries over or resets, and
  whether the balance is per-user or shared across the account. Illustration:
  the metering/replenishment flow.
- **X vs Y (disambiguate first)** — when sales/customers conflate two products,
  or two modes of the same product. The slide gives the one question that
  settles it.

## What to swap per product

Product name, the one structural fact (slide 2), the enablement path (slide 4),
the 3-thing pre-flight check (slide 6), the real ticket list (slide 7), and the
known-gaps (slide 8). The boundary slide's *shape* is constant: "Support owns the
access and the commercial conversation; product owns whether the thing is correct."

## Guardrails

- **Draw the boundary explicitly** and repeat it (slides 5 and 7). The miss this
  deck prevents is Support trying to fix product-quality issues.
- **Name every unconfirmed behavior** (slide 8). A support deck that implies
  certainty it does not have is worse than one that says "confirm at GA."
- **Tie to the prior launch's lesson** when there is one ("same as Remote Reach:
  enablement and access nailed down up front, not after the first escalation").

Related: support training is its own launch workstream, never folded into sales
or channel (it has its own reader and its own deck).
