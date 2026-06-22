---
name: trust-closing-package
description: >
  [OUTCOME]: Drafts post-signing client documents for trust matters: Trust
  Closing Letter, Trust Funding Instructions & Checklist, and (DIY matters)
  DIY Signing Instructions — print-ready .docx in Aubrey Law branding.
  [TRIGGER]: "draft the closing package," "closing documents for [client],"
  "post-signing package," "funding instructions," "closing letter," "add the
  signing instructions," "DIY signing instructions," or any request for
  client-facing wrap-up documents after trust execution.
  [ANTI-TRIGGER]: Not for will-only plans, general drafting, intake, or the
  signing meeting checklist. Not for Estate Plan Summary — use
  generate-estate-plan-summary instead.
---

# Trust Closing Package — Aubrey Law

## Purpose

Produce up to three client-facing documents sent after trust signing:
1. **Trust Closing Letter** — personalized congratulatory letter summarizing
   documents received, funding obligations, beneficiary designations, and next steps.
2. **Trust Funding Instructions & Checklist** — comprehensive reference guide
   explaining how to fund the trust by asset type, with a fillable checklist.
3. **DIY Signing Instructions** *(for DIY/remote signing matters only)* — step-by-step
   signing guide with a checklist for clients executing their plan without an
   attorney-supervised ceremony.

---

## Brand Standards (apply to both documents)

| Element | Spec |
|---|---|
| Font | Garamond throughout |
| Body size | 12pt (24 half-points) |
| Body color | `2C2C2A` (near-black) |
| Navy (titles) | `1B3A6B` |
| Teal (headings, dividers, accents) | `0F6E56` |
| Gray (secondary text) | `555555` |
| Page size | US Letter: 12240 × 15840 DXA |
| Margins | Top/Bottom 1080, Left/Right 1008 DXA |
| Header | Aubrey Law logo image (assets/aubrey-law-logo.png), centered, no text |
| Footer | Top border CCCCCC; centered 10pt: "1329 Highland Ave, Suite 1, Needham, MA 02492  ·  (781) 474-3450  ·  aubreylegal.com" |
| Section headings | Teal 0F6E56, with teal bottom-border rule |
| Table header rows | Teal background 0F6E56, white text FFFFFF |
| Checklist checkboxes | ☐ unicode (U+2610) in first column |

**Logo image:** Stored at `assets/aubrey-law-logo.png` in this skill folder.
Use as inline image in the header of each document.
Image target size: cx ≈ 3288300 EMU × cy ≈ 610636 EMU (~3.42 in wide × 0.63 in tall).

---

## Before Starting

1. Read `references/closing-letter-guide.md` and `references/funding-instructions-guide.md`
   for complete content specs, section order, conditional logic, and table row lists.
2. If this is a **DIY/remote signing matter**, also read `references/diy-signing-guide.md`
   for the signing instructions document spec.
3. Check if a `claude.md` file exists in the current directory. If so, read it
   for matter context and use it to pre-fill inputs.
4. Read `learnings.md` in this skill's folder (if it exists) and apply any active rules.

---

## Step 1: Gather Matter Information

| Field | Notes |
|---|---|
| Client full legal name | Required |
| Spouse full legal name | If married; leave blank if single |
| Trust name | e.g., "The John and Jane Smith Revocable Trust" |
| Date of trust execution | mm/dd/yyyy |
| Trustee name(s) | For correct titling format in Funding Instructions |
| Marital status | Married / Single |
| Minor children? | Yes / No — affects document list and "Keeping Current" section |
| Documents in package | Which documents were executed |
| Signing date / letter date | Date to appear at top of Closing Letter |
| Special notes | Out-of-state real estate, business interests, S-Corp shares, etc. |
| DIY signing? | Yes / No — if Yes, also produce the DIY Signing Instructions document |

Do not ask for information that can be inferred.

---

## Step 2: Draft the Trust Closing Letter

Read `references/closing-letter-guide.md` for complete section content, brand colors,
font sizes, heading border styles, document list conditional logic, and signature block.

Draft as a .docx using the **docx skill** (JavaScript/docx-js).
File name: `Closing-Letter_[CLIENT-LAST-NAME]_v1.docx`

Key formatting:
- Header: logo image centered (from assets/aubrey-law-logo.png)
- Title: Garamond 14pt bold, navy 1B3A6B, centered
- Section headings: Garamond 11pt, teal 0F6E56, teal bottom border
- Body: Garamond 12pt, justified
- Checklist table: teal header row, ☐ checkbox column, full page width

---

## Step 3: Draft the Trust Funding Instructions

Read `references/funding-instructions-guide.md` for all 7 sections, asset-type
checklist rows (and which to suppress), RMD table, FAQ blocks, and required disclaimer.

Draft as a .docx using the **docx skill** (JavaScript/docx-js).
File name: `Funding-Instructions_[CLIENT-LAST-NAME]_v1.docx`

Key formatting:
- Header: same logo as Closing Letter
- Title block: navy supertitle + teal subtitle + gray trust name, all centered
- Checklist: 3-column table (☐, Asset Type, Action Required), teal header
- Suppress inapplicable rows when confirmed by Scott
- Disclaimer required at bottom

---

## Step 4: Draft the DIY Signing Instructions *(DIY matters only)*

Skip this step if the signing was attorney-supervised.

Read `references/diy-signing-guide.md` for the full content of both the
Step-by-Step Instructions and the Checklist sections, the witness block reference,
the notary block reference, and the formatting spec.

Draft as a .docx using the **docx skill** (JavaScript/docx-js).
File name: `DIY-Signing-Instructions_[CLIENT-LAST-NAME]_v1.docx`

Key formatting:
- Header: same logo as Closing Letter and Funding Instructions
- Title: `How to Properly Sign Your Estate Plan` — Garamond 14pt bold, navy `1B3A6B`, centered
- Sub-line: `Prepared for: [CLIENT FULL NAME]` — Garamond 11pt, centered, teal divider below
- Main section headings (`STEP BY STEP INSTRUCTIONS`, `CHECKLIST`): teal, 11pt, teal bottom border
- Sub-step headings: bold, 11pt
- Body: Garamond 12pt, bullet lists in ListParagraph style

---

## Step 5: Quality Review

- [ ] Logo in header on both documents (and DIY signing doc if applicable)
- [ ] Footer correct on all pages
- [ ] Client name(s) and trust name consistent throughout
- [ ] Correct titling format in Funding Instructions
- [ ] Conditional blocks (marital status, minor children) correctly applied
- [ ] No unfilled brackets remain
- [ ] Teal 0F6E56 for headings, navy 1B3A6B for titles, Garamond font
- [ ] Teal table header rows with white text
- [ ] Disclaimer at bottom of Funding Instructions
- [ ] Files named correctly
- [ ] DIY Signing Instructions included if DIY matter; omitted if attorney-supervised

Add `[REQUIRES ATTORNEY REVIEW]` at top of each draft.

---

## Legal Compliance Guardrails

- Funding Instructions must include the standard disclaimer at the bottom.
- Preserve Scott's exact language from reference guides — do not improvise.
- Flag uncertainty rather than guess at client-specific situations.
- Output requires attorney review before client delivery.
- DIY Signing Instructions must reproduce the source language exactly — do not paraphrase witness or notary block content.

---

## Step 6: Deliver

Present all .docx files to Scott with a brief summary of any conditional blocks
applied, any rows suppressed, and whether the DIY Signing Instructions were included.
Ask for feedback and log to `learnings.md`.
