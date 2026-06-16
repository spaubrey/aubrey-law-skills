# Advance Directive — Section Drafting Guide
# Source: Scott Aubrey / Aubrey Law actual template (Living_Will_v1.1.docx)
# Authority: M.G.L. c. 201D-adjacent (common-law Living Will / Advance Directive
# in Massachusetts — not statutorily codified the way the HCP is)

---

## PRODUCTION RULES (apply when emitting the document)

### Placeholder set

The template uses DPOA-style bracketed placeholders (consistent with the
DPOA convention). Resolve every one of these before emitting. Any
unresolved placeholder is a defect.

| Placeholder | Source | Notes |
|---|---|---|
| `[CLIENT]` | client.full_legal_name | UPPERCASE plain text everywhere it appears (title, body, signature footer, notary acknowledgement) |
| `[City]` | client.city | Title case |
| `[SIGNING COUNTY]` | client county OR the county where signing occurs | Title case |
| `[DocDate]` | notary acknowledgement date | e.g., `May 21, 2025`. For unscheduled signings, leave as ` ____________ `. Appears twice (principal notary block AND witness notary block). |
| `[Notary Commission]` | notary commission expiration date | Leave blank ` ____________ ` — populated by notary at signing. Appears twice. |
| `[Client Pronoun]` | client subject pronoun | `he` or `she` (lowercase). Appears once in the principal notary acknowledgement (P19): "acknowledged that [Client Pronoun] signed it voluntarily" |
| `[Client HisHer]` | client possessive pronoun | `his` or `her` (lowercase). Appears four times in the witness affirmations clause (P28): "at [Client HisHer] request," "in [Client HisHer] presence," "for or at [Client HisHer] direction," "upon [Client HisHer] death" |

**No conditional macros.** AHD content does not vary by client marital
status, agent configuration, etc.

### Document-specific formatting

- **Three tables in the body**: Table 0 (2×2) is the principal signature
  block — `[CLIENT]` appears in cell [1,1]. Table 1 (2×3) is the first
  witness signature block. Table 2 (2×3) is the second witness signature
  block. Witness tables contain the structure "of [CITY], [STATE]" in row
  0 and "________, Witness" / "Address" in row 1.
- **No article headings** — v2 is flat prose. Do NOT add ARTICLE 1./
  ARTICLE 2. headings. The structure flows logically without explicit
  section labels.
- **"[Remainder of page intentionally left blank]" marker** appears on P10
  before the execution block. This is a layout cue indicating a soft page
  break before the signing section. Preserve verbatim.
- **Two notary blocks**: one for the Principal (P16–P24), one for the
  Witnesses (P31–P38). Both use `[DocDate]` and `[Notary Commission]`.

---

## TITLE

```
ADVANCE DIRECTIVE OF [CLIENT]
```

Centered, bold, all caps. Currently uses `Normal` style with manual bold
character formatting — Scott's broader convention is `TR_Title`.

Note the v1→v2 change: "ADVANCE HEALTH DIRECTIVE" was shortened to
"ADVANCE DIRECTIVE."

---

## OPENING DECLARATION

```
I, [CLIENT] of [City], Massachusetts ("Principal"), willfully and
voluntarily make known my desire under the circumstances set forth below,
and I do hereby declare:
```

Single paragraph. Body text style.

---

## DIRECTION TO HEALTH CARE PROXY AGENT AND PROVIDERS

```
If I am incapable of making an informed decision regarding my health care,
I direct my Health Care Agent under a duly executed Health Care Proxy or
my health care providers, as the case may be, to follow my instructions
as set forth below:
```

This is the bridging clause that grants instructional authority. Single
paragraph. Body text style.

---

## THREE TRIGGERING CONDITIONS

Three consecutive paragraphs, each defining a triggering condition followed
by the same directive ("I direct that my life not be extended by
life-sustaining procedures, including the administration of nutrition and
hydration artificially, unless necessary for the relief of my pain or for
my comfort.").

### Terminal condition (P3)
```
If my death from a terminal condition (i.e. an incurable condition caused
by injury, disease, or illness which, to a reasonable degree of medical
certainty, makes death imminent and from which, despite the application
of life-sustaining procedures, there can be no recovery) is imminent,
I direct that my life not be extended by life-sustaining procedures
including the administration of nutrition and hydration artificially,
unless necessary for the relief of my pain or for my comfort.
```

### Persistent vegetative state (P4)
```
If I am in a persistent vegetative state (i.e. a condition caused by
injury, disease, or illness: (1) in which I have suffered a loss of
consciousness, exhibiting no behavioral evidence of self-awareness or
awareness of surroundings in a learned manner other than reflex activity
of muscles and nerves for low level conditioned response; and (2) from
which, after the passage of a medically appropriate period of time, it
can be determined, to a reasonable degree of medical certainty, that
there can be no recovery), I direct that my life not be extended by
life-sustaining procedures, including the administration of nutrition
and hydration artificially, unless necessary for the relief of my pain
or for my comfort.
```

### End-stage condition (P5)
```
If I have an end-stage condition (i.e. an advanced, progressive,
irreversible condition caused by injury, disease, or illness (1) that
has caused severe and permanent deterioration indicated by my
incompetency and complete physical dependency; and (2) for which, to a
reasonable degree of medical certainty, treatment of the irreversible
condition would be medically ineffective), I direct that my life not be
extended by life-sustaining procedures, including the administration of
nutrition and hydration artificially, unless necessary for the relief
of my pain or for my comfort.
```

Note v1→v2 change: in v1 these were sub-items (a), (b), (c) under
ARTICLE 1. DIRECTIVE with bold lead-ins. In v2 they are flat consecutive
paragraphs with the condition name embedded in parentheses ("i.e. ...").

---

## COMFORT CARE + STATEMENT OF VALUES (P6)

```
I request effective comfort care and pain relief even though it may
hasten my death, including artificially administered hydration and
nutrition if necessary or advisable for my pain relief or my comfort
care. I wish to reassure my Health Care Agent, my family, and my health
care providers that I recognize that death is as much a reality as
birth, growth, maturity, and old age. Death is the ultimate certainty.
I do not fear death as much as I fear the loss of my independence and
dignity, the deterioration of my body and mind, and hopeless pain. It
is my desire to limit my health care to that which offers some
reasonable prospect of my recovery, or gives me comfort and support,
alleviates pain, or which facilitates my interaction with others to the
extent that this is possible.
```

**Major v1→v2 change**: v1 had Comfort Care (Article 2) and Statement of
Values (Article 3) as separate articles. v2 folds them into a single
paragraph (P6). Scott's standard philosophical language ("death is the
ultimate certainty," "I do not fear death as much as I fear the loss of
my independence and dignity") is preserved verbatim within the combined
paragraph.

---

## CONTINUATION CLAUSE (P7)

```
In the absence of my ability to give directions regarding the use of
such life-prolonging procedures, it is my intention that this Declaration
be honored by my family and physician as the final expression of my
legal right with regard to medical or surgical treatment and to accept
the consequences therefor.
```

Body paragraph. Reaffirms binding effect.

---

## HEALTH CARE PROXY EMPOWERMENT (P8)

```
I empower my Health Care Proxy to speak for my family in their sole and
unrestricted discretion in these matters.
```

Single short body paragraph. Note this differs from v1's longer "Article
4. AUTHORITY OF HEALTH CARE AGENT" — v2 is consolidated to one sentence.

---

## PAGE LAYOUT MARKER (P10)

```
[Remainder of page intentionally left blank]
```

Layout cue. Preserve verbatim. New in v2.

---

## EXECUTION CLAUSE (P12)

```
IN WITNESS WHEREOF, I have executed this declaration, as my free and
voluntary act and deed, on ____ day of ________, 20__.
```

No placeholders — manual blanks for date. v2 uses `____ day of ________,
20__` rather than v1's `_____ day of [MONTH], [YEAR]`. For unscheduled
signings, leave the blanks. For scheduled signings, fill the blanks
directly (no placeholder substitution needed).

---

## PRINCIPAL SIGNATURE BLOCK (Table 0)

A 2×2 table. Cell [1,1] contains `[CLIENT]`. The table provides the visual
layout for the principal's signature line and printed name. Preserve the
table structure; only substitute `[CLIENT]` with the client's UPPERCASE
full legal name.

---

## PRINCIPAL NOTARY BLOCK (P16–P25)

```
COMMONWEALTH OF MASSACHUSETTS
COUNTY OF [SIGNING COUNTY]

On [DocDate], before me, the undersigned notary public, personally
appeared
[CLIENT], ___ personally known to me, or ___ proved to me through
satisfactory evidence of identification, which was a government-issued
photo identification to be the person whose name is signed on the
preceding or attached document, and who acknowledged that [Client Pronoun]
signed it voluntarily for its stated purpose.

WITNESS my hand and notarial seal.

(SEAL)
                                            ______________________________________
                                            Notary Public
                                            My Commission Expires: [Notary Commission]
```

The "personally appeared" / "[CLIENT]" line break is a paragraph break
(P18 ends at "personally appeared", P19 starts with "[CLIENT]"). Same
for "Notary Public" and "My Commission Expires:" which are now separate
paragraphs (P24 and P25).

For unscheduled signings, `[DocDate]` resolves to ` ____________ ` and
`[Notary Commission]` stays blank.

---

## WITNESS AFFIRMATIONS CLAUSE (P28)

Single paragraph containing nine numbered affirmations inline:

```
We, __________________________, __________________________, the
undersigned witnesses, each hereby attest and declare under penalty of
perjury under the laws of the Commonwealth of Massachusetts that:

(1) the foregoing instrument was personally signed by the above
principal in my presence, and thereupon I, at [Client HisHer] request
and in [Client HisHer] presence and in the presence of the other
witnesses, have hereunto subscribed my name as a witness;

(2) I did not sign the above signature of said principal for or at
[Client HisHer] direction;

(3) I personally know the above principal (or the person signing the
foregoing instrument was proved to me through satisfactory evidence of
identification to be the principal) and believe the principal to be of
sound mind and under no constraint, duress, fraud or undue influence;

(4) I am not related to the above principal by blood, marriage or
adoption;

(5) I am not entitled (to the best of my knowledge and belief) to any
portion of the estate of the above principal upon [Client HisHer] death
under any will or codicil or by operation of law;

(6) I do not have any present or inchoate claim against any portion of
the estate of the above principal;

(7) I do not have any financial responsibility for the medical care of
the above principal;

(8) I am not a physician or an employee of any physician, and I am not
an operator or employee of, or patient in, any hospital, health care
provider, residential care facility, community care facility or similar
institution; and

(9) I am at least eighteen (18) years of age.
```

In the template this is a SINGLE paragraph (P28) with the nine
affirmations inline; the line breaks above are for readability of this
guide only. Preserve as a single paragraph in output.

`[Client HisHer]` appears four times in P28 (the possessive "her" in
"believe her to be of sound mind" was intentionally rewritten as "the
principal" during the v1.1 fix to avoid introducing a separate
object-pronoun placeholder).

Two underscore blanks at the start of P28 receive the witnesses' typed/
written names. Witness names and addresses are NOT collected separately
as placeholders — witnesses fill the blanks at signing.

---

## WITNESS SIGNATURE BLOCKS (Tables 1 and 2)

Two 2×3 tables. Each contains:
- Row 0, Col 1: "of"
- Row 1, Col 0: signature blank + ", Witness"
- Row 1, Col 2: "Address"

Visual layout for two witness signatures with city/state and address
fields. No placeholders to substitute. Preserve table structure exactly.

---

## WITNESS NOTARY BLOCK (P31–P38)

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

Same `[DocDate]` and `[Notary Commission]` as the principal notary block.

---

## QUALITY CHECKLIST (AHD-specific)

- [ ] Title verbatim: ADVANCE DIRECTIVE OF [CLIENT in UPPERCASE]
- [ ] No `ADVANCE HEALTH DIRECTIVE` (that's the v1 wording) anywhere in
      the output
- [ ] No literal placeholder brackets remain (`[CLIENT]`, `[City]`,
      `[SIGNING COUNTY]`, `[DocDate]`, `[Notary Commission]`, `[Client
      Pronoun]`, `[Client HisHer]`) — all resolved or, if intentionally
      left blank for signing, replaced with underscored blanks
- [ ] No literal `\n` characters anywhere in the output
- [ ] `[Client Pronoun]` resolved to "he" or "she" (lowercase) in P19
- [ ] `[Client HisHer]` resolved to "his" or "her" (lowercase) in all
      four occurrences within P28
- [ ] All three triggering conditions present (terminal, persistent
      vegetative state, end-stage)
- [ ] Comfort care + statement of values combined paragraph present
      (P6) with Scott's standard philosophical language ("death is the
      ultimate certainty," "I do not fear death as much as I fear the
      loss of my independence and dignity") preserved verbatim
- [ ] HCP empowerment clause present (P8)
- [ ] "[Remainder of page intentionally left blank]" marker preserved
      (P10)
- [ ] Execution clause uses `____ day of ________, 20__` blanks (NOT
      the v1 `[MONTH]`/`[YEAR]` placeholders)
- [ ] Both notary blocks present and complete (Principal at P16–P25,
      Witnesses at P31–P38)
- [ ] Witness affirmations clause (P28) is a single paragraph containing
      all nine numbered affirmations inline — NOT split into separate
      paragraphs
- [ ] All three tables preserved with correct structure (Table 0 = 2×2
      principal signature, Tables 1 & 2 = 2×3 witness signature blocks)
- [ ] Two witnesses required at execution; statutory disqualifiers from
      the nine-affirmation clause must be honored (witnesses cannot be
      related, claim against estate, financially responsible for medical
      care, the principal's physician, etc.)
- [ ] Principal also signs in front of notary (P16–P25)
