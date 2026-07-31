---
type: blueprint
genre: Product Change Notice — new product, software
output: docx
---

# PCN — New Product Introduction (software)

Shared grammar, numbering, and the confidentiality banner live in
`pcn-core.md`. Read it first.

Announces a new software product or subscription to the channel. Software PCNs
are rarer than hardware ones and the process is less familiar to the teams
running them, so follow this structure rather than improvising.

Like hardware NPIs, these announce ahead of availability, so a software NPI is
almost always under embargo too.

Differences from the hardware variant: no Key Capabilities list, no Technical
Specifications block. In their place, Product Tiers and Packaging and Commercial
Terms — because what a buyer chooses between is an entitlement level, not a
piece of hardware.

## Section order

### Audience

Per `pcn-core.md`.

### Product Overview

One sentence naming the product and what it does for the end customer, then a
paragraph of context: which platform it attaches to, what problem it solves, and
what it replaces or supplements. Avoid implementation detail — the channel sells
the outcome.

### Key Dates

| NPI PCN | Market Announcement | Commercial Availability |
| --- | --- | --- |
| {{PCN_DATE}} | {{ANNOUNCEMENT_DATE}} | {{AVAILABILITY_DATE}} |

### Product Tiers

What the customer chooses between. One block per tier, each stating the tier
name, who it is for, and what distinguishes it from the tier below:

| {{TIER_1}} | {{TIER_2}} | {{TIER_3}} |
| --- | --- | --- |
| {{WHO_IT_IS_FOR}} — {{WHAT_IS_INCLUDED}} | {{WHO_IT_IS_FOR}} — {{WHAT_IS_INCLUDED}} | {{WHO_IT_IS_FOR}} — {{WHAT_IS_INCLUDED}} |

### Packaging and Commercial Terms

The section hardware PCNs do not have. Cover, explicitly:

- **Unit of sale** — per device, per seat, per site, per token
- **Term** — subscription length and whether it auto-renews
- **Attach requirements** — what the customer must already own
- **Overage or metering** — what happens past the included allowance
- **Trial or promotional terms** — and when they expire

Ambiguity here becomes a support ticket. Be specific.

### Customer Impact and Action Required

**Portfolio Impact** — what this changes for customers already on the platform,
including whether any existing entitlement changes.

**Order Now** — how to quote and order it, and who to contact.

### SKU Table

| Part Number | Description | Region | MSRP |
| --- | --- | --- | --- |
| {{PART_NUMBER}} | {{DESCRIPTION}} | {{REGION}} | {{MSRP}} |

### Authorization

Per `pcn-core.md`.
