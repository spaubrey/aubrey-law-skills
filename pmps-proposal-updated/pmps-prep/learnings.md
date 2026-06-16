# Learnings
Track what works and what doesn't. Updated after each use.

## Rules (always apply)

- **All body text is BLACK (#000000).** No grey body text anywhere. Use the
  `BLACK` constant in `_shared.js` for every TextRun unless rendering a
  branded color (Navy headers, Teal sub-headers, Red CONFIDENTIAL banner,
  Red MA Tax Due figures in the comparison table). If you reach for a grey
  hex like `#333333` or `#666666`, stop — body text stays black.

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

- **No firm tagline on cover page.** The cover page shows "Prepared by /
  Scott Aubrey, Esq." only — the "Aubrey Law | Needham, Massachusetts" line
  was removed (May 2026). Do not re-add it.

- **No "Lifetime Gifting" bullet in Additional Tax Strategies.** The annual
  exclusion / Roth conversion bullet was removed (May 2026). The section still
  renders for ILIT and Beneficiary Designation items when applicable.

- **No "Residuary Beneficiaries" subsection in Key Trust Provisions.** The
  backup-beneficiary paragraph was removed (May 2026). Residuary designation
  is handled in the consultation, not the proposal.

- **Optional Services defaults (May 2026):** Real Property Transfer fee is
  **$350** (quitclaim deed). Attorney-Supervised Signing description is
  **"In-person signing"** — no "or remote" and no "with notary coordination."

- **Process & Timeline is 3 steps only (May 2026):** Design → Drafting →
  Client Review/Revisions. The old Revisions step was merged into Step 3.
  Signing and Funding rows were removed entirely — the timeline ends at
  Client Review/Revisions. If you add rows back, do not re-introduce the
  Signing or Funding steps without checking with Scott.

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

- **The reference proposal uses #333333 grey for body text.** Scott
  explicitly does NOT want this — the new template uses pure black. If a
  future reference document comes back with grey body text, that is not a
  signal to switch back.
