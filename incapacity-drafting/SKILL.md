---
name: incapacity-drafting
description: >
  [OUTCOME]: Drafts a stand-alone MA incapacity package — Advance Health
  Directive, Health Care Proxy, HCP Preferences Worksheet, HIPAA
  Authorization, Durable Power of Attorney — for an individual or married
  couple (separate set per spouse). Files named "Client Full Name_Document
  Title.docx" saved to OUTPUTS.
  [TRIGGER]: "draft incapacity documents," "incapacity package," "DPOA and
  HCP," "POA/HCP/HIPAA/Living Will," "incapacity docs for [client]," "HCP
  preferences worksheet for [client]."
  [ANTI-TRIGGER]: Do NOT use for full will plans (will-based-drafting),
  trust plans (trust-drafting), PPM, Temp Delegation, deeds, closing
  packages, or summaries.
---

# Incapacity Drafting Skill — Aubrey Law

## Purpose

Draft the five core Massachusetts incapacity documents as a stand-alone
package: Advance Health Directive (Living Will), Health Care Proxy, HCP
Preferences Worksheet, HIPAA Authorization, and Durable Power of Attorney.
Output: fully populated .docx files, one per document per client, saved to
the project OUTPUTS folder under a matter subfolder, ready for Scott's
review.

**CRITICAL — Document Generation:**
All .docx files MUST be generated using `/home/claude/al_generator.py` and the
clean AL template at `/home/claude/al-template/`. Do NOT use the `docx` skill
or any other method — fonts, styles, and branding will be wrong.

Also read at start: the `estate-planning` skill for placeholder conventions,
MA execution blocks, and Scott's standard clause language.

---

## Authoritative Sources for Document Content

The five uploaded templates in `references/` are the canonical source of
truth for verbatim language. The article-by-article guides spell out exactly
what each section says, what gets substituted, and what conditional rules
apply. When emitting a document, read the matching guide first, then cross-
reference against the .docx template if anything is ambiguous.

| Document | Article guide | Template file |
|---|---|---|
| Health Care Proxy | `references/hcp-articles.md` | `references/HCP_v1.1.docx` |
| HCP Preferences Worksheet | `references/hcp-preferences-worksheet.md` | `references/HCP_Preferences_Worksheet.docx` |
| HIPAA Authorization | `references/hipaa-articles.md` | `references/HIPAA_v1.1.docx` |
| Advance Directive | `references/ahd-articles.md` | `references/Living_Will_v1.1.docx` |
| Durable Power of Attorney | `references/dpoa-articles.md` | `references/DPOA_v1.1.docx` |

The legacy `dpoa-incapacity-guide.md`, if present in the installed skill
folder, is superseded by `dpoa-articles.md`. Delete the legacy file once
this version is in place.

---

## Before Starting

1. Check `learnings.md` and apply any rules.
2. If the matter folder contains a `claude.md`, read it for pre-filled client
   data (names, addresses, fiduciaries).
3. If the user supplied a design sheet or intake questionnaire (pasted text,
   uploaded PDF/docx, JSON payload), extract data from it. If not, fall back
   to interactive Q&A via AskUserQuestion.

---

## Step 1 — Collect & Validate Inputs

**Matter type:** Individual (1 set of 5 docs) or Married Couple (2 sets = 10
docs).

**Per-client required fields:**
- Full legal name (as it will appear on the documents) — used in
  `[CLIENT]` placeholder across all five documents
- City + county of residence + state (MA assumed) — used in `[City]` (HCP
  P1) and `[SIGNING COUNTY]` (HCP, AHD, HIPAA notary blocks)
- Date of birth — used in `[Client DOB]` (HIPAA P5 only)
- Street address — used in `[Street Address]` (HCP P1 only; HIPAA v2 no
  longer collects address)
- Pronouns (`he/she`) — used in `[client he/she]` (HCP P50, HIPAA P24,
  AHD P18). Note that DPOA uses `[Client Pronoun]` (titlecase generic
  name) and AHD v2 has a hardcoded "she/her" defect — three different
  conventions across templates pending harmonization.

**Spouse field (married matters only):**
- Spouse's full legal name — used **only** in the DPOA's "Care in
  Proximity of Spouse" section (`[IF_MARRIED]` block). HIPAA v2 removed
  the spouse clause; HCP v2 and AHD v2 have no spouse references.

**Fiduciary fields:** see `references/fiduciary-checklist.md` for the full list
(HCP agents, DPOA agents, HIPAA recipients, special instructions, co-agent
rules, effective-date preferences, gifting preferences). Note: HCP v2 has
ONLY ONE alternate HCP slot (v1 supported two); the article guide and
quality checklist will flag if more than one alternate is collected.

**DPOA-specific fields:**
- `dpoa.initial_agent` — required; the named Attorney-in-Fact (single person)
- `dpoa.co_agent` — optional; if set, triggers `[IF_CO_AGENT]` and requires
  `dpoa.coagent_authority` to be set as well
- `dpoa.coagent_authority` ∈ `{joint, separate}` — required when `co_agent`
  is set. Default: `separate` (per Scott's standard practice)
- `dpoa.successors[]` — ordered list of successor agent names; inserted as a
  numbered list after the successor opening sentence
- `dpoa.initial_agent.is_married` — boolean; if true, triggers
  `[IF_AIF_IS_MARRIED]` block in the Self-Dealing section

**Prompt style:** If a design sheet is provided, extract silently and ask
ONLY about missing required fields. If no design sheet, use AskUserQuestion
in one or two batches (≤7 questions per batch).

If any required field is still missing after interview, note it in DRAFTING
NOTES at the top of the affected document — do not halt generation.

---

## Step 2 — Determine Document Set & File Naming

| Matter Type | Files Produced |
|---|---|
| Individual | 5 files, named for the client |
| Married Couple | 10 files — 5 for each spouse, named for each spouse |

**File naming (exact, per Scott's instruction):**

```
{Client Full Legal Name}_Advance Health Directive.docx
{Client Full Legal Name}_Health Care Proxy.docx
{Client Full Legal Name}_HCP Preferences Worksheet.docx
{Client Full Legal Name}_HIPAA Authorization.docx
{Client Full Legal Name}_Durable Power of Attorney.docx
```

Use the client's full legal name exactly as drafted on the document. No
abbreviations, no version suffixes (`_v1`), no initials. Spaces are fine.

**Output directory:** Save all files to the project OUTPUTS folder under a
subfolder named after the matter (e.g., `OUTPUTS/Smith_Jane_and_John/`). If
`claude.md` specifies a different matter folder name, use that.

---

## Step 3 — Draft the Documents

For each document, read the article guide first, then emit via
`al_generator.py`.

→ Read `references/formatting-rules.md` FIRST for cross-document
  formatting conventions: uppercase names, execution-date blanks, notary
  blocks on new pages, signature footer lines, pronoun handling.
→ For HCP content → `references/hcp-articles.md`
→ For HCP Preferences Worksheet → `references/hcp-preferences-worksheet.md`
→ For HIPAA content → `references/hipaa-articles.md`
→ For AHD content → `references/ahd-articles.md`
→ For DPOA content → `references/dpoa-articles.md` (canonical guide for the
  current DPOA_v1.1.docx template)

The five templates in `references/` are the verbatim source of truth —
read them directly if any article guide is ambiguous about formatting.
Current versions: DPOA_v1.1.docx, HCP_v1.1.docx, HIPAA_v1.1.docx,
Living_Will_v1.1.docx, HCP_Preferences_Worksheet.docx. All four primary
documents are on parallel v1.1 versioning.

Key defaults (all overridable by design sheet or Scott's instruction):
- **HCP:** MGL c. 201D; witnesses may NOT be the agent or alternate; notary
  required for both principal and witnesses (two notary blocks). v1.1
  template state: only ONE alternate HCP slot; Anatomical Gift Election
  is hardcoded ON ("any needed organs, tissues or parts for any
  purpose") — no client.anatomical_gift field used; flat bold lead-ins
  for section headings (no letter prefixes); embedded HEALTHCARE
  PREFERENCES section removed (preferences worksheet is delivered as a
  separate document).
- **HCP Preferences Worksheet:** client-facing discussion guide; not legally
  binding; no witnesses, no notary; single client signature; eleven topic
  tables with empty `*My notes:*` rows; date left blank for client.
- **HIPAA:** 45 CFR §§ 160–164; broad scope; Authorized Persons = HCP
  chain (primary + alternate) + DPOA chain (primary + successors) +
  trustees of any trust where client is a beneficiary or trustee. v1.1
  template state: spouse clause REMOVED (no separate `[SPOUSE FULL NAME]`
  placeholder, no `[IF_MARRIED]` logic); client address REMOVED (no
  `[ADDRESS]` placeholder); psychotherapy notes election REMOVED (no
  opt-in/opt-out lines — psychotherapy notes excluded by default); notary
  county uses `[SIGNING COUNTY]` placeholder (works for any signing
  location). No expiration beyond two years post-death; notary required
  (no witnesses).
- **AHD:** three triggering conditions (terminal / persistent vegetative
  state / end-stage); comfort care + statement of values combined into one
  paragraph; HCP empowerment clause; witnesses + notary; tighten witness
  signature table per `formatting-rules.md` §4. Placeholders use DPOA
  naming convention (`[CLIENT]`, `[City]`, `[SIGNING COUNTY]`,
  `[DocDate]`, `[Notary Commission]`). Pronoun handling: `[Client
  Pronoun]` for the subject pronoun in the principal notary acknowledgement
  (P19), `[Client HisHer]` for possessive pronouns in the witness
  affirmations clause (P28).
- **DPOA:** MGL c. 190B § 5-501 (durability); MGL c. 190B Art. V-A (digital
  assets); immediately effective (no springing trigger); separate authority
  the default when co-agents are named; gifting hardcoded OFF in template
  (no override); digital assets ON; single notary block (witnesses sign
  inline). All six conditional macros (`[IF_SOLO_AGENT]`, `[IF_CO_AGENT]`,
  `[IF_JOINT]`, `[IF_SEPARATE]`, `[IF_MARRIED]`, `[IF_AIF_IS_MARRIED]`) must
  be resolved at generation time — never emit the macro tags. Successor
  names inserted as a numbered list after the successor opening sentence.

**Cross-document rules that apply to ALL documents:**
- Names (Principal and fiduciaries) in body text: **UPPERCASE plain text**.
  Drop the bolded-placeholder formatting shown in the templates and article
  guides — that bolding is visual placeholder highlighting only, not a
  production cue.
- Signature footer line: Principal's full legal name in UPPERCASE under
  every signature line.
- Unscheduled signing: use `____ day of ___________` / ` ________________` /
  `________________` for ordinal date / execution date / notary commission.
- Notary blocks: insert a page break so each notary block starts on a
  new page.

For married matters, draft the Client's full set first, then the Spouse's
full set. Do NOT co-mingle fiduciaries between spouses unless both clients
named the same person intentionally (flag for Scott's confirmation).

---

## Step 4 — Generate .docx Files

Use `/home/claude/al_generator.py` with `/home/claude/al-template/`. Call
`reset_article_counter()` at the start of each document where article
numbering applies.

Note on article heading formats — these differ by document:
- **AHD:** flat prose with no article headings (v2 change — v1's
  `ARTICLE 1.  DIRECTIVE` format is gone). Sections flow without explicit
  labels; the structure is logical only. Preserve the template's
  paragraph order and the "[Remainder of page intentionally left blank]"
  layout marker.
- **HCP:** flat bold lead-ins, NO letter-prefix section headings. v1's
  `A. HEALTH CARE PROXY`, `B. APPOINTMENT...`, `C. POWERS...` labels were
  removed in v2 — section labels are now plain bold (`HEALTH CARE PROXY.`,
  `APPOINTMENT OF HEALTH CARE AGENT.`, etc.).
- **HIPAA:** flat bold lead-ins, NO numbered section labels. v1's `1.`,
  `2.`, `3.` numbered paragraphs were removed in v2 — section labels are
  now plain bold (`Identity of Person or Class of Persons Authorized to
  Make Disclosure.`, `Description of Information to Be Disclosed.`,
  etc.).
- **Worksheet:** flat structure with topic tables — no articles or sections.
- **DPOA:** no ARTICLE-style headings. All powers and structural sections
  are flat `TR_Art2` paragraphs with bolded lead-in labels — sentence case
  for the enumerated powers (`Banking Powers.`, `Tax Powers.`), ALL CAPS
  for the structural sections (`HEALTH CARE DECISIONS AND FUNERAL PLANS.`,
  `THIRD PARTY RELIANCE.`). Style names use underscores (`TR_Art2`,
  `TR_Body1`) rather than the trust's hyphenated names.

Write output files directly to the OUTPUTS subfolder using the naming
convention in Step 2.

---

## Step 5 — Quality Review (Always)

Before delivering, run the full checklist in
`references/incapacity-quality-checklist.md` PLUS the document-specific
checklists at the bottom of each article guide
(`hcp-articles.md`, `hipaa-articles.md`, `ahd-articles.md`,
`hcp-preferences-worksheet.md`, `dpoa-articles.md`). Verify file count and
naming, client-data consistency, fiduciary chain, statutory citations,
execution blocks, document-specific defaults, AND the cross-document
formatting rules from `formatting-rules.md` (uppercase names, footer line,
notary page breaks, execution-date blanks, pronoun grammar).

For DPOA specifically, the most common failure modes are:
1. Leaving literal `[IF_*]` or `[END_IF_*]` macro tags in the output
2. Leaving unresolved bracketed placeholders (`[CLIENT]`, `[SPOUSE]`, etc.)
3. Forgetting to insert the successor name list after the successor opening
   sentence
4. Including `[IF_MARRIED]` content for single clients (especially the
   entire "Care in Proximity of Spouse" section, which must be omitted
   wholesale)

These should be verified before every DPOA delivery.

If any item fails, log it as a DRAFTING NOTE inside the affected document
AND surface it in the Step 6 summary. Do NOT silently fix and ship.

---

## Step 6 — Deliver Summary

Use `present_files` to surface each .docx as a clickable card. The summary
should include:

- Files generated, grouped by client.
- All DRAFTING NOTES flags (missing fields, non-default choices, items
  requiring verification).
- One-line fiduciary chain summary per client
  (e.g., "HCP: Jane → John → Mary; DPOA: Jane → John").
- Execution reminders:
  - HCP: 2 witnesses required (not the agent or alternates) + notary
  - HCP Preferences Worksheet: no witnesses, no notary — client signs alone
  - HIPAA: notary only, no witnesses
  - AHD: 2 witnesses required (statutory disqualifiers — see ahd-articles
    checklist) + notary
  - DPOA: 2 witnesses required (not the Attorney-in-Fact or any successor;
    witnesses sign inline in the body — no separate witness signature
    block) + single notary block for the Principal
- Note that the HCP Preferences Worksheet is delivered to the client as a
  companion discussion guide and is not part of the legally binding HCP.

---

## Legal Compliance Guardrails

1. **Source citations:** Cite MGL c. 201D (HCP), MGL c. 190B § 5-501 (DPOA),
   45 CFR §§ 160–164 (HIPAA), MGL c. 190B Art. V-A (digital assets) — never
   summarize from memory.
2. **Uncertainty flagging:** Use `[REQUIRES VERIFICATION]` in DRAFTING NOTES
   for uncertain choices.
3. **Not legal research:** AI output is a drafting aid — not authoritative
   legal research.
4. **Preserve original language:** Quote source documents and Scott's
   standard clauses verbatim. The five uploaded templates in
   `references/` (DPOA_v1.1, HCP_v1.1, HIPAA_v1.1, Living_Will_v1.1, and
   HCP_Preferences_Worksheet) are the canonical source of truth.
5. **Attorney review required:** Every draft requires Scott's review before
   client delivery or execution.
6. **Resolve all DPOA conditional macros:** The DPOA template contains six
   `[IF_X]...[END_IF_X]` macros that MUST be resolved at generation time.
   Any unresolved macro tag in output is a defect. See `dpoa-articles.md`
   for the full macro table.

---

## Learnings

Check `learnings.md` at the start of each run. After completing, ask Scott:
"Did the output meet your expectations? Anything to improve for next time?"
Log useful feedback to `learnings.md`.
