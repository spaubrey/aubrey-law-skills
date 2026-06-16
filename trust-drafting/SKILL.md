---
name: trust-drafting
description: >
  [OUTCOME]: Drafts a Massachusetts revocable trust package (individual or
  joint) — Revocable Trust, Pour-Over Will, Funding Instructions & Checklist,
  Assignment of Personal Property (per person), and Certificate of Trust — as
  print-ready .docx. When a client financial summary spreadsheet is provided,
  also drafts a client-specific Trust Funding Plan: named assets, real values,
  per-asset actions, and a numbered priority checklist, alongside the Funding
  Instructions. Legal instruments use Garamond black; funding docs keep Aubrey
  branding.
  [TRIGGER]: "draft trust documents," "draft the trust," "individual/joint
  revocable trust," "trust and pour-over will," "generate trust package,"
  "funding checklist," "funding plan," or "/trust-drafting." Also triggers when
  client intake data or a financial summary spreadsheet accompanies a drafting
  request.
  [ANTI-TRIGGER]: NOT for incapacity-only documents, will-only plans, trust
  amendments, deed transfers, post-signing closing packages, plan summaries,
  or engagement agreements.
---

# Trust Drafting Skill

## Purpose
Draft the complete Aubrey Law revocable trust package for a new matter.
Produces six documents (five for an individual client): Revocable Trust,
Pour-Over Will, Funding Instructions & Checklist, Assignment of Personal
Property (per person), and Certificate of Trust. When a client financial
summary spreadsheet is provided, additionally produces a client-specific
**Trust Funding Plan** built from that data.

## Before Starting
1. Check this directory for a `claude.md` or `CLAUDE.md` file. If found,
   read it for matter context (client names, dates, fiduciaries, asset profile).
   Use it to pre-fill inputs and skip questions already answered.
2. Read `learnings.md` in this skill folder. Apply any rules listed there.
3. Read `references/firm-context.md` for firm branding and standards.

---

## Step 1: Collect Client Data

Use AskUserInput to gather what is not already in `claude.md`.
Read `references/intake-questions.md` for the full question set.

Minimum required fields:
- Trust type: Individual or Joint
- Client full name, address, city, county (MA)
- Spouse full name and address (joint only)
- Trust name (e.g., "The John Smith Revocable Trust")
- Date of trust execution (or "TBD" — use blank line)
- Initial co-trustee (if any) — name and relationship
- Successor trustee(s) — names and relationship
- Personal representative(s) / executor(s) for Pour-Over Will
- Guardian(s) — required only if minor children exist
- Children (names, DOB if minors)
- Signing county (for notary blocks)

Ask no more than 8 questions in one pass. Collect remaining data in a
second pass if needed.

---

## Step 2: Select Templates and Load References

1. **Individual trust** → use template logic in `references/individual-trust-guide.md`
2. **Joint trust** → use template logic in `references/joint-trust-guide.md`
3. **Pour-Over Will** → use `references/pourover-will-guide.md`
4. **Funding Instructions** → read `references/funding-instructions-guide.md`
5. **Trust Funding Plan** (only if a client financial summary spreadsheet is
   provided) → read `references/funding-checklist-guide.md`
6. **Assignment of Personal Property** → read `references/assignment-cert-guide.md`
7. **Certificate of Trust** → read `references/assignment-cert-guide.md`

Load only the reference(s) needed for the document currently being drafted.
Release each reference before loading the next.

---

## Step 3: Draft Documents — Order of Operations

Draft in this sequence (each as a separate .docx):

1. **Revocable Trust** (`YYYY-MM-DD_[Trust-Name]_[CLIENT-LAST-NAME].docx`)
   - Fill all `[PLACEHOLDER]` and `{{ template }}` fields
   - Apply correct singular/plural language per trust type
   - Include co-trustee provisions only if co-trustee named
   - See `references/individual-trust-guide.md` or `references/joint-trust-guide.md`

2. **Pour-Over Will** (`YYYY-MM-DD_Pour-Over-Will_[CLIENT-LAST-NAME].docx`)
   - For joint trusts: one will per spouse
   - Cross-reference trust name and date
   - Include guardian clause only if minor children
   - See `references/pourover-will-guide.md`

3. **Trust Funding Instructions & Checklist**
   (`YYYY-MM-DD_Funding-Instructions_[CLIENT-LAST-NAME].docx`)
   - Full Aubrey Law branded document
   - Suppress irrelevant asset rows per client profile
   - See `references/funding-instructions-guide.md`

3a. **Trust Funding Plan** — ONLY if a client financial summary spreadsheet was
   provided (`YYYY-MM-DD_Trust-Funding-Plan_[CLIENT-LAST-NAME].docx`)
   - This is a separate, client-specific deliverable produced *in addition to*
     the generic Funding Instructions above.
   - Read the spreadsheet and build the asset inventory, per-asset actions, and
     numbered priority checklist from the client's real data.
   - **MANDATORY STRATEGY GATE:** Before drafting the narrative recommendation
     sections, use AskUserInput to ask Scott which tax/structuring strategies to
     include for this matter (interspousal equalization, bypass funding,
     see-through beneficiary designations, TIC retitling, etc.). Offer only
     strategies the asset data supports. Omit narrative + checklist rows for any
     strategy he declines.
   - See `references/funding-checklist-guide.md`

4. **Assignment of Personal Property** — one per person
   - Individual: `YYYY-MM-DD_Assignment-of-Personal-Property_[CLIENT-LAST-NAME].docx`
   - Joint: two files, one per spouse
   - See `references/assignment-cert-guide.md`

5. **Certificate of Trust**
   (`YYYY-MM-DD_Certificate-of-Trust_[CLIENT-LAST-NAME].docx`)
   - One per matter regardless of trust type
   - Vary language for individual vs. joint and co-trustee vs. not
   - See `references/assignment-cert-guide.md`

---

## Step 4: Formatting Standards

**Legal instruments** (Revocable Trust, Pour-Over Will, Assignment of
Personal Property, Certificate of Trust):
- **Font:** Garamond throughout — 12pt body, 14pt bold titles
- **Color:** Black `000000` only. No navy, no teal, no gray accents.
- **No logo.** No header image. Plain header (or none).
- **Footer:** Plain black text, document title and page number only
  (e.g., `ASSIGNMENT OF PERSONAL PROPERTY FOR [CLIENT FULL NAME] | 1`)
- **Page:** US Letter 12240 × 15840 DXA; margins Top/Bottom 1080, Left/Right 1008

**Funding Instructions & Checklist** (client guide, not an executed
legal document): retains full Aubrey Law branding — logo header, navy
accents, firm footer — per `references/funding-instructions-guide.md`.

**Docx-js:** Always set page size explicitly. Never use unicode bullets.
Use `LevelFormat.BULLET` for lists. See DOCX skill for full rules.

Use `npm install -g docx` and generate via JavaScript.
Run `python scripts/office/validate.py [file].docx` after each file.

---

## Step 5: Output and Deliver

Save all files to `/mnt/user-data/outputs/`.

Announce each file as it completes. After all files:
- Confirm which documents were generated
- Note any placeholders left blank (e.g., trust date if TBD)
- Note any rows suppressed in the checklist
- Flag anything requiring attorney review

---

## Legal Compliance Guardrails (Mandatory)

1. **Source citations:** All statutory language (M.G.L. citations in Certificate
   of Trust) must be reproduced verbatim from `references/assignment-cert-guide.md`.
   Never paraphrase statutory text.
2. **Uncertainty flagging:** If any field is ambiguous or missing, insert
   `[REQUIRES COMPLETION]` and flag it in the delivery summary.
3. **Not legal advice:** These are drafting tools. Claude does not make legal
   judgments about appropriate trust structure, tax treatment, or fiduciary selection.
4. **Preserve original language:** Do not paraphrase trust boilerplate. Use
   exact language from the template source files.
5. **Attorney review required:** Every output includes the note:
   *"Draft documents — requires attorney review before execution."*

---

## Learnings
Check `learnings.md` before each run. After completing the package, ask:
"Did the output meet your expectations? Anything to improve for next time?"
Log useful feedback to `learnings.md`.
