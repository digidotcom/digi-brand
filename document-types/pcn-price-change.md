---
type: blueprint
genre: Product Change Notice — price change
output: docx
---

# PCN — Price Change

Shared grammar and numbering live in `pcn-core.md`. Read it first.

Notifies the channel that pricing is changing. Its two distinctive sections —
Timing of Change and the FAQ — exist to answer the two questions partners
always ask: what happens to my backlog, and what happens to my open quotes.
Answer them in the document or answer them on the phone.

A price change is normally communicated openly to the affected channel, so it
is usually not embargoed — but apply the confidentiality banner from
`pcn-core.md` if the change accompanies an unannounced product.

There is no Authorization block on a price change.

## Section order

### PCN Date

`{{PCN_DATE}}` — when the notice is issued.

### Effective Date

`{{EFFECTIVE_DATE}}` — when the new pricing takes effect. Give the channel a
standard notice window between the two.

### Products Affected

The product families in scope, as a single line:
`{{FAMILY_1}} | {{FAMILY_2}} | {{FAMILY_3}} | Accessories`

### Audience

Per `pcn-core.md`. **This determines which pricing may appear** — see below.

### Description of Change

One or two paragraphs. State the rationale before the numbers. A price change
with a stated reason reads as program management; one without reads as a
squeeze.

Close with a line directing readers to their account manager for questions about
open quotes or in-flight opportunities.

### Updated Pricing

**The price type varies by notice.** Sometimes it is distributor pricing,
sometimes it is MSRP. Do not assume either — pick the one that matches the
audience, and use its table form. Getting this wrong sends distributor economics
to the wrong readers.

**Distributor form.** Rows are SKUs, columns are channel tiers, grouped by
product category. Use tier placeholders unless the program tier names are
confirmed publishable:

| SKU | {{TIER_1}} | {{TIER_2}} | {{TIER_3}} |
| --- | --- | --- | --- |
| {{PART_NUMBER}} | {{PRICE}} | {{PRICE}} | {{PRICE}} |

State the quantity break and currency above the tables, e.g.
`All prices in {{CURRENCY}} at Qty {{QTY_BREAK}}.`

**MSRP form.** No tier columns. One row per SKU with the old and new price so
the delta is visible:

| Part Number | Description | Region | Current MSRP | New MSRP |
| --- | --- | --- | --- | --- |
| {{PART_NUMBER}} | {{DESCRIPTION}} | {{REGION}} | {{CURRENT_MSRP}} | {{NEW_MSRP}} |

Group by product category when the list runs long. Categories follow the
portfolio, e.g. Routers, Gateways, Extenders, Accessories.

### Timing of Change

Three labeled rows. This is the section that prevents escalations:

| Go-Live Date | {{EFFECTIVE_DATE}} — new pricing reflected in all Digi systems and price lists |
| --- | --- |
| Backlog Orders | {{BACKLOG_POLICY}} |
| Active Quotes | {{QUOTE_VALIDITY_POLICY}} |

Standard policies, adapt as the change requires:

- **Backlog** — Digi honors the pricing in effect at the time of order
  confirmation for orders placed before the effective date.
- **Active quotes** — quotes remain valid for their stated validity period from
  the date of issue.

### Frequently Asked Questions

Three questions minimum, answered plainly:

**What happens to my open quotes?**
State the validity period and who to contact about repricing.

**What about orders already in my backlog?**
State the honoring policy and who to contact about a specific order.

**Who should I contact with additional questions?**
Name the role, not a person — account manager or channel support.

Add a fourth question when the change has an unusual wrinkle, such as a mid-term
subscription or a regional carve-out.
