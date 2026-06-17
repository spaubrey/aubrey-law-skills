# HIPAA Authorization — Section Drafting Guide
# Source: Scott Aubrey / Aubrey Law actual template (HIPAA_v1.1.docx)
# Authority: 45 CFR §§ 160-164 (HIPAA Privacy Rule)

---

## MAJOR CHANGES FROM v1

The v2 template is dramatically simpler than v1. Key changes the generator
must account for:

- **Placeholder set reduced from 11 fields to 5** (no more spouse, no
  more client address, no more separate notary commission month/year)
- **Spouse clause REMOVED** — v1 had a `[SPOUSE FULL NAME]` placeholder
  and married/individual conditional logic. v2 has no spouse-specific
  clauses. The authorized recipients are HCP chain + DPOA chain +
  trustees only. `[IF_MARRIED]` / `[END_IF_MARRIED]` macros are no
  longer needed for HIPAA.
- **Client address REMOVED** — v1 had `[ADDRESS]` in the identification
  block. v2 identifies the client by name + DOB only.
- **Psychotherapy notes election REMOVED** — v1 had `___ I authorize
  disclosure` / `___ I do not authorize disclosure` opt-in/opt-out lines
  for psychotherapy notes. v2 has no separate election — psychotherapy
  notes are explicitly excluded from default disclosure ("mental illness
  (except psychotherapy notes)") and there is no opt-in mechanism in the
  template itself. If a client specifically wants to authorize
  psychotherapy notes disclosure, flag to Scott for manual customization.
- **Numbered section labels REMOVED** — v1 had numbered paragraphs (1.,
  2., 3., ...). v2 has flat bold lead-ins (`Identity of Person...`,
  `Description of Information...`, `Person or Class of Persons...`,
  etc.).
- **TR_ styles applied throughout** — body paragraphs now use `TR_Body1`,
  `TR_Agr1`, `TR_Body3`, `TR_SigLine`, `TR_SigName`, `TR_Base`, and
  `TR_Title`. v1 used Normal for body text. This brings HIPAA to
  DPOA-level brand consistency.

---

## PRODUCTION RULES (apply when emitting the document)

### Placeholder set

| Placeholder | Source | Notes |
|---|---|---|
| `[CLIENT]` | client.full_legal_name | UPPERCASE plain text. Appears in title block (P1, P4, P20) and notary block (P24). |
| `[Client DOB]` | client.date_of_birth | e.g., `January 15, 1962`. Appears only in the identification block (P5). |
| `[DocDate]` | document execution date | Appears in P18 ("Dated:") and P24 (notary acknowledgement). For unscheduled signings, leave as ` ____________ `. |
| `[Notary Commission]` | notary commission expiration date | Leave blank — populated at signing. Appears in P29. |
| `[client he/she]` | client subject pronoun | lowercase: `he` or `she`. Appears in principal notary acknowledgement (P24). |
| `[SIGNING COUNTY]` | client county OR the county where signing occurs | **UPPERCASE** (e.g., "NORFOLK", "MIDDLESEX"). Appears in notary block (P23). |

That's the complete placeholder set — six total.

**No conditional macros.** v2 does not use any `[IF_X]` / `[END_IF_X]`
markers.

### Document-specific formatting

- **TR_ styles applied to body** — `TR_Title` for the title and the
  identification subheader; `TR_Body1` for opening declarations and the
  date; `TR_Agr1` for the operative agreement paragraphs (Identity,
  Description, Person/Class, Purpose, Termination, Re-Disclosure, Right
  to Treatment, Instructions, Revocation, Valid Document, Waiver and
  Release, Copy); `TR_Body3`, `TR_Base`, `TR_SigLine`, `TR_SigName` for
  the signature and notary blocks.
- **Single notary block** — Principal only. HIPAA does not require
  witnesses, only notarization. No witness signature tables.
- **NO HEADER TABLES** — entire document is paragraph-based. Zero
  tables. (HCP and Living Will have witness signature tables; HIPAA does
  not.)
- **`[client he/she]` pronoun convention** — lowercase, options visible.
  Matches HCP_v2 convention.

---

## TITLE (P0)

```
AUTHORIZATION FOR RELEASE OF PROTECTED HEALTH INFORMATION
```

Style: `TR_Title`. Centered, bold, all caps.

---

## OPENING DECLARATION (P1)

Style: `TR_Body1`.

```
I, [CLIENT], intend this authorization to comply, now and in the future,
with all requirements set forth in the Standards for Privacy of
Individually Identifiable Health Information (known as the "Privacy
Rule") which implements the privacy requirements of the Health Insurance
Portability and Accountability Act of 1996 (Pub L 104-191, 110 Stat
1936; 45 CFR Sections 160-164), commonly known as "HIPAA," so that the
information described below will be freely available to those described
below. All provisions hereof shall be construed in accordance with that
intent.
```

---

## AUTHORIZATION DECLARATION (P2)

Style: `TR_Body1`.

```
I hereby authorize each Covered Entity identified below to disclose my
individually identifiable health information as described below, which
may include information concerning communicable diseases such as Human
Immunodeficiency Virus ("HIV") and Acquired Immune Deficiency Syndrome
("AIDS"), mental illness (except psychotherapy notes), chemical or
alcohol dependency, laboratory test results, medical history, treatment,
or any other such related information.
```

Note: "mental illness (except psychotherapy notes)" — psychotherapy
notes are explicitly excluded. There is no in-template mechanism to
opt-in to psychotherapy notes disclosure.

---

## ADDITIONAL IDENTIFICATION (P3–P5)

Style for header (P3): `TR_Title`.

```
My Additional Identification Information:
```

Style for `Name:` line (P4): `TR_SigName`.

```
Name: [CLIENT]
```

Style for `Date of Birth:` line (P5): `TR_Base`.

```
Date of Birth: [Client DOB]
```

No address field — v1's `[ADDRESS]` placeholder has been removed.

---

## OPERATIVE PROVISIONS (P6–P17)

All operative paragraphs use style `TR_Agr1`. Each has a bold lead-in
phrase followed by the body.

**P6 — Identity of Disclosing Parties:**
```
Identity of Person or Class of Persons Authorized to Make Disclosure.
I hereby authorize all covered entities as defined in HIPAA, and all
other health care providers, health plans, and health care
clearinghouses, including but not limited to each and every doctor,
psychiatrist, psychologist, dentist, therapist, nurse, hospital, clinic,
pharmacy, laboratory, ambulance service, assisted living facility,
residential care facility, bed and board facility, nursing home, medical
insurance company or any other medical provider or agent thereof having
protected health information (as that term is defined in HIPAA), each
being referred to herein as a "Covered Entity," to disclose the
information set forth in the following paragraph.
```

**P7 — Description of Information:**
```
Description of Information to Be Disclosed. The person or persons
identified in the preceding paragraph may disclose the following
information: All health care information, reports and/or records
concerning my medical history, condition, diagnosis, testing, prognosis,
treatment, billing information and identity of health care providers,
whether past, present or future and any other information which is in
any way related to my health care. Additionally, this disclosure shall
include the ability to ask questions and discuss this protected medical
information with the person or entity who has possession of the
protected medical information even if I am fully competent to ask
questions and discuss this matter at the time. It is my intention to
give a full authorization to ANY protected medical information to the
persons named in this Authorization.
```

**P8 — Authorized Recipients (NO SPOUSE CLAUSE in v2):**
```
Person or Class of Persons to Whom the Covered Entity May Disclose the
Above Described Protected Health Information. The above described
information shall be disclosed to any Health Care Proxy acting or
designated to act (whether named as a primary or alternate Health Care
Proxy) in my Health Care Proxy, any Attorney-in-Fact acting or
designated to act (whether named as a primary or alternate Attorney-in-
Fact) in my Durable General Power of Attorney, and any trustee or
successor trustee acting or designated to act with respect to any trust
of which I am named as a beneficiary or trustee each known herein as an
"Authorized Person."
```

The authorized recipients are:
1. HCP chain (primary + alternate)
2. DPOA chain (primary + alternate AIFs)
3. Trustees (current and successor) of any trust where the principal is
   a beneficiary or trustee

No explicit spouse clause. If a client wants the spouse named explicitly
(separate from the HCP/DPOA/trustee chains), flag to Scott for manual
customization.

**P9 — Purpose:**
```
Purpose of Disclosure. At my request.
```

**P10 — Termination:**
```
Termination. This Authorization shall terminate on the first to occur
of: (1) two years following my death or (2) upon my written revocation
actually received by the Covered Entity. Proof of receipt of my written
revocation may be either by certified mail, registered mail, facsimile,
or any other receipt evidencing actual receipt by the Covered Entity.
Such revocation shall be effective upon the actual receipt of the notice
by the Covered Entity except to the extent that the Covered Entity has
taken action in reliance on this Authorization.
```

**P11 — Re-Disclosure:**
```
Re-Disclosure. By signing this Authorization, I acknowledge that the
information used or disclosed pursuant to this Authorization may be
subject to re-disclosure by the Authorized Person and the information
once disclosed will no longer be protected by the rules created in
HIPAA. No Covered Entity shall require my authorized persons to
indemnify the Covered Entity or agree to perform any act in order for
the Covered Entity to comply with this Authorization.
```

**P12 — Right to Treatment:**
```
Acknowledgement of Right to Treatment. I understand and hereby
acknowledge that the Covered Entities may not condition my receipt of
health care upon my execution of this Authorization, and I may refuse
to sign this Authorization if I wish to do so.
```

**P13 — Instructions to Authorized Persons:**
```
Instructions to My Authorized Persons. My Authorized Person shall have
the right to bring a legal action in any applicable forum against any
Covered Entity that refuses to recognize and accept this Authorization
for the purposes that I have expressed. Additionally, my Authorized
Person is authorized to sign any documents that the Authorized Person
deems appropriate to obtain the protected medical information.
```

**P14 — Revocation:**
```
Revocation. This Authorization may be revoked in writing by me at any
time.
```

**P15 — Valid Document:**
```
Valid Document. A copy or facsimile of this original Authorization shall
be accepted as though it was an original document.
```

**P16 — Waiver and Release:**
```
My Waiver and Release. I hereby release any Covered Entity that acts in
reliance on this Authorization from any liability that may accrue from
releasing my protected medical information and for any actions taken by
my Authorized Person. I also specifically prohibit my Authorized Person,
or any other person designated as my agent in any capacity from filing
a complaint of any kind against any Covered Entity that complies with
the directions of my Authorized Person hereunder to the extent that
such a complaint purports to charge said Covered Entity with any
violation of the Privacy Rules or other Federal or State laws related
to disclosure of medical records as a result of their compliance with
said directions.
```

**P17 — Copy:**
```
Copy. I understand that I have a right to receive a copy of this
Authorization.
```

---

## EXECUTION BLOCK (P18–P20)

**P18 — Date** (style `TR_Body1`):
```
Dated: [DocDate]
```

**P19 — Signature line** (style `TR_SigLine`):
```
__________________________________
```

**P20 — Printed name** (style `TR_SigName`):
```
[CLIENT]
```

---

## NOTARY BLOCK (P22–P29)

**P22 — Commonwealth header** (style `Text Heading 2`):
```
COMMONWEALTH OF MASSACHUSETTS
```

**P23 — County line** (style `Normal`):
```
COUNTY OF [SIGNING COUNTY]
```

**P24 — Acknowledgement** (style `TR_Body3`):
```
On [DocDate], before me, the undersigned notary public, personally
appeared
[CLIENT], ___ personally known to me, or ___ proved to me through
satisfactory evidence of identification, which was a government-issued
photo identification, to be the person whose name is signed on the
preceding or attached document, and who acknowledged that [client he/she]
signed it voluntarily for its stated purpose.
```

The line break between "personally appeared" and "[CLIENT]" is a proper
soft line break (`<w:br/>`), NOT a literal `\n` defect — preserve as-is.

**P25 — Witness phrase** (style `TR_Body3`):
```
WITNESS my hand and notarial seal.
```

**P26 — Seal placeholder** (style `TR_Base`):
```
(SEAL)
```

**P27 — Notary signature line** (style `TR_SigLine`):
```
______________________________________
```

**P28 — Notary label** (style `TR_SigName`):
```
Notary Public
```

**P29 — Commission expiration** (style `TR_SigName`):
```
My Commission Expires: [Notary Commission]
```

Note: P29 uses `TR_SigName`, NOT `Text Heading 2` (which was a v1
inconsistency). In v2 this paragraph is its own properly-styled line.

---

## QUALITY CHECKLIST (HIPAA-specific)

**Run the three-item pre-delivery scan from SKILL.md Step 5a–5c first:**
- [ ] **Footer** — HIPAA footer is static text only (`AUTHORIZATION FOR RELEASE OF
      PROTECTED HEALTH INFORMATION`); no `[CLIENT]` placeholder. Confirm footer
      text is intact but no substitution needed.
- [ ] **Document date** — `[DocDate]` resolved or replaced with `____________` in
      the Dated line (P18) AND the notary block (P24); no literal bracket tag remains.
- [ ] **Signing county** — `[SIGNING COUNTY]` resolved to UPPERCASE county name in
      the notary block; no literal bracket tag remains.

**Then run the full checklist:**
- [ ] Title verbatim: AUTHORIZATION FOR RELEASE OF PROTECTED HEALTH
      INFORMATION
- [ ] No literal placeholder brackets remain (`[CLIENT]`, `[Client DOB]`,
      `[DocDate]`, `[Notary Commission]`, `[client he/she]`,
      `[SIGNING COUNTY]`) — all resolved or, if intentionally left blank
      for signing, replaced with underscored blanks
- [ ] **`[SIGNING COUNTY]` value is UPPERCASE** (e.g., "NORFOLK", "MIDDLESEX")
- [ ] **`[CLIENT]` name is UPPERCASE plain text** — no bold on name value
- [ ] No `[SPOUSE FULL NAME]` placeholder — that was v1; v2 has no
      spouse-specific clause
- [ ] No `[ADDRESS]` placeholder — that was v1; v2 has no client address
      in the identification block
- [ ] No numbered section labels (1., 2., 3., ...) — those were v1; v2
      uses flat bold lead-ins
- [ ] No psychotherapy notes election lines (`___ I authorize
      disclosure...` / `___ I do not authorize...`) — those were v1; v2
      excludes psychotherapy notes by default
- [ ] Notary county line reads `COUNTY OF [SIGNING COUNTY]` —
      placeholder is resolved at generation time to the actual signing
      county (UPPERCASE)
- [ ] `[client he/she]` resolved to "he" or "she" (lowercase) per
      principal's gender
- [ ] No witnesses required for HIPAA (notarization only) — verify the
      output document does NOT include witness signature blocks
- [ ] All operative provisions (P6–P17) present with `TR_Agr1` style and
      correct bold lead-ins
- [ ] Termination clause includes "two years following my death" and
      written-revocation provision
