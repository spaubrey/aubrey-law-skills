# Learnings
Track what works and what doesn't. Updated after each use.

## Rules (always apply)

- **All body text AND all sub-section headings are BLACK (#000000).** No grey
  body text anywhere, and no teal/green sub-headings. Use the `BLACK`
  constant in `_shared.js` for every TextRun unless rendering a branded
  color (Navy main section headers, Red CONFIDENTIAL banner, Red MA Tax
  Due figures, Teal-fill table cells/borders/savings dollar figure). If
  you reach for a grey hex like `#333333` or `#666666`, stop — body text
  stays black.

- **`subSectionHdr` default text color is BLACK.** Per Scott (June 2026),
  the H2 sub-section headings render in pure black, not teal. This affects
  every "Children", "Massachusetts Estate Tax", "Federal Estate Tax",
  "Core Trust Documents", "Distribution to Children", "Pet Trust Provisions",
  "Legal Plan Coverage", etc. heading. The running header "AUBREY LAW"
  text and the cover-page subtitle are also BLACK. Teal is reserved for
  table fills (L_TEAL), accent rule lines, and the comparison-table
  savings dollar figures.

- **Tables never split across pages.** Every table row built by this skill
  uses the `tRow()` helper, which sets `cantSplit: true`. If you add a new
  table or row directly with `new TableRow(...)`, you MUST set `cantSplit: true`.

- **Major sections force a page break.** Six section headers in the proposal
  use `pageBreakBefore: true`: Financial Overview, Estate Tax Analysis,
  Recommended Estate Plan, Fiduciary Appointments, Additional Considerations,
  Estate Plan Summary. This is intentional — it gives long sections room to
  breathe at the cost of some whitespace on preceding pages. Do not remove
  these without checking with Scott.

- **`_shared.js` is shared between pmps-proposal and pmps-one-page-summary.**
  Maintain backwards compat:
  - `makeHeader()` / `makeFooter(docType)` — legacy, used by the one-pager.
    Header is empty; footer is firm-contact line with right-aligned page no.
  - `makeHeaderProposal(docType, clientId)` / `makeFooterProposal()` — new,
    used by the proposal. Text header with AUBREY LAW | docType | clientId;
    centered "Confidential Attorney Work Product | Page N" footer.

- **Estate Plan Summary dedupes by `name`.** Per-spouse documents (e.g., two
  trusts, one per spouse) collapse to a single row with ✓ in both columns.
  To distinguish them in the Recommended Estate Plan section, use
  `displayName` for the labeled bullet while keeping `name` identical and
  setting `forSpouse: 1` / `forSpouse: 2`.

- **Column widths for fixed-text columns.** Some words are wider than they
  look in Garamond:
  - "Recommended" needs at least **2200 DXA** in the Status column with the
    standard 160 DXA cell padding. Tested at 1500/1760/2200; 2200 is the
    first that fits cleanly.
  - "Step" wraps to "Ste\np" in a 720 DXA column at Garamond 10pt. Widen to
    **880 DXA** in the Process & Timeline table.

- **CSS-style "cantSplit" is row-level, not table-level.** Setting it on a
  `TableRow` is what keeps rows together; setting it on a `Table` does
  nothing. Always pass it per row via the `tRow()` helper.

- **`pageBreakBefore` on section headers.** This is set in the `sectionHdr()`
  options object: `sectionHdr("Title", NAVY, { pageBreakBefore: true })`.
  Section headers also have `keepNext: true` and `keepLines: true` set by
  default so they stay with the following paragraph.

- **Fee section branches on matter type, not on whether `optionalServices` is
  populated.** Flat-fee clients (`data.flatFee` is set) get an "Engagement Fee"
  subsection with included / not-included bullets; the Optional Services table
  is suppressed entirely. Legal-plan clients (`data.hasLegalPlan: true`,
  `data.flatFee` not set) get "Legal Plan Coverage" + "Optional Services".
  Don't try to render Optional Services for a flat-fee client even if
  `data.optionalServices` is passed — the flat fee is comprehensive and only
  deed recording fees are separately payable.

- **Deed recording fees are NEVER included in any Aubrey Law engagement.** They
  are paid directly to the Registry of Deeds by the client. The "This fee does
  not include" list for flat-fee clients with real estate auto-generates a
  bullet keyed to `clients.county`. The MetLife / ARAG / LegalShield
  `legalPlan.notCovered` list should also include "Deed recording fees".

## Observations (patterns noticed)

- **`pmps-one-page-summary.js` was a backwards-compat hazard.** It imports
  `makeHeader` / `makeFooter` from `_shared.js`. The first rewrite changed
  those signatures and silently broke the one-pager. Fix: kept the legacy
  names with their original behavior and added `makeHeaderProposal` /
  `makeFooterProposal` for new code. Always grep for usages of any
  `_shared.js` export before changing its signature.

- **Pet pronoun grammar is hard to detect from `cons.pets` alone.** The
  `petPronoun()` helper looks for "him/he/his" or "her/she" tokens in the
  free-text description. When the user writes "Rusty (golden retriever)"
  with no pronouns, the helper falls back to "they/are" — grammatically
  awkward for a single named pet. Workaround: set `cons.petName` AND write
  the `cons.pets` string with a pronoun ("Rusty is our golden retriever").

- **LibreOffice renders tables slightly tighter than Word.** Column widths
  that look fine in Word may wrap in the LibreOffice → PDF conversion path.
  Always inspect the rendered PDF, not just the .docx in Word, when changing
  table widths.

- **Process & Timeline is now 3 steps, not 6.** As of May 2026, the
  PROCESS_TIMELINE array has 3 rows: Design → Drafting → Client Review/Revisions.
  The old Revisions, Signing, and Funding rows were removed. Step 3 description
  includes "and incorporate changes" to absorb the former standalone Revisions step.
  Do not add extra rows back unless Scott says so.

- **No "Lifetime Gifting" in Additional Tax Strategies.** The gifting bullet
  (annual exclusion + Roth language) was deliberately removed. ILIT and
  Beneficiary Designation bullets remain conditional on `cons` flags.

- **No "Residuary Beneficiaries" section.** The sub-section under Key Trust
  Provisions was removed. Distribution to Children and Pet Trust Provisions
  remain.

- **Cover page tagline removed.** "Aubrey Law | Needham, Massachusetts"
  under "Scott Aubrey, Esq." on the cover is gone. The footer still has
  the firm contact line — that is separate and stays.

- **Optional Services defaults updated May 2026.** Real Property Transfer
  fee is $350 (was $400). Attorney-Supervised Signing description is
  "In-person signing" (removed "or remote signing with notary coordination").

- **The reference proposal uses #333333 grey for body text.** Scott
  explicitly does NOT want this — the new template uses pure black. If a
  future reference document comes back with grey body text, that is not a
  signal to switch back.

---

## June 2026 — Four plan structures + Clayton/QTIP, net tax fix

Added support for `plan.planStructure` (master switch) with four values and made
the previously hard-coded separate-trust/Clayton narrative conditional. See
`references/pmps-planstructure-mapping.md` for the full toggle matrix.

- **`plan.planStructure`** = `joint_outright` | `joint_disclaimer` |
  `separate_clayton` | `individual_single`. Resolved by
  `shared.resolvePlanStructure(data)`, which derives `isCouple`,
  `hasCreditShelter`, `clayton`, `maQtip`, `disclaimer`, `isSeparateTrusts`,
  `isJointTrust`, `isIndividual`. **Backward compatible:** when `planStructure`
  is absent, it falls back to the legacy top-level booleans, so old data still
  renders.

- **Net tax is authoritative (Scott confirmed June 2026).** The template only
  *displays* the pre-supplied `tax` object; it does not compute tax. `netTax`
  fields are net of the $99,600 unified credit. The earlier Venables output
  showed GROSS figures ($1,769,506) — those came from the data builder, not this
  template. For live matters to show net, the data step must supply net figures.
  Schema SAMPLEs and `references/ma-estate-tax-computation.md` now both encode net.

- **$4M fix.** The "both exemptions preserved" scenario shelters
  `grossEstate − $4,000,000` at the second death (was $2M in the old reference).
  Table and narrative now agree. Enforced in the schema SAMPLEs.

- **Post-2023 anti-cliff credit.** The MA Estate Tax paragraph previously used
  pre-2023 "cliff" language ("the entire estate is subject to tax"). Corrected
  to the credit treatment (credit up to $99,600 effectively exempts the first
  $2M; only the excess is taxed). This is a methodology change — flagged for
  Scott's M-706 verification.

- **Structure-specific narrative branches:**
  - Executive Summary paragraph 2 explains the *mechanism* per structure
    (Clayton election; disclaimer + 9-month dependency; outright trade-off;
    individual lifetime strategies).
  - New **"What This Plan Accomplishes"** subsection (was previously only in the
    data, never in the template) with structure-tailored bullets.
  - New **"How the Credit Shelter Planning Works"** subsection: Clayton/QTIP +
    Shaffer (SJC-12812) for separate_clayton; disclaimer mechanics for
    joint_disclaimer; "Preserving the First Exemption — Options to Consider" for
    joint_outright over threshold.
  - **§35 out-of-state property** note (2025 Mass. Acts Ch. 9) fires when
    `considerations.businessInterest`/`outOfStateProperty` set or a flag matches.
  - **ILIT-liquidity bullet** ("…forced sale of your business interests") fires
    only when a business interest is flagged (Scott's decision June 2026).

- **individual_single guard tightened.** The MA Estate Tax paragraph is now
  couple-only; individuals get a single-person variant with NO spouse /
  first-death / second-death references. Verified: 0 occurrences of "spouse" in
  the individual sample output.

- **Fiduciary key compatibility.** `shared.normalizeFiduciary()` accepts both the
  legacy keys (`trustee`, `successorTrustee`) and current schema keys
  (`initialTrustee`, `successorTrustees[]`, `poaSuccessor`, `hcpSuccessor`).
  `normalizeNotes()` accepts a string or an array of `{label, body}`.

- **`forSpouse` document labels.** Doc-list label logic now handles
  `forSpouse: 1|2` (separate_clayton's two per-spouse trusts) in addition to
  `joint`/`perSpouse`.

**Preserved:** all April/May 2026 patches (3-step timeline, removed Lifetime
Gifting / Residuary / cover tagline, $350 Real Property Transfer, pure-black
body), Garamond, navy/teal, cantSplit, page breaks, clientIdentifier, itemized
engagement fee.

**Files touched:** `pmps-proposal.js`, `pmps-one-page-summary.js`, `_shared.js`
(added resolver + normalizers), `references/ma-estate-tax-computation.md`
(replaced), `references/pmps-planstructure-mapping.md` (added).

**ALL tax figures remain estimates pending Scott's M-706 verification.**
