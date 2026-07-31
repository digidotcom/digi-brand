---
type: blueprint
genre: Product Change Notice — new product, hardware
output: docx
---

# PCN — New Product Introduction (hardware)

Shared grammar, numbering, and the confidentiality banner live in
`pcn-core.md`. Read it first.

Announces a new hardware product to the channel ahead of market availability.
Almost always under embargo.

## Section order

### Audience

Per `pcn-core.md`. For hardware this is usually distributors and resellers,
followed by the target verticals.

### Product Overview

Two parts. First, one sentence naming the product and its category. Then a
paragraph of context: what it succeeds or consolidates, what standard it is
built on, and what it enables. If the product ships as part of a service bundle,
include a two-column feature table describing the bundle.

### Key Capabilities

A bulleted list, roughly eight to twelve items. Each bullet is a capability, not
a marketing claim — lead with the specification and let it carry the benefit.
Cover, where applicable: primary radio technology and standard, secondary radio,
SIM and carrier flexibility, redundancy, security certifications, environmental
and ruggedization standards, procurement compliance, and management platform.

### Key Dates

A three-column table:

| NPI PCN | Market Announcement | Commercial Availability |
| --- | --- | --- |
| {{PCN_DATE}} | {{ANNOUNCEMENT_DATE}} | {{PART_NUMBER}}: {{AVAILABILITY_DATE}} |

Commercial availability is per-SKU when variants ship on different dates.

### Product Variants

One column per variant, each with the variant's positioning name, its part
number placeholder, and one sentence on who it is for:

| {{VARIANT_1_NAME}} | {{VARIANT_2_NAME}} | {{VARIANT_3_NAME}} |
| --- | --- | --- |
| {{PART_NUMBER}} — {{ONE_LINE_POSITIONING}} | {{PART_NUMBER}} — {{ONE_LINE_POSITIONING}} | {{PART_NUMBER}} — {{ONE_LINE_POSITIONING}} |

### Technical Specifications

Grouped specification blocks, each a two-column label/value table. Standard
groups: Environment & Certifications, Power & Form Factor, Compute & OS,
Cellular Connectivity, Interfaces & I/O, Management.

Keep values terse. This section is a reference table, not prose.

### Customer Impact and Action Required

Two blocks side by side.

**Portfolio Impact** — what this does to the existing lineup. State plainly
whether it replaces, consolidates, or sits alongside current products, and
whether those remain available during transition.

**Order Now** — what the reader should do, and who to contact.

### SKU Table

| Part Number | Description | Region | MSRP |
| --- | --- | --- | --- |
| {{PART_NUMBER}} | {{DESCRIPTION}} | {{REGION}} | {{MSRP}} |

Description is the full channel description string, not the marketing name.

### Authorization

Per `pcn-core.md`.
