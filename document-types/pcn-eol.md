---
type: blueprint
genre: Product Change Notice — end of life
output: docx
---

# PCN — End of Life

Shared grammar and numbering live in `pcn-core.md`. Read it first.

Structurally its own document. It shares only Audience, Action Required, and
Authorization with the new-product variants. There is no product overview, no
capability list, and no specification table — the reader already owns the
product. What they need is: what is going away, what replaces it, how long they
have, and what to do.

An EOL notice is usually not embargoed.

## Section order

### Header block

| Product End of Life Notification | Date: {{PCN_DATE}} |
| --- | --- |
| Product: {{PART_NUMBER}} | |

### Audience

Per `pcn-core.md`. EOL notices often extend beyond the channel to end customers.

### Product Notice

The core paragraph. State, in this order:

1. That Digi is discontinuing the product, named by part number.
2. Whether a qualified replacement exists, and what it is.
3. Whether the change is transparent to end customers — that is, whether any
   design, configuration, or integration work is required.
4. What to order going forward.
5. What happens to existing inventory.
6. Who to contact.

Be explicit about "no action required" when that is true. It is the single most
useful sentence in the document.

### Replacement Mapping

| EOL Part Number | Recommended Replacement | Replacement Type |
| --- | --- | --- |
| {{PART_NUMBER}} | {{REPLACEMENT_PART_NUMBER}} | {{REPLACEMENT_TYPE}} |

`Replacement Type` is a controlled value. Use:

- **Drop-in** — electrically and mechanically identical; no change of any kind.
- **Functional** — equivalent function, may differ physically or electrically in
  ways that do not affect the documented use case.
- **Alternative** — closest available product; the customer must evaluate fit.
- **None** — no replacement exists.

This column is the one the reader acts on. Choose it carefully; "Functional"
where the truth is "Alternative" generates a field failure.

### Timing of Change

| Timing of Change | {{LTB_LTS_TERMS}} |
| --- | --- |

State the Last-Time-Buy and Last-Time-Ship windows with dates. **When no LTB or
LTS window is offered, say so explicitly** — silence reads as an oversight and
generates escalations.

### EOL Terms and Conditions

A short bulleted list of the operative facts:

- {{EOL_PART_NUMBER}} is discontinued {{DISCONTINUATION_TIMING}}.
- {{REPLACEMENT_PART_NUMBER}} is available for order {{REPLACEMENT_TIMING}}.
- Add warranty, support, and repair terms where they differ from standard.

### Action Required

What resale partners must physically do — typically removing the old SKU from
fulfillment systems and adding the replacement. Be imperative and specific.

### Authorization

Per `pcn-core.md`.
