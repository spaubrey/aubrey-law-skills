# Data Schema Quick Reference

This is the complete data object shape used by both pmps-proposal.js and
pmps-one-page-summary.js. Populate all fields before running the templates.

The canonical schema (with SAMPLE and EMPTY objects) lives at:
`skills/pmps-prep-skill/pmps-prep/Templates/pmps-data-schema.js`

Read that file if you need the full SAMPLE with example values for each field.

---

## Top-Level Shape

```javascript
const data = {
  matter: { ... },        // File metadata, output path
  clients: { ... },       // Client identity and type
  children: [ ... ],      // Array of child objects
  hasMinorChildren: bool,
  hasLegalPlan: bool,
  legalPlan: null | { name, type, covered: [...], notCovered: [...] },
  flatFee: "$X,XXX",      // Used when hasLegalPlan = false
  hasTrust: bool,
  hasCreditShelter: bool, // Couples only; requires gross estate > $2M
  hasRealEstate: bool,
  hasLifeInsurance: bool,
  hasAnticipatedInheritance: bool,
  hasPets: bool,
  assets: { ... },
  tax: { ... },
  plan: { type, documents: [ ... ] },
  fiduciaries: { notes, spouse1: { ... }, spouse2: { ... } | null },
  considerations: { ... },
  // Optional overrides — leave undefined to use firm defaults from pmps-proposal.js
  optionalServices: null | [ { name, description, fee, status } ],
  processTimeline:  null | [ { step, phase, description, timeline } ],
  flags: []               // Attorney flags shown in documents
};
```

---

## matter

```javascript
matter: {
  date: "May 14, 2026",                  // Display string
  filePrefix: "Miller-Bethlehem",        // Filename prefix → Miller-Bethlehem_Proposal.docx
  outputDir: "/absolute/path/"           // Must exist before running templates
}
```

For couples with different surnames, hyphenate the prefix (e.g., "Miller-Bethlehem").
The Estate Plan Proposal header will automatically render this as
"Miller – Bethlehem" via the `clientIdentifier()` helper in `_shared.js`.

---

## clients

```javascript
clients: {
  type: "couple" | "individual",
  spouse1: {
    firstName: "Ram",
    lastName: "Miller",
    fullName: "Ram Ron Miller",
    dob: "December 30, 1967",   // Display string, optional
    age: 58,
    citizenship: "US"
  },
  spouse2: null,                // null for individual clients
  address: "21 Dorcar Rd, Newton, MA",
  county: "Norfolk County",
  dateOfMarriage: "August 28, 2001",   // Used in Client Profile table
  marriedSince: null                    // Legacy alias for dateOfMarriage
}
```

---

## children

```javascript
children: [
  {
    name: "Sophia Chen",
    dob: "January 10, 2012",
    age: 14,
    isMinor: true,
    relationship: "Daughter",   // optional — "Son" / "Daughter" / etc.
    gender: "F"                  // optional — used to derive relationship if missing
  }
]
// Empty array if no children
```

Both `dob` AND `isMinor` are required for each child. The Client Profile
"Children" table renders Name / Date of Birth / Relationship / Age / Status.

---

## assets

```javascript
assets: {
  grossEstate: 12238552,
  grossEstateDisplay: "$12,238,552",
  grossEstateApprox: "$12.2 million",
  breakdown: [
    { category: "Real Estate (21 Dorcar Rd, net of mortgage)", value: 2079000, display: "$2,079,000" },
    { category: "Bank Accounts (BofA checking & savings)",     value: 150000,  display: "$150,000" },
    { category: "Retirement Accounts (Fidelity, Morgan Stanley, others)", value: 2568600, display: "$2,568,600" },
    { category: "Brokerage / Investment Accounts",             value: 3669952, display: "$3,669,952" },
    { category: "Life Insurance (Brighthouse Financial, term)", value: 1500000, display: "$1,500,000" },
    { category: "Vehicles (Jaguar XKE, Toyota Rav4)",          value: 250000,  display: "$250,000" },
    { category: "Other Tangible Assets",                        value: 21000,   display: "$21,000" },
    { category: "Anticipated Inheritance (Ruth Miller)",        value: 2000000, display: "$2,000,000" }
  ]
}
```

Each `breakdown` entry becomes a row in the Financial Overview table. The
"ESTIMATED GROSS ESTATE" total row at the bottom uses `grossEstateDisplay`.

---

## tax

### Couples with credit shelter scenario:
```javascript
tax: {
  scenario1: {
    label: "Without Planning",
    taxableEstate: 12238552,
    netTax: 1325368,
    netTaxDisplay: "$1,325,368"
    // adjustedTaxableEstate, bracket, excess, etc. are optional and used for verification
  },
  scenario2: {
    label: "With Credit Shelter Trust",
    firstDeath: {
      bypassAmount: 2000000,
      netTax: 0
    },
    secondDeath: {
      taxableEstate: 10238552,    // grossEstate - bypassAmount
      netTax: 1005368
    },
    totalNetTax: 1005368,
    netTaxDisplay: "$1,005,368"
  },
  savings: 320000,
  savingsDisplay: "$320,000",
  savingsApprox: "~$320,000"
}
```

### Individuals or estates under $2M:
```javascript
tax: {
  scenario1: {
    label: "At Death",
    taxableEstate: 1800000,
    netTax: 0,
    netTaxDisplay: "$0"
  },
  scenario2: null,
  savings: 0,
  savingsDisplay: "$0",
  savingsApprox: "$0"
}
```

The Federal Estate Tax section in the proposal renders automatically when
`assets.grossEstate >= 7,000,000` (the TCJA sunset threshold defined in
`FIRM_CONFIG.FEDERAL_SECTION_THRESHOLD` inside `pmps-proposal.js`).

---

## plan.documents

```javascript
plan: {
  type: "Trust-Based with Credit Shelter",   // Display string
  documents: [
    // Per-spouse trust with distinct configurations — use forSpouse + same name
    { name: "Revocable Living Trust",
      displayName: "Revocable Living Trust (Ram Ron Miller Revocable Trust)",
      category: "core", forSpouse: 1,
      description: " The centerpiece of Ram's plan. ..." },
    { name: "Revocable Living Trust",
      displayName: "Revocable Living Trust (Gili Lisa Bethlehem Revocable Trust)",
      category: "core", forSpouse: 2,
      description: " Mirror trust for Gili. ..." },

    // Identical per-spouse document — perSpouse: true, one entry only
    { name: "Pour-Over Will",
      displayName: "Pour-Over Will (for each spouse)",
      category: "will", perSpouse: true },

    { name: "Durable General Power of Attorney",
      displayName: "Durable General Power of Attorney (for each spouse)",
      category: "incapacity", perSpouse: true },

    // Single joint document
    { name: "Quitclaim Deed",
      category: "asset", joint: true,
      description: " Transfers the home at 21 Dorcar Road into the trusts." },

    { name: "Parental Appointment of Guardian",
      displayName: "Parental Appointment of Guardian (Joint)",
      category: "guardian", joint: true }
  ]
}
```

**Document fields:**

- `name` — short canonical name. Used in the Estate Plan Summary table; entries
  with the same `name` are auto-merged into one row.
- `displayName` — fuller label for the Recommended Estate Plan section (optional).
- `category` — one of `core` / `will` / `incapacity` / `asset` / `guardian`.
  Auto-inferred from `name` if omitted, but explicit is safer.
- `joint` — single document covering both spouses (e.g., Quitclaim Deed).
  Rendered as "Joint" in the Estate Plan Summary marks column.
- `perSpouse` — one identical copy per spouse (e.g., DPOA). Rendered as ✓ in
  both spouses' columns in the Estate Plan Summary.
- `forSpouse: 1 | 2` — unique to one spouse (e.g., a trust with spouse-specific
  terms). When two entries share the same `name` but different `forSpouse`
  values, they merge into one Estate Plan Summary row with ✓ in both columns.
- `description` — optional inline description (overrides the built-in default).
  Leading space is preserved verbatim (e.g., `" The centerpiece..."`).

---

## fiduciaries

```javascript
fiduciaries: {
  spouse1: {
    initialTrustee: "Ram (self)",
    successorTrustees: [             // Up to 5 levels supported
      "Gili",
      "Idan",
      "Orry Margaret Miller",
      "Kurt Overton",
      "Danna Bethlehem"
    ],
    personalRep:    "Gili",
    poaAgent:       "Gili",
    poaSuccessor:   "Idan, then Kurt Overton",   // Optional second row
    hcpAgent:       "Gili",
    hcpSuccessor:   "Idan, then Orry",            // Optional second row
    guardian:       "Orry Margaret Miller"        // Required if hasMinorChildren
  },
  spouse2: { ... },   // Same shape as spouse1; null for individual clients

  // Notes block — array of either strings or { label, body } objects
  notes: [
    { label: "Non-Resident Fiduciaries",
      body: "Orry (Canada) and Danna (Israel) — practical considerations include banking access, tax filing obligations, and potential court requirements." },
    { label: "Idan's Role",
      body: "At 21, he is named as a high-priority successor. Consider a minimum age requirement (e.g., 25) for service." },
    "Plain-string notes also work and render as a simple bullet."
  ]
}
```

The Fiduciary Appointments table renders rows in this order:
Initial Trustee → Successor Trustee #1 → ... → Successor Trustee #N →
Personal Representative → Financial POA Primary → Financial POA Successor →
Health Care Agent Primary → Health Care Agent Successor → Guardian.

Rows with empty values across both spouses are rendered as "[To be determined]".

---

## considerations

```javascript
considerations: {
  // Each of these triggers a sub-section under "Additional Considerations":
  anticipatedInheritance: "Ram expects ~$2M from Ruth Miller. ...",
  beneficiaryDesignations: "Retirement accounts (~$2.57M) and most brokerage accounts ...",
  realEstateTransfer: "We will transfer your home into the trust ...",
  lifeInsurance: "The $1.5M Brighthouse Financial policy ...",
  pets: "Rusty (golden retriever) — discuss pet trust provisions.",
  petName: "Rusty",   // Optional override — used in Pet Trust Provisions text
  // Tax-strategy flags — when true, add bullets to Additional Tax Strategies
  ilit: true,
  gifting: true,
  giftingNote: null   // Optional custom text for the gifting bullet
}
// All optional. Set to null or omit if not applicable.
```

**Young Adult Estate Plans** is rendered automatically when any child has
`isMinor: false` AND `age < 30`. No data entry required — the section reads
the children array directly.

---

## legalPlan

```javascript
legalPlan: {
  name: "ARAG Legal Plan",
  type: "ARAG",
  covered: [
    "Last Will and Testament",
    "Revocable Living Trust with No Tax Planning",
    "Durable Power of Attorney",
    "Health Care Proxy",
    "Living Will / Advance Directive",
    "HIPAA Authorization"
  ],
  notCovered: [
    "Tax planning provisions",
    "Deed recording fees",
    "Notary and witness fees",
    "Attorney-supervised signing ceremonies"
  ]
}
// null when hasLegalPlan: false
```

Each `covered` and `notCovered` string is rendered as a bullet under the
Legal Plan Coverage sub-section. If you omit `covered` / `notCovered`, the
template falls back to a standard list.

---

## Optional Overrides

### `flatFee` — Engagement Fee for non-legal-plan clients

When `data.hasLegalPlan` is false and `data.flatFee` is set (e.g. `"$3,500"`),
the proposal renders an "Engagement Fee" subsection under Additional
Considerations. The flat fee is presented in bold navy with included and
not-included bullet lists. The "Optional Services" table is suppressed —
flat-fee matters do not have optional add-ons because the flat fee is
comprehensive.

```javascript
flatFee: "$3,500",
flatFeeIncludes: [   // optional override; defaults below
  "Preparation of all documents listed in this proposal",
  "All attorney consultations and revisions during the engagement",
  "Attorney-supervised signing ceremony with notary and witnesses included",
  "Post-signing trust funding instructions and closing package"  // added if hasTrust
],
flatFeeExcludes: [   // optional override; defaults below
  // Auto-included when hasRealEstate is true:
  "Deed recording fees, paid directly to the {county} County Registry of Deeds",
  "Future amendments, restatements, or revisions made after the plan is signed (billed separately when needed)"
]
```

### `optionalServices` — Legal-plan clients only

Override the standard Optional Services table. Only renders for legal-plan
clients; ignored when `data.flatFee` is set. Defaults are defined in
`FIRM_CONFIG.OPTIONAL_SERVICES` inside `pmps-proposal.js`.

```javascript
optionalServices: [
  { name: "Credit Shelter Estate Planning",
    description: "Separate trusts for each spouse to preserve both Massachusetts exemptions",
    fee: "$2,500",
    status: "Recommended" },
  { name: "Real Property Transfer",
    description: "Quitclaim deed to transfer home into trust",
    fee: "$400",
    status: "Recommended" },
  { name: "Attorney-Supervised Signing",
    description: "In-person or remote signing with notary coordination",
    fee: "$375",
    status: "Optional" }
]
```

### `processTimeline`

Override the standard 6-step Process & Timeline table. Defaults are defined in
`FIRM_CONFIG.PROCESS_TIMELINE` inside `pmps-proposal.js`.

```javascript
processTimeline: [
  { step: "1", phase: "Design",        description: "Attorney prepares final design sheet", timeline: "1 week" },
  { step: "2", phase: "Drafting",      description: "All documents prepared",                timeline: "2–3 weeks" },
  { step: "3", phase: "Client Review", description: "Review all drafts, provide feedback",   timeline: "1–2 weeks" },
  { step: "4", phase: "Revisions",     description: "Incorporate changes",                   timeline: "1 week" },
  { step: "5", phase: "Signing",       description: "Execute documents with witnesses/notary", timeline: "Scheduled" },
  { step: "6", phase: "Funding",       description: "Re-title assets, update beneficiaries, record deed", timeline: "2–4 weeks" }
]
```

---

## Page-Break Behavior

The Estate Plan Proposal forces page breaks before these sections:

- Financial Overview
- Estate Tax Analysis
- Recommended Estate Plan
- Fiduciary Appointments
- Additional Considerations
- Estate Plan Summary

Page breaks before each of these sections give long sections (like Estate Tax
Analysis and Recommended Estate Plan) room to breathe. The trade-off is some
whitespace at the bottom of preceding pages when content is short. To suppress
a page break, edit the corresponding `sectionHdr(..., { pageBreakBefore: true })`
call in `pmps-proposal.js`.

All tables in the proposal are configured with `cantSplit: true` so they will
not break across pages.
