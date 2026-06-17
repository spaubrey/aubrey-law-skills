# Health Care Proxy — Section Drafting Guide
# Source: Scott Aubrey / Aubrey Law actual template (HCP_v1.1.docx)
# Authority: M.G.L. c. 201D

---

## PRODUCTION RULES (apply when emitting the document)

### Placeholder set

The template uses DPOA-style bracketed placeholders. Resolve every one of
these before emitting. Any unresolved placeholder is a defect.

| Placeholder | Source | Notes |
|---|---|---|
| `[CLIENT]` | client.full_legal_name | UPPERCASE plain text everywhere |
| `[Street Address]` | client.street_address | Title case |
| `[City]` | client.city | Title case |
| `[SIGNING COUNTY]` | client county OR the county where signing occurs | **UPPERCASE** |
| `[Ordinal_DocDate]` | principal signing date (ordinal form) | e.g., `21st day of May, 2025`. For unscheduled signings, leave as `_____ day of _________________, 20___`. Appears on the principal signing line only. |
| `[DocDate]` | notary acknowledgement date | e.g., `May 21, 2025`. For unscheduled signings, leave as `________________, 20__`. Appears in both notary blocks (principal + witness). |
| `[Notary Commission]` | notary commission expiration date | Leave blank — populated at signing. Appears in both notary blocks. |
| `[client he/she]` | client subject pronoun | lowercase. e.g., `he` or `she`. Appears in principal notary acknowledgement |

### HCP fiduciary placeholders

The template includes one primary HCP and ONE alternate HCP (v1 had two
alternates; v2 reduced to one).

**Primary HCP block:**
| Placeholder | Source |
|---|---|
| `[PRIMARY HCP FULL NAME]` | primary.full_name (UPPERCASE) |
| `[Primary HCP Relationship]` | primary.relationship (e.g., "Wife", "Son") — **plain text, NOT bold** |
| `[Primary HCP Full Address]` | primary.address (full single-line) |
| `[Primary HCP Phone]` | primary.phone |

**Alternate HCP block:**
| Placeholder | Source |
|---|---|
| `[ALTERNATE 1 HCP FULL NAME]` | alternate.full_name (UPPERCASE) |
| `[Alternate 1 HCP Relationship]` | alternate.relationship — **plain text, NOT bold** |
| `[Alternate 1 HCP Full Address]` | alternate.address |
| `[Alternate 1 HCP Phone]` | alternate.phone |

`[PRIMARY HCP FULL NAME]` also appears in the body paragraph (P8) that
introduces the alternate: "If [PRIMARY HCP FULL NAME] not available..."

**No conditional macros.** v2 does not use any `[IF_X]` / `[END_IF_X]`
markers.

### Document-specific formatting

- **No letter-prefix section headings** — v1 had `A. HEALTH CARE PROXY`,
  `B. APPOINTMENT OF HEALTH CARE AGENT`, `C. POWERS GIVEN`, etc. v2 has
  flat bold lead-ins: `HEALTH CARE PROXY.`, `APPOINTMENT OF HEALTH CARE
  AGENT.`, `POWERS GIVEN TO HEALTH CARE AGENT.`, `REVOCATION.`,
  `REIMBURSEMENT.`, `GOVERNING LAW.`, `PHOTOCOPIES.`, `SEVERABILITY.`,
  `VALIDITY IN ALL STATES AND COUNTRIES.`
- **Anatomical Gift Election is hardcoded ON** — single paragraph (P30)
  reads: "Upon my death, I give any needed organs, tissues or parts. My
  gift is for any purpose." No election lines, no opt-out. v1's three-
  option election (any-lawful / specified / decline) is gone.
- **Two witness signature tables** (Tables 0 and 1, each 2×3) — same
  layout as Living Will v2: "of [CITY], [STATE]" / "________, Witness" /
  "Address" cells.
- **Two notary blocks**: Principal (P48–P55) and Witnesses (P66–P73). Both
  use `[DocDate]` and `[Notary Commission]`. The principal notary block
  uses `[client he/she]` for the pronoun.
- **"[Remainder of page intentionally left blank]" marker** appears on P39
  before the execution block. Preserve verbatim.
- **TR_ styles partially applied** — body paragraphs use `Normal` or
  `List Paragraph`; notary block uses `TR_Body3`, `TR_Base`, `TR_SigLine`,
  `TR_SigName`. The Title (P0) is `Normal` with manual bold (not
  `TR_Title`).

---

## TITLE

```
MASSACHUSETTS HEALTH CARE PROXY OF [CLIENT]
```

Centered, bold, all caps. Currently uses `Normal` style with manual bold
character formatting.

---

## OPENING DECLARATION (P1)

```
I, [CLIENT] (the Principal), residing at [Street Address], [City],
Massachusetts, being a competent adult at least eighteen (18) years of
age or older, of sound mind and under no constraint or undue influence,
hereby appoint the following person to be my Health Care Agent
(hereinafter referred to as "Health Care Agent" or "Agent") under the
terms of this document:
```

---

## HEALTH CARE PROXY SECTION (P2)

Bold lead-in: `HEALTH CARE PROXY.`

```
I intend to create a Health Care Proxy according to Chapter 201D of the
General Laws of Massachusetts. In making this appointment, I am giving
my Health Care Agent the authority to make any and all health care
decisions on my behalf, subject to any limitations I state in this
document, in the event that I should at some future time become incapable
of making health care decisions for myself.
```

---

## APPOINTMENT OF HEALTH CARE AGENT (P3–P12)

Bold lead-in (P3): `APPOINTMENT OF HEALTH CARE AGENT.`

**Primary HCP (P4–P7):**
```
Name:  [PRIMARY HCP FULL NAME]
Relationship:  [Primary HCP Relationship]
Address: [Primary HCP Full Address]
Telephone:  [Primary HCP Phone]
```

> **Formatting note:** `Name:`, `Relationship:`, `Address:`, `Telephone:` labels follow the template's style.
> The **Relationship value** (e.g., "Wife", "Son") must be **plain text — NOT bold**.
> The name value `[PRIMARY HCP FULL NAME]` must be **UPPERCASE plain text** (no bold).

**Alternate transition (P8):**
```
If [PRIMARY HCP FULL NAME] not available, willing or competent to serve
and is not expected to become available, willing or competent to make a
timely decision given my medical circumstances, or in the event that my
original Health Care Agent is disqualified from acting on my behalf,
then I designate the individuals listed below as alternate Healthcare
Proxys, to serve in the order in which their names appear.
```

(Note: text says "individuals listed below" / "in the order in which
their names appear" but only ONE alternate is provided. If you want
multiple alternates, this is a template defect — flag to Scott.)

**Alternate HCP (P9–P12):**
```
Name:  [ALTERNATE 1 HCP FULL NAME]
Relationship:  [Alternate 1 HCP Relationship]
Address: [Alternate 1 HCP Full Address]
Telephone:  [Alternate 1 HCP Phone]
```

> **Formatting note:** The **Relationship value** (e.g., "Daughter", "Friend") must be **plain text — NOT bold**.
> The name value `[ALTERNATE 1 HCP FULL NAME]` must be **UPPERCASE plain text** (no bold).

---

## POWERS GIVEN TO HEALTH CARE AGENT (P13–P29)

Bold lead-in (P13): `POWERS GIVEN TO HEALTH CARE AGENT.`

A series of operative paragraphs covering: scope of authority (P14);
capacity determination by attending physician (P15); cessation/
recommencement on capacity restoration (P16); notification of capacity
determination (P17); consultation requirement (P18); discussion with
principal when possible (P19); immediate authority for HIPAA records
(P20); priority over other decision-makers including DPOA agent (P21);
principal's objection prevails unless court order (P22); comfort care
not precluded (P23); limitations clause (P24); agent liability waiver
(P25); facility/insurance contracting authority (P26); medical personnel
hiring (P27); consent to or withholding of procedures including life-
sustaining (P28); receipt of personal property (P29).

Read `HCP_v1.1.docx` for verbatim wording of each paragraph.

---

## ANATOMICAL GIFT (P30)

```
Upon my death, I give any needed organs, tissues or parts. My gift is
for any purpose.
```

**Hardcoded ON.** No election lines, no opt-out, no `client.anatomical_gift`
field used (the field exists on the design sheet but is no longer
operative for HCP — anatomical gift is always opt-in for any lawful
purpose). If a specific client wants different election language,
flag to Scott for manual customization.

---

## REVOCATION (P31–P33)

Bold lead-in: `REVOCATION.`

```
This Health Care Proxy shall be revoked upon any one of the following
events:

My execution of a subsequent Health Care Proxy;

My notification to my Health Care Agent or a health care provider orally
or in writing or by any other act evidencing a specific intent to revoke
the Health Care Proxy.
```

---

## REIMBURSEMENT (P34)

Bold lead-in: `REIMBURSEMENT.`

```
My Health Care Agent will be reimbursed for all costs and expenses
reasonably incurred.
```

---

## GOVERNING LAW (P35)

Bold lead-in: `GOVERNING LAW.`

```
This document shall be governed by the laws of the Commonwealth of
Massachusetts in all respects, including its validity, construction,
interpretation, and termination. I intend for this Health Care Proxy
to be honored in any jurisdiction where it may be presented and for any
such jurisdiction to refer to Massachusetts law to interpret and
determine the validity of this document and any of the powers granted
under this document.
```

---

## PHOTOCOPIES (P36)

Bold lead-in: `PHOTOCOPIES.`

```
My Health Care Agent is authorized to make photocopies of this document
as frequently and in such quantity as my Health Care Agent shall deem
appropriate. All photocopies shall have the same force and effect as
any original.
```

---

## SEVERABILITY (P37)

Bold lead-in: `SEVERABILITY.`

```
If any part of any provision of this document shall be invalid or
unenforceable under applicable law, such part shall be ineffective to
the extent of such invalidity only, without in any way affecting the
remaining part of such provision or the remaining provisions of this
document.
```

---

## VALIDITY IN ALL STATES AND COUNTRIES (P38)

Bold lead-in: `VALIDITY IN ALL STATES AND COUNTRIES.`

```
This instrument is executed and delivered in the Commonwealth of
Massachusetts, and the laws of the Commonwealth of Massachusetts shall
govern all questions as to the validity of this power and the
construction of its provisions. Nevertheless, I intend that this
instrument be given full force and effect in any state or country in
which I may find myself or in which my Health Care Agent finds it
necessary or desirable, in his or her discretion, to exercise powers
granted herein. I make note that in light of my travel and property,
now owned or hereafter acquired in any jurisdiction, I may choose to
execute additional Health Care Proxies or Durable Powers of Attorney
for Health Care to be governed under the laws of other jurisdictions.
In that event, it is my intent that this Health Care Proxy shall remain
in full force and effect concurrently with such subsequent documents
unless this Health Care Proxy is revoked in writing by express reference
to this instrument. Such additional instruments shall not affect my
intention that this instrument be honored in all jurisdictions.
```

---

## PAGE LAYOUT MARKER (P39)

```
[Remainder of page intentionally left blank]
```

---

## SIGNATURE OF PRINCIPAL (P41–P44)

```
SIGNATURE OF PRINCIPAL

I sign this Health Care Proxy on this [Ordinal_DocDate],
in the presence of two witnesses, neither of whom is my Health Care
Agent or Alternate Health Care Agent.


__________________________________
[CLIENT], Principal
```

`[Ordinal_DocDate]` — ordinal long form, e.g. "21st day of May, 2025".
For unscheduled signings resolve to `_____ day of _________________, 20___`.
The notary blocks use `[DocDate]` (short form); the signing line uses `[Ordinal_DocDate]`.

---

## PRINCIPAL NOTARY BLOCK (P48–P55)

```
COMMONWEALTH OF MASSACHUSETTS
COUNTY OF [SIGNING COUNTY]

On [DocDate], before me, the undersigned notary public, personally
appeared
[CLIENT], ___ personally known to me, or ___ proved to me through
satisfactory evidence of identification, which was a government-issued
photo identification, to be the person whose name is signed on the
preceding or attached document, and who acknowledged that [client he/she]
signed it voluntarily for its stated purpose.

WITNESS my hand and notarial seal.

(SEAL)
                                            ______________________________________
                                            Notary Public
                                            My Commission Expires: [Notary Commission]
```

Notary block uses TR_ styles correctly. The line break between
"personally appeared" and "[CLIENT]" is a proper soft line break
(`<w:br/>`), NOT a literal `\n` defect — preserve as-is.

For unscheduled signings, `[DocDate]` resolves to `________________, 20__` and
`[Notary Commission]` stays blank.

---

## WITNESSES SECTION (P59–P64)

```
WITNESSES

We, __________________________, __________________________, the
undersigned, have witnessed the execution of this document by the
Principal or at the direction of the Principal and state that the
Principal appears to be at least eighteen (18) years of age, of sound
mind and under no constraint or undue influence. We have not been named
as Health Care Agent or Alternate Health Care Agent in this document.
```

**Witness signature blocks** — Tables 0 and 1 (each 2×3):
- Row 0, Col 1: "of"
- Row 1, Col 0: signature blank + ", Witness"
- Row 1, Col 2: "Address"

Witness names and addresses NOT collected as placeholders — fill in at
signing.

---

## WITNESS NOTARY BLOCK (P66–P73)

```
COMMONWEALTH OF MASSACHUSETTS
COUNTY OF [SIGNING COUNTY]

On [DocDate], before me, the undersigned notary public,
___________________________ and ___________________________ personally
appeared, proved to me through satisfactory evidence of identification,
which were a government-issued photo identification, to be the persons
who signed the preceding or attached document in my presence and who
swore or affirmed to me that the contents of the document are truthful
and accurate to the best of their knowledge and belief.

WITNESS my hand and notarial seal.

(SEAL)
                                            ______________________________________
                                            Notary Public
                                            My Commission Expires: [Notary Commission]
```

End of HCP document. The witness notary block (P66–P73) is the final
content — no trailing preferences section.

---

## QUALITY CHECKLIST (HCP-specific)

**Run the three-item pre-delivery scan from SKILL.md Step 5a–5c first:**
- [ ] **Footer** — `footer1.xml` reads `MASSACHUSETTS HEALTH CARE PROXY OF [CLIENT NAME IN CAPS]`
      with `[CLIENT]` resolved. Inspect `footer1.xml` directly — not covered by body scan.
- [ ] **Signing line date** — `[Ordinal_DocDate]` resolved to ordinal form
      (e.g., "21st day of May, 2025") or replaced with
      `_____ day of _________________, 20___` for unscheduled signings;
      no literal bracket tag or hardcoded blanks remain.
- [ ] **Notary block dates** — `[DocDate]` resolved or replaced with
      `____________` in both notary blocks (principal + witness); no literal
      bracket tag remains.
- [ ] **Signing county** — `[SIGNING COUNTY]` resolved to UPPERCASE county name in
      BOTH notary blocks (principal + witness); no literal bracket tag remains.

**Then run the full checklist:**
- [ ] Title verbatim: MASSACHUSETTS HEALTH CARE PROXY OF [CLIENT in
      UPPERCASE]
- [ ] No literal placeholder brackets remain (`[CLIENT]`,
      `[Street Address]`, `[City]`, `[SIGNING COUNTY]`, `[DocDate]`,
      `[Notary Commission]`, `[client he/she]`, all 8 fiduciary
      placeholders) — all resolved or, if intentionally left blank for
      signing, replaced with underscored blanks
- [ ] **`[SIGNING COUNTY]` value is UPPERCASE** (e.g., "NORFOLK", "MIDDLESEX")
- [ ] **Relationship values are plain text, NOT bold** — applies to both
      Primary HCP and Alternate HCP Relationship fields
- [ ] **All names (CLIENT, PRIMARY HCP FULL NAME, ALTERNATE 1 HCP FULL NAME)
      are UPPERCASE plain text** — no bold on name values
- [ ] Section labels use flat bold lead-ins (`HEALTH CARE PROXY.`,
      `APPOINTMENT OF HEALTH CARE AGENT.`, etc.) — NOT letter prefixes
      (A., B., C.) which were v1 style
- [ ] Anatomical Gift section reads "Upon my death, I give any needed
      organs, tissues or parts. My gift is for any purpose." — no
      election lines, no opt-out
- [ ] Only ONE alternate HCP block in the appointment section (NOT two —
      template defect would be multiple alternates)
- [ ] All operative power paragraphs (P13–P29) present
- [ ] Both notary blocks present with `[SIGNING COUNTY]` correctly
      substituted
- [ ] Witness clause says "neither of whom is my Health Care Agent or
      Alternate Health Care Agent" — witnesses must be disqualified per
      MGL c. 201D
- [ ] No embedded HEALTHCARE PREFERENCES section trailing the witness
      notary block — the preferences worksheet is a separate document
- [ ] Two witness signature tables preserved (2×3 each)
- [ ] "[Remainder of page intentionally left blank]" marker preserved
      before SIGNATURE OF PRINCIPAL section
- [ ] Witness disqualification: witnesses MAY NOT be the Health Care
      Agent or any Alternate Health Care Agent (statutory)
- [ ] `[client he/she]` resolved to "he" or "she" (lowercase) per
      principal's gender
