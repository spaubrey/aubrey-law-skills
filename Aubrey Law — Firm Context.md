**Single source of truth for visual standards, identity, and output paths.**  
All skills that produce client-facing or attorney work-product documents read  
from this file rather than hardcoding their own values.

---

## Firm Identity

|   |   |
|---|---|
|Field|Value|
|Firm name|Aubrey Law, LLC|
|Attorney|Scott Aubrey, Esq.|
|Email|[scott@aubreylegal.com](mailto:scott@aubreylegal.com)|
|Phone|(781) 474-3450|
|Website|aubreylegal.com|
|Street address|1329 Highland Ave, Suite 1A, Needham, MA 02492|

---

## Typography

|   |   |
|---|---|
|Element|Spec|
|Font (all documents)|Garamond|
|Body size|12pt (24 half-points in docx-js)|
|Footer size|10pt|
|Body color|`000000` (true black)|
|Body alignment|Justified (`AlignmentType.BOTH` in docx-js) for client-facing docs; left-aligned acceptable for attorney work product|

No fall-back fonts. No mixing in Arial except the unicode checkbox character `☐` (U+2610) which renders better in Arial 26pt for visual weight.

---

## Color Palette

The canonical pair, dominant across recent skills:

|                                             |          |
| ------------------------------------------- | -------- |
| Role                                        | Hex      |
| Navy — titles, primary headings             | `1B3A6B` |
| Teal — dividers, table header rows, accents | `0F6E56` |
| Body text, Section Headings                 | `000000` |
| Secondary / footer text                     | `555555` |
| Table header text (on teal)                 | `FFFFFF` |
| Footer top-border rule                      | `CCCCCC` |
| RED flag (review skill)                     | `C00000` |
| YELLOW flag (review skill)                  | `FFC000` |
| GREEN flag (review skill)                   | `70AD47` |

---

## Page Layout

|   |   |
|---|---|
|Element|Spec|
|Page size|US Letter — 12240 × 15840 DXA|
|Margins (most documents)|Top/Bottom 1080, Left/Right 1008 DXA (~0.75 in / 0.7 in)|
|Margins (engagement agreement)|1440 DXA all sides (1 in)|
|Margins (deed)|1440 top/bottom, 1080 left/right (1 in / 0.75 in) — Registry of Deeds standard|

---

## Header & Footer

The firm has **three distinct header/footer styles**, applied based on document audience.

### Style 1 — Branded (client-facing branded docs)

**Documents:** Closing Letter, Funding Instructions, Estate Plan Summary, Engagement Agreement, Review Memo (client-facing), Quitclaim Deed.

**Header:**

- Aubrey Law logo image, centered, no text.
    
- Logo source: see Logo Asset section below.
    
- Display size: cx ≈ 3,288,300 EMU × cy ≈ 610,636 EMU (~3.42 in × 0.63 in).
    
- docx-js transformation: `{ width: 320, height: 50 }`.
    

**Footer:**

- Top border `CCCCCC`.
    
- Centered 10pt Garamond: `1329 Highland Ave, Suite 1A, Needham, MA 02492 · (781) 474-3450 · aubreylegal.com`
    
- One non-breaking middot `·` between fields.
    

### Style 2 — Legal instrument (estate plan documents)

**Documents:** Last Will and Testament, Revocable Living Trust, Pour-Over Will, Durable Power of Attorney, Health Care Proxy, HIPAA Authorization, Advance Health Directive, Personal Property Memorandum, Assignment of Personal Property, Certificate of Trust, Realty Trust, Parental Appointment of Guardian, Temporary Delegation of Parental Powers.

**Header:** None.

**Footer (split):**

- Left-aligned: document title with principal's name. Format: `<Document Title> of <Principal Full Legal Name>` Examples:
    
    - `Last Will and Testament of Jane B. Smith`
        
    - `Durable Power of Attorney of Jane B. Smith`
        
    - `The Smith Family Revocable Trust` (matter-level — no principal name)
        
    - `Health Care Proxy of Jane B. Smith`
        
- Right-aligned: `Page N` (or `Page N of M` if total page count is straightforward to compute)
    
- 10pt Garamond, body color `000000`.
    
- No top border rule.
    

### Style 3 — Attorney work product

**Documents:** Attorney Review Workbook, MA Estate Tax Worksheet, Consultation Agenda. _(See firm-document-set.md §Estate Plan Proposal note for that doc's footer — it's branded since it's client-facing.)_

**Header:** "**CONFIDENTIAL — ATTORNEY WORK PRODUCT**" upper right, navy `1B3A6B`, bold, 10pt. _(Used on the Review Workbook only — not the Tax Worksheet or Agenda, which are simply attorney-only by audience but not legally protected in the same way.)_

**Footer:**

- Centered: `Page N`
    
- 10pt Garamond, body color `000000`.
    
- No top border rule.
    

### Footer cross-reference table

|   |   |
|---|---|
|Document|Footer style|
|Engagement Agreement|Branded|
|Consultation Agenda|Attorney work product (page number only)|
|Estate Plan Proposal|Branded _(client-facing)_|
|MA Estate Tax Worksheet|Attorney work product|
|One-Page Plan Summary|Branded|
|Last Will and Testament|Legal instrument (split)|
|Revocable Living Trust|Legal instrument (split)|
|Pour-Over Will|Legal instrument (split)|
|Durable Power of Attorney|Legal instrument (split)|
|Health Care Proxy|Legal instrument (split)|
|HIPAA Authorization|Legal instrument (split)|
|Advance Health Directive|Legal instrument (split)|
|Personal Property Memorandum|Legal instrument (split)|
|Assignment of Personal Property|Legal instrument (split)|
|Certificate of Trust|Legal instrument (split)|
|Parental Appointment of Guardian|Legal instrument (split)|
|Temporary Delegation of Parental Powers|Legal instrument (split)|
|Quitclaim Deed|Branded|
|Realty Trust|Legal instrument (split)|
|Trust Closing Letter|Branded|
|Trust Funding Instructions & Checklist|Branded|
|Estate Plan Summary|Branded|
|Attorney Review Workbook|Attorney work product (with confidential header)|
|Client Review Memo|Branded|

---

## Logo Asset

|                   |               |
| ----------------- | ------------- |
| Use               | Path          |
| Canonical PNG     |               |
| Source dimensions | 1400 × 220 px |

---

## Signature Asset

|                        |                                                            |
| ---------------------- | ---------------------------------------------------------- |
| Use                    | Path                                                       |
| Canonical PNG          |                                                            |
| Source dimensions      | 540 × 140 px, RGBA                                         |
| Display size           | cx ≈ 1,371,600 EMU × cy ≈ 360,000 EMU (~1.5 in × 0.39 in)  |
| docx-js transformation | `{ width: 144, height: 37 }`                               |
| Fallback if missing    | Underscore line `________________________________________` |


---

## Output Paths

|                                 |      |
| ------------------------------- | ---- |
| Use                             | Path |
| Working drafts during a session |      |
| Final delivery to client        |      |

---

