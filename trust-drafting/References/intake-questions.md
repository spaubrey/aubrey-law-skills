# Trust Drafting — Intake Questions

Load this reference during Step 1 to guide data collection.

---

## Pass 1 Questions (ask these first)

1. **Trust type**
   - Options: Individual Revocable Trust / Joint Revocable Trust

2. **Client full legal name** (free text)
   - For joint: client name AND spouse name

3. **Client address, city, county** (free text)
   - Must be a Massachusetts county for notary blocks

4. **Trust name** (free text)
   - Example: "The John A. Smith Revocable Trust"
   - Example (joint): "The John A. and Jane B. Smith Revocable Trust"

5. **Trust execution date** (free text or "TBD")
   - If TBD, leave a blank date line: `___________________, 20___`

6. **Children** (names, minor or adult)
   - If none: "No children"
   - If minors exist: also collect DOBs

7. **Successor trustee(s)** (name, relationship)
   - Primary successor, then alternate
   - For joint: typically surviving spouse is first; then named successor

8. **Personal representative / executor for Pour-Over Will**
   - Primary (and co-primary if any)
   - Successor (and co-successor if any)

---

## Pass 2 Questions (collect if not in claude.md)

9. **Initial co-trustee?** (Yes / No)
   - If yes: full name and relationship

10. **Guardian(s)** — only if minor children exist
    - Primary guardian name
    - Successor guardian name
    - Second successor guardian name
    - Any excluded guardians? (name and reason)

11. **Signing county** (for notary blocks)
    - Default: Norfolk County (Needham office)
    - Override if client is signing elsewhere

12. **Asset profile** (for checklist row suppression)
    - Does client have: out-of-state real estate? (Y/N)
    - Business interests? (Y/N)
    - Stock options / RSUs? (Y/N)
    - Oil/gas/mineral rights? (Y/N)
    - 529 plans? (Y/N)

---

## Pre-Fill Logic

If `claude.md` exists in the matter directory:
- Read it first
- Map known fields to the question list above
- Only ask questions that are not already answered
- Confirm ambiguous or partial answers before proceeding

---

## Placeholder Map

| Placeholder | Source |
|---|---|
| `[TRUST NAME]` | Trust name from intake |
| `[GRANTOR]` | Client full name |
| `[SPOUSE FULL NAME]` | Spouse name (joint only) |
| `[INITIAL CO-TRUSTEE]` | Co-trustee name (if any) |
| `[DocDate]` | Trust execution date |
| `[CLIENT ADDRESS]` | Client street address |
| `[CLIENT CITY]` | Client city |
| `[SIGNING COUNTY]` | County for notary |
| `[NotaryExpiration]` | Left blank — notary fills in |
| `[he/she]` | Pronoun per individual's gender |
| `{{ client.full_name }}` | Client full name (will template) |
| `{{ spouse.full_name }}` | Spouse full name (will template) |
| `{{ trust.name }}` | Trust name (will template) |
| `{{ trust.date }}` | Trust date (will template) |
| `{{ fiduciaries.executor.primary.full_name }}` | Primary executor |
| `{{ fiduciaries.executor.successor.full_name }}` | Successor executor |
| `{{ guardians.primary.full_name }}` | Primary guardian |
| `{{ guardians.successor.full_name }}` | Successor guardian |

---

## Output File Names

File name format: `YYYY-MM-DD_[Document-Name]_[CLIENT-LAST-NAME].docx`
- `YYYY-MM-DD` = today's date at time of generation
- No `_v1` suffix

| Document | File Name |
|---|---|
| Individual Revocable Trust | `YYYY-MM-DD_[Trust-Name]_[CLIENT-LAST-NAME].docx` |
| Joint Revocable Trust | `YYYY-MM-DD_[Trust-Name]_[CLIENT-LAST-NAME].docx` |
| Pour-Over Will (individual) | `YYYY-MM-DD_Pour-Over-Will_[CLIENT-LAST-NAME].docx` |
| Pour-Over Will (each spouse) | `YYYY-MM-DD_Pour-Over-Will_[FULL-NAME].docx` |
| Funding Instructions | `YYYY-MM-DD_Funding-Instructions_[CLIENT-LAST-NAME].docx` |
| Assignment of PP (individual) | `YYYY-MM-DD_Assignment-of-Personal-Property_[CLIENT-LAST-NAME].docx` |
| Assignment of PP (per spouse) | `YYYY-MM-DD_Assignment-of-Personal-Property_[FULL-NAME].docx` |
| Certificate of Trust | `YYYY-MM-DD_Certificate-of-Trust_[CLIENT-LAST-NAME].docx` |
