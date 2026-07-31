---
type: blueprint
genre: Product Change Notice
output: docx
---

# PCN — shared grammar

A Product Change Notice is Digi's formal, channel-facing notification that a
product is changing. It gives the channel a standard heads-up window — typically
30 days — before the change takes effect.

The three flavors share less than you would expect. Only the elements below are
common; everything else belongs to the variant. Pick a variant:

- **New product** — hardware: `pcn-npi-hardware.md` · software: `pcn-npi-software.md`
- **End of life** — `pcn-eol.md`
- **Price change** — `pcn-price-change.md`

## Numbering

`PCN_YYMMDD-NN_<Type>_<Subject>`

- `YYMMDD` is the PCN issue date, not the effective date.
- `NN` is a two-digit sequence within that day, starting at `01`.
- `<Type>` is the flavor: `New_Product_Introduction`, `Product_EOL_Notification`,
  or `Price_Change_Notification`.
- `<Subject>` names the product or product family.

Example shape: `PCN_{{YYMMDD}}-{{NN}}_{{TYPE}}_{{SUBJECT}}`

## Audience

Every PCN opens by naming exactly who it is for. This is not boilerplate — the
audience determines what pricing may appear and what may be said about
unreleased product.

Common values:

- `All Cellular Product Distributors and Resellers`
- `Distributors`
- `Partners only`
- `All cellular product distributors, resellers, and customers`

Optionally followed by a vertical list, e.g.
`{{VERTICAL_1}} · {{VERTICAL_2}} · {{VERTICAL_3}}`.

## Shared elements

**Date header.** Every PCN carries its issue date. Most also carry the date the
change takes effect, under whichever label the variant uses (`Effective Date`,
`Market Announcement`, `Go-Live Date`).

**A statement of what is changing.** One paragraph, plain, near the top. The
reader should know what is happening before any table.

**Confidentiality banner** — required when the notice precedes public
announcement:

> **CONFIDENTIAL | EMBARGO UNTIL {{EMBARGO_DATE}}**
> This notice is under embargo. Do not post, share externally, or distribute in
> any form prior to the official market announcement.

Only include it when an embargo genuinely applies. Never ship a real date in a
template.

**Authorization block** — present on new-product and EOL notices, absent on
price changes:

```
{{ISSUING_TEAM}} Product Management
Digi International Inc.
```

## Rules

- Write in the plain, professional register of `digi-brand-guidelines`.
- Never state a price the audience is not entitled to see. Distributor pricing
  goes only to distributor audiences.
- Never name an unreleased SKU in a notice that is not under embargo.
- Every table uses `{{PLACEHOLDER}}` tokens until real values are filled in by
  the author.
