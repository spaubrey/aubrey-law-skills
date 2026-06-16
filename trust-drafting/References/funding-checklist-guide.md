# Client-Specific Funding Checklist — Generation Guide

## What this document is

This guide produces a **client-specific Trust Funding Plan**: a matter-specific
analysis built from the client's actual financial data. It is NOT the generic
"Funding Instructions & Checklist" (that document, governed by
`funding-instructions-guide.md`, explains funding by asset *type* and includes
FAQs). The two are **separate deliverables and both are produced** when a
financial summary is available.

| Document | Source guide | Driven by | Content |
| --- | --- | --- | --- |
| Funding Instructions & Checklist (generic) | `funding-instructions-guide.md` | Asset types present | Educational guide, FAQs, by asset category |
| **Trust Funding Plan (this guide)** | this file | **Client financial spreadsheet** | Named assets, real values, per-asset actions, numbered priority checklist |

**File name:** `YYYY-MM-DD_Trust-Funding-Plan_[CLIENT-LAST-NAME].docx`

The bundled examples show the exact target output and input format:
- `assets/funding-checklist-EXAMPLE.docx` — a completed plan (the Woo matter)
- `assets/financial-summary-EXAMPLE.xlsx` — the spreadsheet it was built from

Read both before generating, so the output matches house format. The example is
a reference for **structure and tone only** — every value, name, address, county,
and action must come from the current client's data, never copied from the example.

---

## Input: the financial summary spreadsheet

The client provides an exported financial summary (`.xlsx`). The expected layout
is the Aubrey Law export format. **It will usually follow this format, but handle
minor variation gracefully** — if a section header is renamed, a column is shifted,
or a category is absent, map by meaning rather than by fixed cell position, and
flag anything you cannot confidently map with `[REQUIRES COMPLETION]`.

### Sheet structure (expected)
A single "Financial Summary" sheet with stacked category sections. Each section
begins with a category header row, followed by a column-label row, then asset rows.

Category sections, in order:
1. **Real Estate** — columns: Type, Address, Owner, (blank), (blank), Estimated Value, Mortgage Balance, Net
2. **Bank Accounts** — columns: Bank, Type, Owner, Account Number, Beneficiaries, Balance, (blank), Net
3. **Retirement Accounts** — same columns as Bank Accounts
4. **Stock, Bonds, Brokerage Accounts** — columns: (blank), (blank), Owner, Description, (blank), Estimated Value, (blank), Net
5. **Life Insurance** — columns: (blank), (blank), Owner, Description, (blank), Estimated Value, (blank), Net
6. **Category Totals** — a roll-up table: Category, Primary, Spouse, Joint, (other), Credit, Debit, Net

### Owner tags (critical)
The `Owner` column uses these tokens. Map them to people using the matter's client
and spouse names (from `claude.md` or intake):
- `primary` → the primary client (e.g., Brian)
- `spouse` → the spouse (e.g., Amy)
- `joint` / `both` → jointly held
- A literal name → use as written

Never assume which spouse is "primary"/"spouse" — confirm against intake data.

### Reading values
- Use the **Net** column for estate-inclusion and the asset inventory table.
- Use **Estimated Value / Balance** as Gross.
- The **Category Totals** roll-up is the source of truth for totals; reconcile your
  per-asset sums against it and flag any discrepancy rather than silently overriding.

### Rows to skip (do not treat as assets)
- The category header row (col A = a category name like "Bank Accounts").
- Any column-label row — including ones where col A is blank but the row contains
  labels like `Owner`, `Description`, `Type`, `Balance`, or `Net`. The Brokerage
  and Life Insurance sections have a blank col A on their label row; identify these
  by the presence of `Owner`/`Description` text, not by col A.
- Blank spacer rows and zero-value placeholder rows (no owner and Net = 0).
- For Brokerage and Life Insurance sections, col A is blank on real asset rows too —
  name the asset from the **Description** column, or fall back to the category name
  plus an index (e.g., "Brokerage Account #1") as the example does.

---

## Output structure

Mirror the example document's section order exactly:

1. **Title block** — `TRUST FUNDING PLAN`, then `[Client Name] and [Spouse Name]`
   (or single name for an individual matter).

2. **Current Asset Inventory table** — Category | Asset | Current Owner | Gross Value
   | Net Value. One row per asset, grouped by category, with a final `TOTAL / All
   Assets` row. Carry the life-insurance face-value footnote when policies are
   individually owned:
   *"Life insurance death benefits are included above at face value for estate
   inclusion purposes (policies are owned individually). Actual estate inclusion
   depends on ownership structure."*

3. **Recommended Funding Plan** — narrative sections, one per asset category that is
   present. Use the section letters/titles from the example as the pattern:
   - Section A — Real Estate
   - Section B — Brokerage / Investment Accounts
   - Section C — Bank Accounts
   - Section D — Retirement Accounts (Do NOT Fund into Trusts)
   - (add a Life Insurance section if policies exist)

   Each section: a short framing paragraph, then bulleted per-asset actions with
   real asset names and dollar values, an **Action:** line, and (for real estate /
   transfers) an **Estate inclusion:** line. Suppress any section whose category has
   no assets.

4. **Funding Action Checklist table** — # | Action Item | Trust | Priority.
   One numbered row per concrete action, with Trust assignment (e.g., "Brian's Trust",
   "Amy's Trust", "Both Trusts") and Priority (HIGH / MEDIUM / ONGOING). End with the
   annual-review ONGOING row.

5. **Important Caveats and Assumptions** — bulleted. Always include: values are
   client-provided estimates as of [export date]; MA estate-tax threshold subject to
   change; not a comprehensive financial plan; brokerage account type assumption
   (taxable vs. tax-deferred); CPA basis review before large transfers; informational
   only / not legal advice.

---

## Strategy selection (MANDATORY GATE)

The plan may incorporate tax and structuring strategies — e.g. interspousal
transfers to equalize estates, bypass/credit-shelter funding, see-through trust
beneficiary designations, tenants-in-common retitling of a residence. **Do NOT
apply these automatically.** Before drafting the narrative sections, present the
applicable strategies to Scott and ask which to include for this matter.

Use AskUserInput. Offer only strategies the asset data actually supports
(e.g., only offer interspousal equalization if estates are materially unequal and
both spouses have trusts). For each strategy Scott declines, omit its narrative and
its checklist rows; for each he includes, draft per the example's treatment.

Default framing for the asset inventory, per-asset retitling actions, and the
mechanical checklist (deeds, retitling, beneficiary updates) is always generated —
the gate governs only the **tax/structure recommendations layered on top**.

---

## Formatting

This is a **client guide, not an executed legal instrument**. It follows the same
branded Aubrey Law styling as the generic Funding Instructions
(logo header, navy/teal accents, firm footer, Garamond) — see
`funding-instructions-guide.md` for exact hex values, header/footer specs, and
table styling. Reuse that styling so the two funding documents look like a set.

- Inventory and checklist tables: teal header row `0F6E56`, white bold text,
  `CCCCCC` borders, Garamond 12pt body.
- Dollar values: format with thousands separators and leading `$`.
- Never use unicode bullets — use `LevelFormat.BULLET`.
- US Letter, margins per the funding-instructions spec.

Run `python scripts/office/validate.py [file].docx` after generating.

---

## Compliance

- This document **does not constitute legal, tax, or financial advice** and creates
  no attorney-client engagement for implementation. Carry the example's disclaimer
  language verbatim.
- Every dollar value, name, address, and county must trace to the client's data.
  Do not import any figure from the example file.
- Flag every unmapped or ambiguous field with `[REQUIRES COMPLETION]` and list it
  in the delivery summary.
- Include the standard footer note:
  *"Draft document — requires attorney review before delivery to client."*
