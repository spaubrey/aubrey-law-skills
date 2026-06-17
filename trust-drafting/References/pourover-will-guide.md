# Pour-Over Will — Drafting Guide

Load this reference when drafting the Pour-Over Will.

Source template: `Assets/pourover-will.docx`
Template engine: Nunjucks/Jinja2-style `{{ }}` and `{% %}` blocks.

---

## Document Identity

- **File name:**
  - Individual: `YYYY-MM-DD_Pour-Over-Will_[CLIENT-LAST-NAME].docx`
  - Joint (per spouse): `YYYY-MM-DD_Pour-Over-Will_[FULL-NAME].docx`
- **Page size:** US Letter (12240 × 15840 DXA)
- **Margins:** Top 1080, Bottom 1080, Left 1008, Right 1008 DXA
- **Font:** Garamond throughout, 12pt body, 14pt bold titles
- **Color:** Black `000000` only — no navy, no teal, no gray
- **Header:** None — no logo, no header image
- **Footer:** Plain black text, document title and page number

---

## Title

```
LAST WILL AND TESTAMENT OF [CLIENT FULL NAME]
```

Centered, Garamond, 14pt bold, black `000000`.

---

## Opening Declaration (verbatim, fill placeholders)

```
I, [CLIENT FULL NAME], a resident of [CLIENT CITY], [CLIENT COUNTY] County,
Massachusetts, revoke any prior Wills and codicils made by me and declare
this to be my Last Will and Testament.
```

---

## Article: Family Information

Fill in:
- Spouse name if married: `I am married to [SPOUSE FULL NAME].`
- Children: list each child's full name

Template conditional blocks to resolve:
- `{% if has_spouse %}` → include if married, omit if single
- `{% if has_children %}` → include if children exist
- `{% for child in children %}` → expand with each child's name

---

## Article: Distribution of My Property

### Section 2.01 — Tangible Personal Property
Use verbatim template language. No changes needed unless client has
specific tangible property instructions — flag for attorney review.

### Section 2.02 — Pour-Over to Revocable Trust
Resolve `{% if uses_revocable_trust %}` → always TRUE for this package.

Fill in:
- `{{ trust.name }}` → Full trust name
- `{{ trust.date }}` → Trust execution date (or blank line if TBD)

Resulting text:
```
I devise the residue of my estate to the Trustee then serving under the
[TRUST NAME] dated [DocDate], (hereinafter sometimes referred to as the
"Revocable Trust") executed immediately prior hereto of which I am the
Grantor and the present Trustee, to be added to the property held
thereunder and administered in accordance with the terms of the Revocable
Trust as the same shall exist at the time of my death and not as a trust
under this Last Will and Testament.
```

---

## Article: Nomination of Personal Representatives

Fill in from intake:
- `{{ fiduciaries.executor.primary.full_name }}` → Primary executor
- `{{ fiduciaries.executor.co_primary.full_name }}` → Co-primary executor
  (omit "and [co-primary]" clause if none named)
- `{{ fiduciaries.executor.successor.full_name }}` → Successor executor
- `{{ fiduciaries.executor.co_successor.full_name }}` → Co-successor
  (omit if none named)

If only one primary executor and one successor (no co-executors):
```
I nominate [PRIMARY EXECUTOR] to be the Personal Representative of this
my Last Will and Testament. In the event of a vacancy, I nominate
[SUCCESSOR EXECUTOR] to serve as Personal Representative.
```

---

## Article: Guardian Nomination

**Include this article ONLY if client has minor children.**

Resolve `{% if requires_guardian_clause %}` → TRUE if minor children exist.

Fill in:
- `{{ guardians.primary.full_name }}` → Primary guardian
- `{{ guardians.successor.full_name }}` → Successor guardian
- `{{ guardians.second_successor.full_name }}` → Second successor (if provided)
- `{{ guardians.excluded }}` → Excluded guardians list (if any)

If no minor children: omit the guardian article entirely.

---

## Execution / Signature Block

```
I, [CLIENT FULL NAME], the Testator, sign my name to this instrument this
_____ day of _____________, and being first duly sworn, do hereby declare
to the undersigned authority that I sign and execute this instrument as my
will and that I sign it willingly...

        ___________________________________
                [CLIENT FULL NAME], Testator
```

Two witness signature lines follow (witnesses fill in at signing).

---

## Witness Attestation Table

Render as a table with blank witness name/address cells.
See template source for exact format.

---

## Joint Trust: Two Wills

For a married couple, produce two separate Pour-Over Will documents:
1. Will for CLIENT → pours over to the joint trust
2. Will for SPOUSE → pours over to the same joint trust

Both wills reference the same trust name and date.
Each will names the other spouse as primary executor (unless overridden
by intake data).

---

## Self-Proved Affidavit (if applicable)

Some clients request a self-proved will affidavit. If requested:
- Add notary block after witness attestation
- Use standard MA self-proved will language
- Flag for attorney review: `[REQUIRES ATTORNEY REVIEW — self-proved affidavit requested]`

By default, do not include unless specifically requested.
