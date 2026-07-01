---
name: metlife-claim
description: >
  Prepares MetLife Legal Plan reimbursement claim documents (.docx) for Aubrey Law matters.
  Use this skill whenever Scott says "prepare a MetLife claim," "do the MetLife billing for
  [client]," "submit a MetLife claim," "generate the MetLife claim," "MetLife reimbursement
  for [client]," "fill out the MetLife claim," "bill MetLife for [client]," or any mention
  of billing or submitting completed work to the MetLife Legal Plan for reimbursement.
  Trigger even on casual requests like "do MetLife for the Smiths" or "prep the MetLife docs."
  Produces a structured, print-ready checklist document with dynamically calculated section
  totals and a grand total — using correct MetLife billing names and codes — ready to reference
  when submitting reimbursement on the MetLife attorney portal. Also includes a Portal
  Submission Table at the end of the doc for use with the submit-metlife-claim skill.
---

# MetLife Legal Plan Claim Generator

Generates a formatted MetLife reimbursement claim `.docx` with dynamic totals — every
section total and the grand total are computed from the actual line items, never hardcoded.

The document includes two parts:
1. **The formatted claim checklist** — for Scott's reference during portal entry
2. **The Portal Submission Table** — a flat list of every line item formatted for the
   `submit-metlife-claim` skill to drive automated portal submission

---

## Workflow

### Step 1 — Collect required information

Use `AskUserQuestion` if any of the following are missing from the conversation:

| Field | Notes |
|-------|-------|
| Member name | Full legal name of MetLife plan member |
| Member ID | MetLife member ID number |
| Plan type | See Plan Types table below |
| Date work started | Can be a date string like "April 1, 2026" |
| Date work finished | Can be a date string like "April 15, 2026" |
| Spouse name | Required for couple plans |
| Include Realty Trust? | Yes/No — adds a Deed + Realty Trust + Affidavit section; ask how many properties |
| Include Minor Guardian? | Yes/No — adds a Temporary Guardian Affidavit to the shared section |

Date submitted defaults to today if not provided.

### Step 2 — Generate the claim document

Build the `.docx` with the structure below. Compute all totals dynamically from
line item fees — never hardcode a total.

**Document structure:**

1. **Header block** — METLIFE CLAIM, plan type subtitle
2. **Info block** — Member ID, names, dates, Total Claim (sum of all line items)
3. **One claim section table per group** (see plan structures below), each with:
   - Column 1: Checkbox ☐
   - Column 2: MetLife billing document name
   - Column 3: Standard fee
   - Column 4: Comment (names, relationship)
   - TOTAL row at bottom of each section
4. **Grand Total** at bottom right
5. **Portal Submission Table** (see below) — appended after the grand total

### Step 3 — Portal Submission Table

After the grand total, append a section titled **"Portal Submission Table"** with
this exact table structure — one row per line item, in the same order as the claim:

| # | Document | Service Type | Fee | Comment | Complete |
|---|----------|-------------|-----|---------|----------|
| 1 | Power of Attorney (Financial)(Member and Spouse) | Power of Attorney | $85.00 | Financial Powers of Attorney for Member and Spouse | Yes |
| 2 | Power of Attorney (Medical)(Member and Spouse) | Power of Attorney | $85.00 | Medical Powers of Attorney for Member and Spouse | Yes |
| ... | ... | ... | ... | ... | ... |

**Service Type values** — use exactly these strings:

| Document | Service Type |
|----------|-------------|
| Power of Attorney (Financial) | Power of Attorney |
| Power of Attorney (Medical) | Power of Attorney |
| Power of Attorney (HIPAA) | Power of Attorney |
| Advanced Medical Directive | Advanced Medical Directive |
| Last Will and Testament | Will |
| Individual Trust No-Tax Planning | Trust - No Tax Planning |
| Joint Trust No-Tax Planning | Trust - No Tax Planning |
| Affidavit | Affidavit |
| Deed | Deed |

**Complete column** — always "Yes" for all rows.

Number the rows sequentially across all sections (don't restart numbering per section).

### Step 4 — Save and present

Save the `.docx` to the workspace folder. Name it:
`[Client Last Name(s)]_MetLife_Claim_[YYYY-MM-DD].docx`

After saving, present the file link and tell Scott:
- The calculated total claim amount
- The number of portal submissions the doc contains (row count of Portal Submission Table)

---

## Plan Types

| `plan_type` value | Description |
|-------------------|-------------|
| `separate_trust` | Married — each spouse has their own individual revocable trust |
| `joint_trust` | Married — one shared joint revocable trust |
| `will_couple` | Married — will-based plan, no trust |
| `will_individual` | Single person — will-based plan |
| `individual_trust` | Single person — individual revocable trust |

---

## What Each Plan Generates

### `separate_trust` (most common MetLife trust scenario)

**Shared — [Member] and [Spouse]**
- Power of Attorney (Financial)(Member and Spouse) — $85 — couple rate
- Power of Attorney (Medical)(Member and Spouse) — $85 — couple rate
- Power of Attorney (HIPAA)(Member and Spouse) — $85 — couple rate
- Advanced Medical Directive (Member and Spouse) — $65 — couple rate

**[Member] Trust Claim**
- Last Will and Testament for Member — $150 — non-reciprocal pour-over will
- Individual Trust No-Tax Planning (Member) — $325
- Affidavit — $65 — Affidavit of Trust for [Member] Revocable Trust

**[Spouse] Trust Claim**
- Last Will and Testament for Spouse — $150 — non-reciprocal pour-over will
- Individual Trust No-Tax Planning (Spouse) — $325
- Affidavit — $65 — Affidavit of Trust for [Spouse] Revocable Trust

*(optional, repeat per property)* **Realty Trust and Deed**
- Deed — $90
- Joint Trust No-Tax Planning (Member and Spouse) — $400
- Affidavit — $65 — Affidavit of Trust for Realty Trust

> Note: In Separate Trust plans, each pour-over Will bills at the individual member
> rate ($150), not the couple rate ($185), because the wills are non-reciprocal.

### `joint_trust`

**Shared**
- Power of Attorney (Financial)(Member and Spouse) — $85
- Power of Attorney (Medical)(Member and Spouse) — $85
- Power of Attorney (HIPAA)(Member and Spouse) — $85
- Advanced Medical Directive (Member and Spouse) — $65

**Trust Claim**
- Last Will and Testament (Member and Spouse) — $185 — couple rate
- Joint Trust No-Tax Planning (Member and Spouse) — $400
- Affidavit — $65

*(optional, repeat per property)* **Realty Trust and Deed** — same as above

### `will_couple`

**Shared**
- Power of Attorney (Financial)(Member and Spouse) — $85
- Power of Attorney (Medical)(Member and Spouse) — $85
- Power of Attorney (HIPAA)(Member and Spouse) — $85
- Advanced Medical Directive (Member and Spouse) — $65

**Wills**
- Last Will and Testament (Member and Spouse) — $185 — couple rate

### `will_individual`

**Shared**
- Power of Attorney (Financial) — $60
- Power of Attorney (Medical) — $60
- Power of Attorney (HIPAA) — $60
- Advanced Medical Directive — $45

**Will**
- Last Will and Testament — $150

### `individual_trust`

**Shared**
- Power of Attorney (Financial) — $60
- Power of Attorney (Medical) — $60
- Power of Attorney (HIPAA) — $60
- Advanced Medical Directive — $45

**Trust Claim**
- Last Will and Testament — $150
- Individual Trust No-Tax Planning — $325
- Affidavit — $65

*(optional, repeat per property)* **Realty Trust and Deed** — same as above

---

## MetLife Billing Name Cross-Reference

Always use MetLife terminology — not Aubrey Law internal names:

| Aubrey Law Name | MetLife Billing Name |
|----------------|----------------------|
| Durable Power of Attorney | Power of Attorney (Financial) |
| Health Care Proxy | Power of Attorney (Medical) |
| HIPAA Authorization | Power of Attorney (HIPAA) |
| Living Will | Advanced Medical Directive |
| Revocable Trust | Trust No-Tax Planning |
| Certificate of Trust | Affidavit |
| Minor Guardianship | Temporary Guardian Affidavit |

---

## Pricing Reference (Internal — April 2026)

| Document | Member Rate | Couple Rate |
|----------|-------------|-------------|
| Will | $150 | $185 |
| Trust (No-Tax Planning) | $325 | $400 |
| Advanced Medical Directive | $45 | $65 |
| Financial POA | $60 | $85 |
| Medical POA | $60 | $85 |
| HIPAA POA | $60 | $85 |
| Affidavit | $65 | $65 |
| Deed | $90 | $90 |

> All three POA types bill at the same rate per MetLife guidelines.

---

## Output Document Structure

The generated `.docx` includes:

- **Header**: METLIFE CLAIM, plan type subtitle
- **Info block**: Member ID, names, dates, and the calculated Total Claim
- **One table per section**, each containing:
  - Column 1: Checkbox (☐) for each line item
  - Column 2: MetLife billing document name
  - Column 3: Standard fee
  - Column 4: Descriptive comment (names, relationship)
  - **TOTAL row**: Sum of all fees in that section (calculated dynamically)
- **Grand Total** at the bottom right
- **Portal Submission Table**: Flat numbered list of all line items with Service Type,
  Fee, Comment, and Complete columns — used by the `submit-metlife-claim` skill

The document is formatted in Aubrey Law navy/blue.
