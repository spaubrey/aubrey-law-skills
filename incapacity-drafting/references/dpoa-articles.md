# Durable Power of Attorney — Section Drafting Guide
# Source: Scott Aubrey / Aubrey Law actual template (DPOA_v1.2.docx)
# Authority: M.G.L. c. 190B § 5-501; M.G.L. c. 190B Article V-A (digital assets)

---

## PRODUCTION RULES (apply when emitting the document)

### Placeholder set

The template uses underscore-bracket placeholders. Resolve every one of these
before emitting. Any unresolved placeholder is a defect.

| Placeholder | Source | Notes |
|---|---|---|
| `[CLIENT]` | client.full_legal_name | UPPERCASE plain text in body and signature footer (cross-document rule) |
| `[City]` | client.city | Title case |
| `[INITIAL POA]` | dpoa.initial_agent | UPPERCASE plain text in body; not a fiduciary chain — single named agent |
| `[CO POA]` | dpoa.co_agent | UPPERCASE plain text; only used inside `[IF_CO_AGENT]` blocks |
| `[SPOUSE]` | spouse.full_legal_name | UPPERCASE plain text; only used inside `[IF_MARRIED]` blocks |
| `[Spouse HisHer]` | spouse pronoun (his/her) | lowercase; possessive; only used inside `[IF_MARRIED]` blocks |
| `[Client Pronoun]` | client pronoun (he/she) | lowercase; used in notary acknowledgement |
| `[SIGNING COUNTY]` | client county OR the county where signing occurs | **UPPERCASE** (e.g., "NORFOLK", "MIDDLESEX") |
| `[Ordinal_DocDate]` | execution date as ordinal phrase | e.g., `21st day of May, 2025`. For unscheduled signings, leave as ` _____ day of ____________, _______ ` |
| `[DocDate]` | notary acknowledgement date | e.g., `May 21, 2025`. For unscheduled signings, leave as ` ____________ ` |
| `[Notary Commission]` | notary commission expiration date | Leave blank ` ____________ ` — populated by notary at signing |

### Conditional macros — resolve at generation time

The template contains six conditional macros. Each is wrapped in
`[IF_X — instruction text]` ... `[END_IF_X]`. **NEVER emit the macro tags
themselves**; resolve them by emitting or omitting the wrapped content based
on the matter configuration.

| Macro | Emit when | Default |
|---|---|---|
| `[IF_SOLO_AGENT]` | `dpoa.co_agent` is null | Most matters |
| `[IF_CO_AGENT]` | `dpoa.co_agent` is set | Opt-in |
| `[IF_JOINT]` | `dpoa.coagent_authority == "joint"` (requires both signatures) | — |
| `[IF_SEPARATE]` | `dpoa.coagent_authority == "separate"` (each may act alone) | **Scott's default when co-agents are named** |
| `[IF_ONE_SUCCESSOR]` | exactly one successor agent named (`dpoa.successors` has 1 entry) | — |
| `[IF_MULTI_SUCCESSOR]` | two or more successor agents named (`dpoa.successors` has 2+ entries) | — |
| `[IF_MARRIED]` | `matter.is_married == true` (client has a spouse named in the matter) | — |
| `[IF_AIF_IS_MARRIED]` | `dpoa.initial_agent.is_married == true` (the Attorney-in-Fact has a spouse) | — |

**Pairing rules:**
- `[IF_SOLO_AGENT]` and `[IF_CO_AGENT]` are mutually exclusive. Pick exactly one.
- `[IF_JOINT]` and `[IF_SEPARATE]` are mutually exclusive and only apply when
  `[IF_CO_AGENT]` is emitted. In the template they are nested inside
  `[IF_CO_AGENT]...[END_IF_CO_AGENT]`. Skip both for solo agents.
- `[IF_ONE_SUCCESSOR]` and `[IF_MULTI_SUCCESSOR]` are mutually exclusive.
  Pick based on the count of `dpoa.successors[]`: exactly 1 → ONE_SUCCESSOR;
  2 or more → MULTI_SUCCESSOR. If no successors are named, omit both blocks
  and flag in DRAFTING NOTES.
- `[IF_MARRIED]` and `[IF_AIF_IS_MARRIED]` are independent — both, either, or
  neither may be true.

If a macro condition is ambiguous from the design sheet, flag in DRAFTING
NOTES and default per the table above. **Do NOT emit the literal macro tags
or the bracketed instruction text** under any circumstances — they are
template scaffolding only.

### Successor chain (NOT in template — inserted at draft time)

The template opens the successor section with one sentence ("...I appoint the
following to serve as my successor Attorney-in-Fact... in the order named:")
but contains no successor names. The drafter must insert a numbered or
bulleted list of successor names immediately after that sentence, using the
data from the design sheet (`dpoa.successors[]` array, in order).

If no successors are named in the design sheet, flag in DRAFTING NOTES:
"No successor Attorney-in-Fact named — confirm with Scott." Do not generate
a successor block with empty placeholder names.

### Document-specific formatting

- **Style names use underscores** (`TR_Body1`, `TR_Art2`, etc.) — note this
  differs from the trust's hyphenated style names. Confirm al_generator.py
  helpers map to the correct underscored style.
- **Title is bold; body paragraph text is NOT bold** — the DPOA title
  (`DURABLE POWER OF ATTORNEY OF [CLIENT]`) uses bold formatting. Section
  lead-in labels (e.g., `Banking Powers.`, `THIRD PARTY RELIANCE.`) are
  bold. The body text that follows each lead-in — the substantive prose —
  must be **plain text (not bold)**. Do not carry bold formatting from the
  template's placeholder highlight styling into the merged output.
- **All powers under one Article:** The template does NOT use the trust's
  ARTICLE ONE / ARTICLE TWO heading structure. All powers and structural
  sections are flat `TR_Art2` paragraphs (Section X.0Y auto-numbered), with
  bolded lead-in labels distinguishing each.
  - Bolded lead-in labels for the "Powers" sub-sections use sentence case
    (`Powers of Collection and Payment.`, `Power to Acquire and Sell.`).
  - Bolded lead-in labels for the structural sections use ALL CAPS
    (`HEALTH CARE DECISIONS AND FUNERAL PLANS.`, `THIRD PARTY RELIANCE.`).
  - The **body text following each lead-in is NOT bold**.
  - Preserve this distinction when emitting.
- **Single notary block:** DPOA has only one notary block (for the
  Principal). There is NO separate witness notary block. Witnesses sign
  inline in the body before the principal signature.
- **No page break before notary block** in the template — unlike HCP/AHD/HIPAA,
  the DPOA flows continuously. Optional: follow Scott's preference per
  `formatting-rules.md` if it dictates a page break.

---

## TITLE

```
DURABLE POWER OF ATTORNEY OF [CLIENT]
```

Centered, bold, all caps (TR_Title style).

---

## APPOINTMENT OPENING

Single paragraph with two mutually exclusive inline blocks — `[IF_CO_AGENT]`
for two agents, `[IF_SOLO_AGENT]` for one. Emit exactly one; omit the other.

**Template text:**
```
I, [CLIENT] of [City], Massachusetts hereby appoint [INITIAL POA]
[IF_CO_AGENT]and [CO POA], to serve as my Agents and Attorneys-in-Fact
(hereinafter referred to collectively as "Attorney-in-Fact")[END_IF_CO_AGENT]
[IF_SOLO_AGENT]to serve as my Agent and Attorney-in-Fact
(hereinafter referred to as "Attorney-in-Fact")[END_IF_SOLO_AGENT]
for me and in my name and behalf to control and manage my property and
affairs in all respects including full power and authority to act as
provided herein.
```

**Rendered output — Solo agent:**
```
I, JANE SMITH of Newton, Massachusetts hereby appoint JOHN SMITH
to serve as my Agent and Attorney-in-Fact (hereinafter referred to as
"Attorney-in-Fact") for me and in my name and behalf...
```

**Rendered output — Co-agents (joint or separate):**
```
I, JANE SMITH of Newton, Massachusetts hereby appoint JOHN SMITH
and MARY JONES, to serve as my Agents and Attorneys-in-Fact (hereinafter
referred to collectively as "Attorney-in-Fact") for me and in my name
and behalf...
```

Note: "Agents and Attorneys-in-Fact" (plural) is used for co-agents
regardless of whether they act jointly or separately — that distinction is
set by the dedicated paragraph below. Do not add "jointly" here.

---

## SUCCESSOR APPOINTMENT

One paragraph containing two mutually exclusive conditional blocks —
`[IF_ONE_SUCCESSOR]` for a single named successor, `[IF_MULTI_SUCCESSOR]`
for two or more. Emit exactly one; omit the other.

**Single successor variant (`[IF_ONE_SUCCESSOR]`):**
```
If [INITIAL POA] becomes incapacitated, is not qualified to serve, or
declines or otherwise fails to serve, then I appoint
[IF_ONE_SUCCESSOR][SUCCESSOR AGENT] to serve as my successor
Attorney-in-Fact for me and in my name and behalf to control and manage
my property and affairs in all respects including full power and
authority.[END_IF_ONE_SUCCESSOR]
```

**Multiple successors variant (`[IF_MULTI_SUCCESSOR]`):**
```
If [INITIAL POA] becomes incapacitated, is not qualified to serve, or
declines or otherwise fails to serve, then I appoint
[IF_MULTI_SUCCESSOR]the following to serve as my successor
Attorney-in-Fact for me and in my name and behalf to control and manage
my property and affairs in all respects including full power and
authority, in the order named:

    FIRST:  [SUCCESSOR AGENT]
    SECOND: [SUCCESSOR AGENT]
    ...
[END_IF_MULTI_SUCCESSOR]
```

The "FIRST:", "SECOND:", etc. ordinal labels are inserted as a numbered
list in indented `TRBody1` paragraphs. Use actual ordinal words (FIRST,
SECOND, THIRD) not numbers. The `[SUCCESSOR AGENT]` placeholder is
replaced with the actual name for each entry from `dpoa.successors[]`.

**Co-agent successor opening:** When `[IF_CO_AGENT]` is in effect, the
opening sentence becomes "If [INITIAL POA] and [CO POA] both become
incapacitated..." — substitute accordingly at generation time.

If no successors are named in the design sheet, omit both blocks and add
a DRAFTING NOTE: "No successor Attorney-in-Fact named — confirm with Scott."
Do not generate a successor block with empty placeholder names.

---

## CO-AGENT AUTHORITY

Two standalone paragraphs — one for joint, one for separate. Each is its own
`<w:p>` element in the XML. **Delete the entire `<w:p>` element** for the
unused variant — do not leave an empty paragraph behind.

**Resolution rules:**

| Scenario | Joint `<w:p>` | Separate `<w:p>` |
|---|---|---|
| Solo agent | **Delete entire `<w:p>`** | **Delete entire `<w:p>`** |
| Co-agent + joint | Keep, strip macro tags | **Delete entire `<w:p>`** |
| Co-agent + separate | **Delete entire `<w:p>`** | Keep, strip macro tags |

**Joint authority paragraph** (`[IF_CO_AGENT][IF_JOINT]...[END_IF_JOINT][END_IF_CO_AGENT]`):
```
If there is more than one Attorney-in-Fact serving at any time, the
Attorneys-in-Fact shall act jointly, and any exercise of authority under
this Power of Attorney shall require the signature or written consent of
both Attorneys-in-Fact. Any third party may, without liability to me or my
estate, conclusively rely upon a written statement from either of the
aforesaid Attorneys-in-Fact or from a licensed attorney at law as to the
resignation, cessation, or inability of such Attorney-in-Fact's
predecessor(s) to serve as attorney-in-fact hereunder.
```

**Separate authority paragraph** (`[IF_CO_AGENT][IF_SEPARATE]...[END_IF_SEPARATE][END_IF_CO_AGENT]`)
— Scott's default when co-agents are named:
```
If there is more than one Attorney-in-Fact serving at any time, each
Attorney-in-Fact may act separately and independently, and any third party
may rely upon the signature or written consent of either Attorney-in-Fact
acting alone. Any third party may, without liability to me or my estate,
conclusively rely upon a written statement from either of the aforesaid
Attorneys-in-Fact or from a licensed attorney at law as to the
resignation, cessation, or inability of such Attorney-in-Fact's
predecessor(s) to serve as attorney-in-fact hereunder.
```

For solo agents, omit both blocks.

---

## GENERAL GRANT OF POWER

Bold lead-in: `GENERAL GRANT OF POWER.` (ALL CAPS — this is a structural
section, not a sub-power)

```
I authorize my Attorney-in-Fact to exercise or perform any act, power,
duty, right or obligation whatsoever that I now have or may hereafter
acquire, in relation to any person, matter, transaction, or property, real
or personal, tangible or intangible, now owned or hereafter acquired by me,
including, without limitation, the following specifically enumerated powers.
I grant to my Attorney-in-Fact full power and authority to do everything
necessary in exercising any of the powers herein granted as fully as I
might or could do if personally present, with full power of substitution or
revocation, hereby ratifying and confirming all that my Attorney-in-Fact
shall lawfully do or cause to be done by virtue of this durable power of
attorney and the powers herein granted.
```

---

## ENUMERATED POWERS (sentence-case bold lead-ins)

Emit in order. Each is a single `TR_Art2` paragraph with a bold lead-in label
followed by the body text. Read `DPOA_v1.2.docx` for the verbatim wording of
each — the template is the ground truth.

1. **Powers of Collection and Payment.** Collect, receive, demand, sue for,
   and discharge all sums, debts, dues, commercial paper, accounts,
   deposits, legacies, contractual benefits, and property; execute releases
   and endorsements.

2. **Power to Acquire and Sell.** Acquire, sell, mortgage (including
   reverse mortgage), pledge, lease, transfer, convey, or dispose of real
   and personal property; relinquish homestead rights. Express intent to
   empower AIF to deal with all real property without limitation.

3. **Management Powers.** Invest, maintain, repair, improve, manage,
   insure, rent, lease, encumber, and deal with property.

4. **Banking Powers.** Sign and endorse checks/drafts; deposit and
   withdraw; acquire/redeem CDs; open and close accounts; certify TIN.

5. **Voting Powers.** Vote shares of stock or other interests in person or
   by proxy.

6. **Business Interests.** Conduct or participate in any business; execute
   partnership agreements; incorporate/reorganize/dissolve; elect officers;
   exercise voting rights and stock options.

7. **Investment Powers.** Open investment accounts; trade stocks, bonds,
   options, securities, partnership interests, commodities (including
   futures); on margin or otherwise.

8. **Tax Powers.** Prepare/sign/file joint, separate, or single income tax
   returns; receive refunds; represent Principal before IRS and state tax
   agencies; execute IRS POA designations for three tax years prior and
   all years thereafter.

9. **Safe Deposit Boxes.** Access (including by force), remove contents,
   surrender any safe deposit box. Institution incurs no liability.

10. **Gifts.** *"My Attorney-in-Fact shall make no gifts from my assets,
    for any reason."* — Hardcoded OFF. No conditional override.

11. **Powers Under Inter Vivos Trust.** Transfer/convey property to trusts
    Principal created (donor or sole beneficiary); create and fund new
    trusts for the benefit of Principal, `[IF_MARRIED]` spouse, `[END_IF_MARRIED]`
    children, or beneficiaries; amend, revoke, appoint, or remove trustees,
    consistent with overall estate plan.

12. **Estate or Benefit Planning Powers.** Apply funds consistent with
    estate planning wishes; conserve property; `[IF_MARRIED]` benefit spouse,
    `[END_IF_MARRIED]` children, or beneficiaries; minimize taxes; maximize
    eligibility for federal/state medical, welfare, housing, public
    programs; make transfers (revocable or irrevocable) into trusts for
    benefit of Principal, `[IF_MARRIED]` spouse, `[END_IF_MARRIED]` children,
    or beneficiaries.

13. **Power to Make Statutory Elections and Disclaimers.** Make statutory
    elections; disclaim interests in property if AIF determines disclaimer
    likely increases after-tax amount passing to family without materially
    affecting Principal's well-being.

14. **Power to Act in Probate Proceedings.** Assent to or oppose probate
    accounts; act in any probate matter.

15. **Power to Act in Legal Proceedings.** Appear, answer, defend, or
    compromise suits against Principal; prosecute or compromise suits AIF
    deems proper; waive attorney-client privilege for any purpose
    including obtaining copies of estate planning documents.

16. **Retirement Plan Powers.** Deal with IRAs, Keogh, 401(a), 403(b),
    401(k), pension, profit-sharing plans; exercise elections/options;
    make withdrawals/rollovers; `[IF_MARRIED]` waive spousal rights;
    `[END_IF_MARRIED]` contribute; remedy invalid beneficiary designations
    only to name `[IF_MARRIED]` spouse, `[END_IF_MARRIED]` children, or
    existing will/trust beneficiaries.

17. **Insurance Powers.** Exercise all rights on life insurance and
    annuity contracts; borrow against; pledge; name new beneficiary
    limited to `[IF_MARRIED]` spouse, `[END_IF_MARRIED]` children, or
    existing will/trust beneficiaries; surrender, assign, exchange.

18. **Motor Vehicles and Boats.** Apply for Certificate of Title; endorse
    and transfer; represent title is clear except as disclosed.

19. **Governmental Entitlement Powers.** Deal with state/federal agencies
    for benefits; prepare/file documents; appeal contested claims; effect
    termination.

20. **Power to Designate a Substitute.** Appoint substitute agents or
    attorneys; revoke their authority.

21. **Powers to Provide for My Care.** Use property to provide for
    maintenance, transportation, medical/dental/surgical care,
    hospitalization, custodial care.

22. **Contracts.** Enter into contracts of whatever nature.

23. **Power to Hire and Pay for Services.** Retain accountants, attorneys,
    social workers, consultants, clerks, employees, workers; pay fees from
    Principal's assets.

24. **Power over Digital Assets, Accounts, and Devices.** Comprehensive
    digital assets clause per M.G.L. c. 190B Article V-A. Includes (a)
    access/control of any device, (b) management/deletion/termination of
    accounts, (c) password changes, (d) transfers/withdrawals, (e) opening
    accounts. Express disclosure authorization to AIF of catalogue +
    content of electronic communications. Authority to engage experts to
    decrypt or bypass authentication. Express consent under Electronic
    Communications Privacy Act, Computer Fraud and Abuse Act,
    Gramm-Leach-Bliley Act. Definitions of "Catalogue of my electronic
    communications," "Content of my electronic communications," "Digital
    Assets," "Digital Accounts," and "Digital Device" follow.

25. **Unenumerated Powers.** AIF may act as Principal's alter ego with
    respect to matters not otherwise enumerated and which Principal could
    do through an agent.

---

## STRUCTURAL SECTIONS (ALL CAPS bold lead-ins)

Continue as `TR_Art2` paragraphs. Read `DPOA_v1.2.docx` for verbatim wording.

26. **HEALTH CARE DECISIONS AND FUNERAL PLANS.** Authorize admission to
    health care facilities; enter care agreements; release medical records
    in AIF's discretion. AIF serves as HIPAA personal representative
    (subordinate to HCP agent if conflict). Enter funeral, burial,
    cremation contracts; pre-pay; establish funeral bank account.

27. **COURT APPOINTED FIDUCIARIES.** If probate guardianship/conservatorship
    is needed, AIF should be appointed as such fiduciary; request waiver
    of surety bond. Not a direction to file; only when absolutely
    necessary.

28. **COMPENSATION FOR MY ATTORNEY-IN-FACT.** Reasonable reimbursement of
    expenses; reasonable compensation for time, effort, and services.

29. **THIRD PARTY RELIANCE.** Third parties may rely on AIF's
    representations; no liability for permitting AIF to exercise powers.

30. **VALIDITY OUT OF STATE, GOVERNING LAW, BOND, PHOTOCOPIES.** Executed
    in MA, MA law governs validity and construction. Honored in any state
    or country. No bond required. Photocopies have same effect as original.

31. **NON-LIMITATION ON POWERS.** Construed as a general durable power of
    attorney; specific enumeration does not limit general grant.

32. **BINDING EFFECT.** Binds Principal, heirs, executors, administrators
    until AIF receives written revocation or reliable intelligence of
    Principal's death. Remains in full force until Principal executes
    written revocation.

33. **REVOCATION OF PRIOR INSTRUMENTS.** Revokes any prior Durable Powers
    of Attorney and powers conferred therein.

34. **RELATIONSHIP TO OTHER DOCUMENTS.** Supplemental to MA Health Care
    Proxy, Advance Directive, and HIPAA Authorization executed on or about
    the same date. HCP agent decisions prevail over AIF decisions in case
    of conflict.

35. **REFUSAL TO HONOR POWER.** If third party refuses to accept validity,
    AIF directed to bring legal action to compensate Principal or heirs
    for resulting damages.

36. **SUCCESSOR ATTORNEY-IN-FACT.** Solo: third parties may rely on
    successor's representation as to original AIF's death, incapacity, or
    resignation. Co-agent: third parties may rely on representation as to
    death/incapacity/resignation of either or both original AIFs.
    Compensation clause applies equally to successors.

37. **SELF-DEALING AND POWERS OF APPOINTMENT.** AIF authorized to engage
    in self-dealing, but benefit to AIF limited to HEMS standard (health,
    education, maintenance, support) unless assented to by adverse-interest
    party. AIF MAY NOT discharge own legal support obligations
    `[IF_AIF_IS_MARRIED]` or benefit AIF's spouse, spouse's estate,
    spouse's creditors, or estate's creditors. `[END_IF_MARRIED]` Express
    intent: no general power of appointment; no inclusion of Principal's
    assets in AIF's gross estate.

38. **CARE IN PROXIMITY OF SPOUSE AND FOR BENEFIT OF SPOUSE.**
    `[IF_MARRIED]` only — entire section. Authorizes expenditures to enable
    Principal to reside or be cared for near spouse; support and maintain
    shared household; expend for spouse's support, maintenance, health needs.
    OMIT THE ENTIRE SECTION for single clients.

39. **VALIDITY DESPITE PASSAGE OF TIME, DISABILITY OR INCAPACITY.**
    Remains in full force despite passage of time; not affected by
    Principal's disability or incapacity. (This is the durability clause —
    M.G.L. c. 190B § 5-501.)

---

## EXECUTION BLOCK

```
IN WITNESS WHEREOF, I have executed this Durable Power of Attorney on this
[Ordinal_DocDate].


______________________________________
[CLIENT], Principal
```

For unscheduled signings, `[Ordinal_DocDate]` resolves to
` _____ day of ____________, _______ `.

---

## WITNESS CLAUSE (inline, no separate witness signature block with addresses)

```
We, __________________________, __________________________, the
undersigned, have witnessed the signing of this document by the Principal
or at the direction of the Principal and state that the Principal appears
to be at least eighteen years of age, of sound mind and under no constraint
or undue influence. We have not been named as the Principal's
Attorney-in-Fact, or as successor Attorney-in-Fact in this document.
```

Two underscored signature blanks inline before the body of the clause.
Witness names and addresses are NOT collected separately in this template
(differs from HCP and AHD). Witnesses sign their names directly on the two
inline blanks.

**Execution reminder:** Witnesses may NOT be the named Attorney-in-Fact or
any successor. Flag in Step 6.

---

## NOTARY BLOCK (Principal only — no separate witness notary)

```
COMMONWEALTH OF MASSACHUSETTS
COUNTY OF [SIGNING COUNTY]

On [DocDate], before me, the undersigned notary public, personally
appeared [CLIENT], ___ personally known to me, or ___ proved to me through
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

For unscheduled signings, `[DocDate]` resolves to ` ____________ ` and
`[Notary Commission]` stays blank.

---

## QUALITY CHECKLIST (DPOA-specific)

**Run the three-item pre-delivery scan from SKILL.md Step 5a–5c first:**
- [ ] **Footer** — `footer1.xml` reads `DURABLE POWER OF ATTORNEY OF [CLIENT NAME IN CAPS]`
      with `[CLIENT]` resolved. Note: `[CLIENT]` is split across three runs in the
      footer XML — inspect `footer1.xml` directly, do not rely on body scan.
- [ ] **Execution date** — `[Ordinal_DocDate]` in execution block and `[DocDate]` in notary block
      both resolved or replaced with correct underscore blanks; no literal bracket tags remain.
- [ ] **Signing county** — `[SIGNING COUNTY]` in notary block resolved to UPPERCASE county name
      (e.g., "NORFOLK"); no literal bracket tag remains.

**Then run the full checklist:**
- [ ] Title verbatim: DURABLE POWER OF ATTORNEY OF [CLIENT name in UPPERCASE]
- [ ] **Title is bold; body paragraph text following each section lead-in is
      NOT bold** — lead-in labels (e.g., `Banking Powers.`,
      `THIRD PARTY RELIANCE.`) are bold; the prose that follows is plain text
- [ ] **`[CLIENT]` name is UPPERCASE plain text** throughout body and
      signature footer — no bold on the name value itself
- [ ] `[IF_SOLO_AGENT]` vs `[IF_CO_AGENT]` correctly emitted; the OTHER variant
      omitted (NOT left in the body as a comment or stub)
- [ ] **Appointment paragraph renders correctly for the matter type:**
      - Solo agent → reads "appoint [NAME] to serve as my Agent and Attorney-in-Fact"
      - Co-agent → reads "appoint [NAME] and [NAME], to serve as my Agents and
        Attorneys-in-Fact (hereinafter referred to collectively as 'Attorney-in-Fact')"
      - No `[IF_CO_AGENT]`, `[END_IF_CO_AGENT]`, `[IF_SOLO_AGENT]`, or
        `[END_IF_SOLO_AGENT]` tags remain in the output
- [ ] **Joint/separate paragraphs correctly resolved — no blank paragraphs left behind:**
      - Solo agent → both joint `<w:p>` and separate `<w:p>` deleted entirely
      - Co-agent + joint → joint paragraph kept (tags stripped); separate `<w:p>` deleted entirely
      - Co-agent + separate → separate paragraph kept (tags stripped); joint `<w:p>` deleted entirely
      - Confirm by checking that no empty `<w:p>` with `TRBody1` style sits between
        the successor section and the GENERAL GRANT OF POWER paragraph
- [ ] `[IF_ONE_SUCCESSOR]` vs `[IF_MULTI_SUCCESSOR]` correctly emitted based on
      successor count; exactly one block present; the other omitted entirely
- [ ] Successor names resolved — no literal `[SUCCESSOR AGENT]` placeholder
      remains; each successor name is the actual person's name
- [ ] Multiple successors use ordinal labels: FIRST, SECOND, THIRD (not numbers)
- [ ] No literal `[IF_*]` or `[END_IF_*]` macro tags remain in the output
- [ ] No literal placeholder brackets remain (`[CLIENT]`, `[SPOUSE]`, etc.) —
      all resolved or, if intentionally left blank for signing, replaced
      with underscored blanks
- [ ] `[IF_JOINT]` vs `[IF_SEPARATE]` correctly emitted for co-agent matters
      (nested inside `[IF_CO_AGENT]`); both omitted for solo agents (default
      to SEPARATE if ambiguous per Scott's instruction)
- [ ] `[IF_MARRIED]` blocks correctly included for married clients, OMITTED
      for single clients (including the entire "Care in Proximity of
      Spouse" section)
- [ ] `[IF_AIF_IS_MARRIED]` block correctly handled in Self-Dealing section
      based on whether the named Attorney-in-Fact has a spouse
- [ ] Successor list inserted after the successor opening sentence — actual
      successor names from design sheet, numbered in order
- [ ] Gifts section reads "shall make no gifts from my assets, for any
      reason" — verbatim, no overrides
- [ ] Digital assets section included in full with all five clauses,
      definitions, and statutory references
- [ ] Relationship to Other Documents references HCP, AHD, and HIPAA
- [ ] Single notary block (Principal only); witness clause inline
- [ ] UPPERCASE name + `, Principal` under signature line
- [ ] M.G.L. c. 190B § 5-501 durability is implicit in the Validity
      Despite Passage of Time section (no explicit statutory cite required
      in body, per template)
- [ ] Pronouns resolved (`[Spouse HisHer]`, `[Client Pronoun]`) or flagged
