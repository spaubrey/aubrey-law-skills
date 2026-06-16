---
name: draft-estate-plan-documents
description: >
  [OUTCOME]: Generates a complete set of Massachusetts estate-planning documents
  (.docx) for a client by building structured client data and running the bundled
  al-generator document generator. Supports the core estate package, incapacity
  documents, pour-over will, and individual/joint revocable trusts.
  [TRIGGER]: Activates when the user says "draft estate plan documents," "generate
  the estate plan," "run the document generator," "draft the trust/will/POA/health
  care proxy for [client]," "generate the incapacity package," "draft the pour-over
  will," or "/draft-estate-plan-documents."
  [ANTI-TRIGGER]: Does NOT activate for estate-plan summaries, closing/funding
  packages, engagement agreements, deed drafting, intake questionnaires, plan
  review, billing, or general estate-planning questions. Use the matching dedicated
  skill for those.
---

# Draft Estate Plan Documents

Generate Massachusetts estate-planning documents by assembling structured client
data and running the bundled `al-generator.py` document generator.

## Before You Start

1. Read `firm-context.md` (in this skill folder or the working directory) for firm
   practice area, jurisdiction (MA only), formatting standards, and quality
   preference.
2. Check whether the current directory has a `claude.md` (matter file). If it does,
   read it for case context — parties, children, fiduciaries, trust name, signing
   date — and pre-fill answers, skipping any question it already answers.
3. Read `learnings.md` in this skill folder and apply any rules.
4. Confirm the generator is set up: see `references/generator-setup.md`. The full
   engine AND the firm's real form templates are bundled in `assets/generator/`, so
   all five packages work out of the box; the only setup step is installing
   `requirements.txt`.

## Step 1: Choose the Package

Ask the user which document set to generate (AskUserInput, single-select):
- `core-estate` — will, revocable trust, POA, health care proxy, living will, HIPAA, ancillary
- `incapacity-documents` — durable POA, health care proxy, living will, HIPAA
- `pourover-will` — pour-over will only
- `joint-trust-simplified` — joint revocable trust (married grantors)
- `trust-individual-single` — individual single revocable trust (unmarried grantor)

Each package's required fields and document list are defined in
`assets/generator/packages/<package>.json`. Read the chosen one before interviewing.

## Step 2: Collect Client Data

Read `references/intake-fields.md` for the per-package question set and the JSON
shape each package expects. Use AskUserInput (3–7 questions per screen) for the
inputs that change each run — client/spouse names, children (and minor status),
fiduciaries, trust name/date, blended-family children, disinheritance, signing
details. Do not ask for anything `claude.md` or `firm-context.md` already answers.

Mirror the matching `assets/generator/examples/*.json` file exactly for structure.
Build the client JSON from the answers and save it to the output run folder.

## Step 3: Validate Before Generating

Run, from inside `assets/generator/`:
```bash
python3 al-generator.py report --data <data.json> --package <package> --state MA
```
Read `references/running-the-generator.md`. Confirm the report shows no
`missing_fields`, no `errors`, the expected `included_clauses`, and correctly
`skipped_clauses`. Fix data and re-run until clean.

## Step 4: Generate

```bash
python3 al-generator.py generate --data <data.json> --package <package> --state MA --out output/<client-run>
```
**The `--out` path must be inside `assets/generator/`** (e.g. `output/smith-2026`),
or the generator raises a ValueError. Confirm the printed report has empty
`errors` and empty `unresolved_markers`. The generator enforces Garamond 12pt
body / 10pt footer automatically.

## Step 5: Quality Review (client-facing — runs by default)

Estate-plan documents are client-facing final deliverables, so per firm preference
the quality review runs by default. Launch a fresh sub-agent reviewer using
`references/quality-review.md` to check the generated documents against the intake
data and the generation report. Surface any discrepancies before delivery; do not
silently fix legal text.

## Step 6: Deliver

Move the documents to the matter's storage (firm uses MS365 / OneDrive). Present
the file list with a header:

> [REQUIRES ATTORNEY REVIEW] — These are automation-generated DRAFTS. A Massachusetts
> attorney must review and approve every document before signing, filing, or client use.

Then log feedback: ask "Did the generated documents meet your expectations? Anything
to improve for next time?" and record useful rules in `learnings.md`.

## Legal Compliance Guardrails (mandatory)

1. **Source citations:** Document text comes only from the bundled templates and
   approved clauses. Never invent or substitute legal language from memory.
2. **Uncertainty flagging:** If unsure whether data maps to a field, flag it
   "[REQUIRES VERIFICATION]" rather than guessing. Never guess a fiduciary,
   beneficiary, date, or trust term.
3. **Not legal research:** This skill assembles firm forms with client data; it
   does not provide legal advice or research and must not be presented as such.
4. **Preserve original language:** Do not paraphrase or edit template/clause legal
   text. Only merge structured field values.
5. **Attorney review required:** Every output carries the [REQUIRES ATTORNEY REVIEW]
   header. MA attorney review is required before any document is used.

## Notes

- Jurisdiction is Massachusetts only. The generator rejects other states.
- The generator blocks unapproved clauses unless `--allow-draft` is passed; use
  draft mode only for internal template development, never for client deliverables.
- For unscheduled signings, set `execution.signing_scheduled: false` and the
  execution date/county/notary fields render as blank lines.
