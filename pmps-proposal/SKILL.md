---
name: pmps-proposal
description: >
  [OUTCOME]: Generates two client-facing Aubrey Law estate planning documents as
  branded .docx files — an Estate Plan Proposal (estate overview, MA estate tax
  analysis, recommended documents, fiduciary appointments, next steps) and a
  One-Page Plan Summary (condensed tax comparison, document list, next steps).
  [TRIGGER]: Activates on "draft the proposal for [client]", "generate the estate
  plan proposal", "create the one-page summary", "run the proposal docs",
  "pmps-proposal for [client]", "make the proposal and summary", or any request
  for the client-facing proposal and/or one-pager. Also triggers on "regenerate
  the proposal" or "update the proposal for [client]."
  [ANTI-TRIGGER]: Does NOT activate for the full 4-doc PMPS package with Agenda
  and Tax Worksheet (use pmps-prep), trust/will drafting, engagement agreements,
  closing packages, deed drafting, or general estate planning questions.
---

# pmps-proposal — Estate Plan Proposal + One-Page Summary

You are generating two client-facing documents for an Aubrey Law Peace of Mind
Planning Session: the Estate Plan Proposal and the One-Page Plan Summary. These
are the documents Scott hands to clients at or after the consultation.

## Start: Load Context and Learnings

1. Read `firm-context.md` in the workspace root for firm standards.
2. Read `learnings.md` in this skill folder and apply any rules.
3. If a `claude.md` exists in the current matter directory, read it for pre-filled client details.

## Legal Compliance Guardrails

These guardrails apply to every output. They exist because AI-generated estate
planning documents carry real risk if treated as final work product.

- **Cite specific sources.** When referencing client data, note where it came from
  (intake form, uploaded questionnaire, typed notes). Flag any data point whose
  source is unclear.
- **Flag uncertainty, never guess.** If intake data is ambiguous, incomplete, or
  inconsistent (figures don't add up, fiduciary names unclear, ages don't match DOBs),
  use `[VERIFY: ...]` tags. Never silently fill plausible-sounding values.
- **Not legal advice.** Tax computations and planning recommendations are drafts for
  Scott's review. They do not constitute legal advice.
- **Preserve original language.** Carry client-stated wishes, beneficiary designations,
  and named fiduciaries through verbatim.
- **Attorney review required.** Every generation report notes these are drafts pending
  Scott's review before client delivery.

---

## Step 1: Clarify Legal Insurance and Fees

Before building the data object, confirm if not clear from intake data:

1. **Does the client have a legal insurance plan?** (MetLife, ARAG, LegalShield)
   This drives the pricing columns in both documents. Ask Scott if unclear.

2. **If no legal plan — what is the flat fee?** Do not guess. Ask Scott:
   *"No legal plan detected. What flat fee should I show? (e.g., $3,500 trust-based,
   $2,000 will-only)"*

---

## Step 2: Parse Client Data

Scott will provide client data as one of: Word/PDF intake questionnaire, Excel
spreadsheet, pasted/typed notes, or a JSON design sheet payload.

Map the input to the data schema. Read `references/data-schema-quick-ref.md` for
the complete field reference (includes a full SAMPLE object). Required fields:

- Client name(s), type (couple vs. individual), address, DOBs
- Children (names, ages, minor status)
- Asset inventory with values (enough to compute gross estate)
- Fiduciary appointments (trustees, personal reps, POA agents, HCP agents, guardians)
- Recommended document list
- `hasLegalPlan` and `flatFee` (from Step 1)

Flags to determine from context: `hasMinorChildren`, `hasTrust`, `hasCreditShelter`
(couples with gross estate > $2M), `hasRealEstate`, `hasLifeInsurance`,
`hasAnticipatedInheritance`, `hasPets`.

**`plan.planStructure` (required for new matters)** — pick one:
- `joint_outright` — couple, joint trust, outright to spouse; NO credit shelter; one $2M exemption (baseline). `hasCreditShelter: false`, scenario2 = null.
- `joint_disclaimer` — couple, joint trust; survivor may disclaim into a bypass trust within 9 months; both exemptions ($4M) preserved if timely. `hasCreditShelter: true`, `maQtip: true`, scenario2 with $4M shelter.
- `separate_clayton` — couple, two trusts + credit shelter + Clayton election (fiduciary-controlled); both exemptions ($4M). `hasCreditShelter: true`, `clayton: true`, `maQtip: true`.
- `individual_single` — single person; one $2M exemption; no spouse/credit-shelter/Clayton/QTIP. `clients.type: "individual"`, `spouse2: null`.

If `planStructure` is omitted, the template falls back to the legacy
`hasCreditShelter` boolean. See `references/pmps-planstructure-mapping.md`.

If data is missing, ask Scott. Do not fill gaps with assumptions.

---

## Step 3: Compute MA Estate Tax

Read `references/ma-estate-tax-computation.md` for the rate table and algorithm.
All `netTax` figures are NET of the $99,600 unified credit. All figures are
estimates pending Scott's M-706 verification.

**Couples with planning** (`joint_disclaimer` / `separate_clayton`, gross > $2M):
- Scenario 1 (Without Planning): full estate taxed at second death (one exemption).
- Scenario 2 (With Planning): $2M bypass at first death ($0 tax); second-death taxable = **gross − $4,000,000** (BOTH exemptions). Savings = S1 netTax − S2 totalNetTax.

**Couples, baseline** (`joint_outright`, gross > $2M): one scenario (full estate
at second death, one exemption). scenario2 = null, savings = 0. Quantify the
lost exemption.

**Individuals** (`individual_single`, gross > $2M): one scenario (tax at death).
`hasCreditShelter: false`, scenario2 = null, savings = 0.

**Under $2M**: no tax due. Set all tax values to $0.

Build the full `tax` object with all intermediate values (adjustedTaxableEstate,
bracket, excess, taxOnExcess, grossTax, netTax).

---

## Step 4: Build the Data Object

Construct the complete data object. Read `references/data-schema-quick-ref.md`
for the complete field reference and a working SAMPLE object. Key details:

- Populate both raw numbers AND display strings (e.g., `grossEstate: 4300000` AND
  `grossEstateDisplay: "$4,300,000"` AND `grossEstateApprox: "$4.3 million"`)
- **Asset breakdown** — populate `assets.breakdown` as an array of `{ category,
  value, display }` items. Each item becomes a row in the Financial Overview table.
- **Children** — each child needs `name`, `dob`, `age`, `isMinor` (boolean), and
  optionally `relationship` ("Son", "Daughter") or `gender` ("M", "F").
- **Documents** — build the `plan.documents` array. Each document supports:
  - `name` — short canonical name (used for the Estate Plan Summary dedup table)
  - `displayName` — optional fuller label for the Recommended Estate Plan section
  - `category` — one of `core` / `will` / `incapacity` / `asset` / `guardian`
    (auto-inferred from name if omitted, but explicit is safer)
  - `joint` (boolean) — single document covering both spouses (e.g., Quitclaim Deed)
  - `perSpouse` (boolean) — one per spouse, identical in both plans (e.g., DPOA)
  - `forSpouse` — 1 or 2 when a document is unique to one spouse (e.g., a trust
    with spouse-specific terms — set `forSpouse: 1` on Ram's trust, `forSpouse: 2`
    on Gili's). The Estate Plan Summary auto-merges entries with the same `name`.
  - `description` — optional inline description (overrides defaults)
- **Fiduciaries** — `fiduciaries.spouse1` / `fiduciaries.spouse2` support up to
  five successor trustees via `successorTrustees: [...]`, plus `poaSuccessor` and
  `hcpSuccessor` for POA/HCP succession lines.
- **Fiduciary notes** — `fiduciaries.notes` is an array of either strings or
  `{ label, body }` objects rendered as bullets in the "Important Notes on
  Fiduciary Appointments" block.
- **Considerations** — populate `considerations` with talking points: `ilit`,
  `gifting`, `beneficiaryDesignations`, `anticipatedInheritance`,
  `realEstateTransfer`, `lifeInsurance`, `pets` (description), `petName`.
- **Legal Plan** — `data.legalPlan.covered` and `.notCovered` are arrays of
  strings rendered as bullets in the Legal Plan Coverage block.
- Set `matter.outputDir` to the absolute path of the client output folder.
- Set `matter.filePrefix` to the client's last name(s) (e.g., `"Smith"`,
  `"Miller-Bethlehem"`). For couples with different surnames, use a hyphenated
  prefix — the document header will render "Miller – Bethlehem" automatically.

**Optional overrides:**
- `data.optionalServices` — override the standard Optional Services table.
  Each item: `{ name, description, fee, status }`. Only renders for legal-plan
  clients; ignored when `data.flatFee` is set.
- `data.processTimeline` — override the standard Process & Timeline table.
  Each item: `{ step, phase, description, timeline }`.
- `data.flatFee` — when set (e.g. `"$3,500"`), the proposal renders an
  "Engagement Fee" subsection instead of "Optional Services". Flat-fee matters
  do not show optional add-ons because the flat fee is comprehensive.
- `data.flatFeeIncludes` — array of strings overriding the default "This fee
  includes:" bullets (preparation, consultations, signing ceremony, funding
  package).
- `data.flatFeeExcludes` — array of strings overriding the default "This fee
  does not include:" bullets. Default automatically includes a deed recording
  fee bullet keyed to `clients.county` when `hasRealEstate` is true.

---

## Step 5: Set Up Scripts and Run

Read `references/script-setup-guide.md` for the complete setup and run instructions.

The templates live in this skill's folder:
```
skills/pmps-proposal/
├── pmps-proposal.js         ← Estate Plan Proposal template
├── pmps-one-page-summary.js ← One-Page Summary template
├── _shared.js               ← Shared helpers (branding, tables, headers)
├── assets/
│   └── aubrey-law-logo.png
└── node_modules/            ← docx library (pre-installed)
```

Both templates require `_shared.js` in the same directory. The proposal uses
`makeHeaderProposal` (text header with client identifier) and
`makeFooterProposal` (centered "Confidential Attorney Work Product | Page N").
The one-pager uses the legacy `makeHeader` (empty) and `makeFooter` (firm
contact line). All helpers are exported from `_shared.js`.

Create the client output directory, then run both templates via bash. Each template
writes one .docx file to `data.matter.outputDir`.

---

## Step 6: Verify and Deliver

1. Confirm both .docx files exist in the output directory
2. Report what was generated and any `[VERIFY: ...]` flags for Scott's review
3. Note any data gaps that may affect document quality
4. Include standard disclaimer: *"All documents are drafts pending your review
   and approval before client delivery. Tax computations reflect current MA estate
   tax structure but do not constitute legal advice."*
5. Provide file links

---

## Estate Plan Proposal — Section Order

The Estate Plan Proposal template renders these sections in fixed order:

1. **Cover page** — title, client names, "Prepared by Scott Aubrey, Esq.",
   "CONFIDENTIAL ATTORNEY-CLIENT COMMUNICATION" banner. No firm tagline line.
   Always followed by a page break.
2. **Executive Summary** — bottom-line tax numbers + plan recommendation summary.
3. **Client Profile** + **Children** table.
4. **Financial Overview** — asset breakdown table with gross estate total.
   *(page break before)*
5. **Estate Tax Analysis** — Massachusetts section + comparison table + optional
   Federal section (only when gross estate ≥ $7M) + Additional Tax Strategies.
   *(page break before)*
6. **Recommended Estate Plan** — documents grouped by category (Core Trust,
   Will/Testamentary, Incapacity Planning, Asset Transfer, Guardian and Parental),
   each rendered as a labeled bullet with a description. Trust plans also include
   a Trust Distribution Framework sub-section.
   *(page break before)*
7. **Fiduciary Appointments** — side-by-side table with up to five successor
   trustee levels plus POA/HCP primary and successor agents. Followed by
   "Important Notes on Fiduciary Appointments" bullet list.
   *(page break before)*
8. **Key Trust Provisions** — Distribution to Children and Pet Trust Provisions
   (only when `hasTrust` is true and pets are listed). Residuary beneficiary
   designation is handled in the consultation, not in the proposal.
9. **Additional Considerations** — Anticipated Inheritance, Beneficiary
   Designation Coordination, Real Estate Transfer, Young Adult Estate Plans,
   Life Insurance Review, and a fee subsection that branches on the matter
   type: Legal Plan Coverage + Optional Services (for legal-plan clients) OR
   Engagement Fee with included / not-included bullets (for flat-fee clients).
   *(page break before)*
10. **Estate Plan Summary** — numbered ✓-mark document table with per-spouse columns.
    Deduplicates by canonical name so per-spouse documents merge into one row.
    *(page break before)*
11. **Process & Timeline** — three-step firm process table (Design → Drafting →
    Client Review/Revisions). Signing and Funding are handled outside this table.

All tables are configured with `cantSplit: true` so they will not break across
pages. Section headers use `keepNext: true` so they stay with their content.

---

## After Delivery

Ask: *"Did these documents meet your expectations? Anything to improve for next time?"*
Log useful feedback to `learnings.md`.
