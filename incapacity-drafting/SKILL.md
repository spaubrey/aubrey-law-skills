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

**CRITICAL — Template-Based Generation Only:**
Every output document MUST be produced by merging client data into the
corresponding .docx template in `references/`. The workflow is:

1. Copy the template .docx to the output location
2. Unpack it: `python /mnt/skills/public/docx/scripts/office/unpack.py <template> <unpacked_dir>`
3. Edit `unpacked_dir/word/document.xml` — replace placeholder text in the XML using the str_replace tool
4. Repack: `python /mnt/skills/public/docx/scripts/office/pack.py <unpacked_dir> <output.docx> --original <template>`

**NEVER create documents from scratch** (no `docx` JS library, no
`al_generator.py`, no writing XML from scratch). If a template file is
missing or cannot be found, stop immediately — see Step 0 below.

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
| Durable Power of Attorney | `references/dpoa-articles.md` | `references/DPOA_v1.2.docx` |

The legacy `dpoa-incapacity-guide.md`, if present in the installed skill
folder, is superseded by `dpoa-articles.md`. Delete the legacy file once
this version is in place.

---

## Step 0 — Verify Templates (Do This First, Before Anything Else)

Before collecting any client data, verify that every required template exists
in the skill's `references/` folder. The five required template files are:

| Template file | Document |
|---|---|
| `references/HCP_v1.1.docx` | Health Care Proxy |
| `references/HCP_Preferences_Worksheet.docx` | HCP Preferences Worksheet |
| `references/HIPAA_v1.1.docx` | HIPAA Authorization |
| `references/Living_Will_v1.1.docx` | Advance Directive |
| `references/DPOA_v1.2.docx` | Durable Power of Attorney |

**Check:** Run `ls <skill_path>/references/*.docx` or use the `view` tool on
the references directory to confirm all five are present.

**If any template is missing:**
- Do NOT attempt to draft that document from scratch.
- Stop and ask Scott: "The template for [Document Name] is missing from
  the skill's references folder (`references/[filename]`). Please locate
  and install the template file before I can generate this document.
  Should I proceed with the other documents, or wait until all templates
  are available?"
- Only proceed with documents whose templates ARE present unless Scott
  explicitly instructs otherwise.

**If ALL templates are present:** Proceed to Step 1.

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

## Step 3 — Prepare Client Data for Merge

Read the article guide for each document being generated:

→ `references/hcp-articles.md` — HCP placeholder set, conditional rules, formatting
→ `references/hcp-preferences-worksheet.md` — Worksheet content and layout
→ `references/hipaa-articles.md` — HIPAA placeholder set
→ `references/ahd-articles.md` — AHD placeholder set, pronoun handling
→ `references/dpoa-articles.md` — DPOA placeholder set and all six conditional macros

Build a complete placeholder resolution table from client data before
touching any template. For each document, list every placeholder and its
resolved value (or the underscore blank for signing-day fields). If any
required value is unresolvable, flag it in DRAFTING NOTES — do not halt.

**DPOA conditional macros:** Resolve all six macros
(`[IF_SOLO_AGENT]`, `[IF_CO_AGENT]`, `[IF_JOINT]`, `[IF_SEPARATE]`,
`[IF_MARRIED]`, `[IF_AIF_IS_MARRIED]`) before opening any XML. Determine
exactly which content blocks to include and which to omit.

Key document defaults (see article guides for full detail):
- **HCP:** Two notary blocks; anatomical gift hardcoded ON; one alternate HCP slot.
- **HCP Preferences Worksheet:** No witnesses, no notary; eleven topic tables.
- **HIPAA:** Notary only (no witnesses); no spouse clause; no address field.
- **AHD:** Two witnesses + notary; three triggering conditions; two notary blocks.
- **DPOA:** Single notary block; witnesses sign inline; eight conditional macros must be resolved (`[IF_SOLO_AGENT]`, `[IF_CO_AGENT]`, `[IF_JOINT]`, `[IF_SEPARATE]`, `[IF_ONE_SUCCESSOR]`, `[IF_MULTI_SUCCESSOR]`, `[IF_MARRIED]`, `[IF_AIF_IS_MARRIED]`).

**Cross-document rules that apply to ALL documents:**
- **Names** (Principal and fiduciaries): **UPPERCASE plain text** — strip any bold from name runs.
- **SIGNING COUNTY**: **UPPERCASE** (e.g., "NORFOLK", "MIDDLESEX") in all notary blocks.
- **HCP Relationship fields**: **plain text, NOT bold**.
- **DPOA**: title and lead-in labels are bold; body prose following each lead-in is **NOT bold**.
- **All placeholders must be resolved**: no `[BRACKET]` tags in output; signing-day blanks use underscore strings.
- Signature footer: Principal's full legal name UPPERCASE under every signature line.

For married matters, prepare data for Client first, then Spouse. Do NOT
co-mingle fiduciaries between spouses unless intentional (flag for Scott).

---

## Step 4 — Generate .docx Files from Templates

For each document, follow this exact sequence. **NEVER create documents from
scratch. Always start from the template .docx file in `references/`.**

### 4a — Copy template to a working temp location

```bash
cp <skill_path>/references/<TemplateFile>.docx /tmp/<ClientName>_<DocTitle>_work.docx
```

Template-to-document mapping:
| Template | Document |
|---|---|
| `references/HCP_v1.1.docx` | Health Care Proxy |
| `references/HCP_Preferences_Worksheet.docx` | HCP Preferences Worksheet |
| `references/HIPAA_v1.1.docx` | HIPAA Authorization |
| `references/Living_Will_v1.1.docx` | Advance Directive |
| `references/DPOA_v1.2.docx` | Durable Power of Attorney |

### 4b — Unpack the working copy

```bash
python /mnt/skills/public/docx/scripts/office/unpack.py \
  /tmp/<ClientName>_<DocTitle>_work.docx \
  /tmp/<ClientName>_<DocTitle>_unpacked/
```

### 4c — Inspect document.xml to locate placeholders

Use the `view` tool on `unpacked/word/document.xml`. Identify the exact XML
representation of each placeholder — they may be split across multiple
`<w:r>` runs. Do not guess at the XML structure; always inspect first.

For DPOA conditional blocks, there are two structural patterns — handle them differently:

**Inline blocks** — condition sits inside a larger paragraph alongside other text.
If true: strip the `[IF_X]`/`[END_IF_X]` tags, keep content. If false: remove
content and tags, leave surrounding paragraph intact.
→ Examples: `[IF_CO_AGENT]` and `[IF_SOLO_AGENT]` in the appointment paragraph.

**Full-paragraph blocks** — entire `<w:p>` element contains only the conditional.
If true: strip macro tags, keep the `<w:p>`. If false: **delete the entire
`<w:p>` element** — leaving it empty produces a blank line in the document.
→ Examples: the joint authority `<w:p>` and the separate authority `<w:p>`.
For solo-agent matters, delete both. For co-agent matters, delete whichever
of joint/separate does not apply.

Never leave literal macro tags in the output.

### 4d — Substitute placeholders using str_replace

Use the `str_replace` tool directly on
`/tmp/<ClientName>_<DocTitle>_unpacked/word/document.xml`.
Make one replacement per call. Replace each placeholder (or its split-run
XML) with the resolved client value.

Bold handling:
- Names → UPPERCASE, remove `<w:b/>` from the run's `<w:rPr>` if present
- SIGNING COUNTY → UPPERCASE, no bold
- HCP Relationship values → plain text, remove `<w:b/>` if present
- DPOA body prose → remove `<w:b/>` from prose runs (keep it only on lead-in label runs)

### 4e — Repack to final output path

```bash
python /mnt/skills/public/docx/scripts/office/pack.py \
  /tmp/<ClientName>_<DocTitle>_unpacked/ \
  <OUTPUTS_DIR>/<ClientName>_<DocTitle>.docx \
  --original /tmp/<ClientName>_<DocTitle>_work.docx
```

If pack fails validation, read the error, fix the XML in the unpacked
directory, and repack. Do not deliver a document that fails packing.

### 4f — Clean up temp files

```bash
rm -rf /tmp/<ClientName>_<DocTitle>_work.docx /tmp/<ClientName>_<DocTitle>_unpacked/
```

Repeat 4a–4f for each document in the set. For married matters, complete all
five documents for the Client before starting the Spouse's set.

---

## Step 5 — Pre-Delivery Scan (Run This Before Anything Else in QA)

**Three items are consistently missed. Check these first, on every document,
before running the broader quality checklist.**

### 5a — Footer Placeholder

Three documents carry a `[CLIENT]` placeholder in the page footer:
DPOA, HCP, and AHD. The footer is a **separate XML file** (`word/footer1.xml`)
and is NOT checked when you scan `word/document.xml`. It is easy to miss.

**How to check:** After generating each document, unpack it and inspect
`word/footer1.xml` directly. Confirm that the footer text reads:

| Document | Expected footer text |
|---|---|
| DPOA | `DURABLE POWER OF ATTORNEY OF [CLIENT NAME IN CAPS]` |
| HCP | `MASSACHUSETTS HEALTH CARE PROXY OF [CLIENT NAME IN CAPS]` |
| AHD | `ADVANCE DIRECTIVE OF [CLIENT NAME IN CAPS]` |
| HIPAA | `AUTHORIZATION FOR RELEASE OF PROTECTED HEALTH INFORMATION` (static — no placeholder) |
| Worksheet | No footer |

**Split-run warning:** In the template XML, `[CLIENT]` in the footer is
split across three separate `<w:r>` runs: one run contains `[`, one contains
`CLIENT`, one contains `]`. When substituting, you must replace the
combined text across those runs — not look for the literal string `[CLIENT]`
in a single run. Inspect the raw XML before substituting to locate the
exact run boundaries.

---

### 5b — Execution / Document Date

Every document except the Worksheet has a date placeholder that must be
either populated or converted to a blank underline. These are consistently
left as literal bracket tags.

| Document | Placeholder(s) | Location |
|---|---|---|
| DPOA | `[Ordinal_DocDate]` (e.g., "21st day of May, 2025") | Execution block |
| DPOA | `[DocDate]` (e.g., "May 21, 2025") | Notary block |
| HCP | `[DocDate]` | Both notary blocks (principal + witness) |
| HIPAA | `[DocDate]` | Dated line + notary block |
| AHD | `[DocDate]` | Both notary blocks (principal + witness) |

**Rule:** If signing date is known → substitute it. If unscheduled →
replace with the correct blank form:
- `[Ordinal_DocDate]` → `_____ day of _____________, _______`
- `[DocDate]` → `____________`

A literal `[DocDate]` or `[Ordinal_DocDate]` remaining in output is a defect.

---

### 5c — Signing County

`[SIGNING COUNTY]` appears in the notary block(s) of DPOA, HCP, HIPAA,
and AHD. It must be substituted with the county name in **UPPERCASE**.

| Document | Occurrences |
|---|---|
| DPOA | 1 (principal notary block) |
| HCP | 2 (principal notary block + witness notary block) |
| HIPAA | 1 (notary block) |
| AHD | 2 (principal notary block + witness notary block) |

**Rule:** Substitute with the client's county of residence, UPPERCASE,
no "County" suffix — e.g., `NORFOLK`, `MIDDLESEX`, `SUFFOLK`.
If the signing location differs from the client's home county, use the
actual signing county (confirm with Scott). A literal `[SIGNING COUNTY]`
remaining in output is a defect.

---

## Step 5 — Full Quality Review

After the three-item pre-delivery scan passes, run the full checklist in
`references/incapacity-quality-checklist.md` PLUS the document-specific
checklists at the bottom of each article guide
(`hcp-articles.md`, `hipaa-articles.md`, `ahd-articles.md`,
`hcp-preferences-worksheet.md`, `dpoa-articles.md`). Verify file count and
naming, client-data consistency, fiduciary chain, statutory citations,
execution blocks, document-specific defaults, AND the cross-document
formatting rules (uppercase names, footer line, notary page breaks,
execution-date blanks, pronoun grammar).

**Additional formatting checks (run on every document):**
1. **All names UPPERCASE** — CLIENT and all fiduciary names appear in
   UPPERCASE plain text. No bold on name values.
2. **HCP Relationship fields plain text** — not bold.
3. **DPOA body prose not bold** — lead-in labels bold; following prose plain.
4. **No unresolved placeholders anywhere** — scan both `document.xml` AND
   `footer1.xml`. Any `[BRACKET]` tag in either file is a defect.

For DPOA specifically, the most common failure modes are:
1. Leaving literal `[IF_*]` or `[END_IF_*]` macro tags in the output
2. Leaving unresolved `[SUCCESSOR AGENT]` or other bracketed placeholders
3. Emitting both `[IF_ONE_SUCCESSOR]` and `[IF_MULTI_SUCCESSOR]` blocks
   instead of exactly one
4. Including `[IF_CO_AGENT]` content (joint/separate paragraph, co-agent
   appointment clause) for solo-agent matters
5. Including `[IF_MARRIED]` content for single clients (especially the
   entire "Care in Proximity of Spouse" section, which must be omitted
   wholesale)

If any item fails, log it as a DRAFTING NOTE inside the affected document
AND surface it in the Step 6 summary. Do NOT silently fix and ship.

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
