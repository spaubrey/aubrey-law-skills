# Runbook — Update pmps-prep (and pmps-proposal) for four plan structures + Clayton/QTIP

**For:** Claude in Cowork, run on the Mac mini where the skill files live.
**Style:** Execute ONE phase per turn. Stop at each checkpoint and wait for Scott's explicit "go" before the next phase. Do not batch phases. Never finalize tax figures as authoritative — all dollar figures stay flagged as estimates pending Scott's M-706 verification. Preserve existing Aubrey Law conventions (Garamond; navy #1B3A6B/1B3A5C; teal 1A7A6D; decimal numbering; cantSplit tables; section order), the `[VERIFY: ...]` behavior, and every legal-compliance guardrail. Preserve the documented April/May 2026 template patches in pmps-proposal.js (individual-client conditional guards, removed sections) — do not overwrite them.

**Staged inputs** (Scott will place these in the working area): `pmps_planstructure_samples.js`, `pmps_empty_template.js`, `pmps_planstructure_mapping.md`. Read them, but reconcile against the REAL schema — they were reconstructed from SKILL.md and field names may differ.

---

## Phase 0 — Snapshot & survey (no edits)
1. Confirm the pmps-prep skill path and whether it is under git. If under git, create a branch or note the current commit. If NOT under git, recommend `git init` on the skills directory and ask Scott whether to do so before proceeding.
2. Make a dated backup copy of the full `pmps-prep` folder AND `pmps-proposal` folder.
3. Read: `SKILL.md`, `Templates/pmps-data-schema.js` (the real SAMPLE/EMPTY), all four templates, `_shared.js`, `references/ma-estate-tax-computation.md`, and the three staged input files.
4. Report: confirmed paths, git status, backup location, and a short list of the exact field names the real schema uses for the `tax`, `fiduciaries`, `plan`, and `documents` objects (so later phases use real names, not my reconstructed ones).
**CHECKPOINT 0 — wait for "go".**

---

## Phase 1 — Tax engine ONLY (`references/ma-estate-tax-computation.md`)
Apply the focused tax-computation update:
- Verify/correct the pre-2001 state-death-tax-credit bracket table; $2M exclusion, ~$99,600 credit, $60,000 adjustment, rates to 16%, cliff structure, M-706 due 9 months.
- Define per-structure scenarios: `joint_outright` baseline (one exemption); `joint_disclaimer` & `separate_clayton` = without-planning vs. both-exemptions-preserved (2nd-death taxable = gross − $4,000,000); `individual_single` single scenario, no comparison.
- FIX the prior bug: "with planning" shelters $4,000,000, not $2,000,000; table must match narrative.
- Embed MA notes: state-only QTIP (TIR 86-4, M.G.L. c. 65C); *Shaffer v. Commissioner of Revenue*, SJC-12812 (2020); 2025 Mass. Acts Ch. 9, §35 out-of-state property computation.
- Include a worked example on a $14,391,911 gross estate (≈ $1,769,506 / $1,129,506 / $640,000), labeled estimates pending verification.
**Do not touch any template yet.** Show Scott the corrected bracket table and worked example.
**CHECKPOINT 1 — Scott confirms the methodology against his M-706 before continuing. Wait.**

---

## Phase 2 — Schema (`Templates/pmps-data-schema.js`)
1. Add `plan.planStructure` (four values) and the `clayton` / `maQtip` flags.
2. Reconcile the staged SAMPLE and EMPTY objects against the real schema; fix any key mismatches (especially `tax` intermediate fields and `fiduciaries` sub-keys). Add all four SAMPLE objects and the updated EMPTY.
3. Copy `pmps_planstructure_mapping.md` into `references/`.
**CHECKPOINT 2 — report field reconciliations made; wait for "go".**

---

## Phase 3 — Branch the templates (`pmps-prep`)
Wire `planStructure` branching into the four templates per the mapping doc: document list (1 joint vs. 2 separate vs. individual), tax section/scenarios, Clayton/QTIP subsection (full for separate_clayton, brief for joint_disclaimer, omit otherwise), *Shaffer*/§35 notes, fiduciary table layout, ILIT framing (drafting-only, one-time Crummey, 1–2 ILITs). Keep existing individual-client guards intact.
**CHECKPOINT 3 — wait for "go".**

---

## Phase 4 — Test all four structures (scratch output)
Generate the full package for each of `joint_outright`, `joint_disclaimer`, `separate_clayton`, `individual_single` using the SAMPLE objects, writing to a SCRATCH OUTPUTS folder (not a live matter). Verify:
- Tax tables shelter $4M (not $2M) and match the narrative.
- individual_single: no spouse/2nd-death references; 2-column fiduciary table.
- separate_clayton: two trusts; QTIP + Shaffer + §35 notes present.
- joint_disclaimer: disclaimer-dependency language present.
- No unresolved merge fields, no template errors.
Report results per structure with file links.
**CHECKPOINT 4 — Scott reviews rendered docs; wait for "go".**

---

## Phase 5 — Mirror to `pmps-proposal`
Apply the same four-structure logic, MA tax content, Shaffer/§35 notes, $4M fix, and ILIT framing to pmps-proposal. Keep its tax-computation reference in sync with pmps-prep. Re-run a spot test for at least separate_clayton and individual_single.
**CHECKPOINT 5 — wait for "go".**

---

## Phase 6 — Finalize
1. Update `learnings.md` in both skills noting what changed and the date.
2. Produce a summary: files changed, field reconciliations, all `[VERIFY]` items, and a reminder that tax figures are estimates pending M-706 verification.
3. If under git, stage commits per phase (or one well-described commit) — but do NOT push/commit without Scott's confirmation.

**Stop conditions (any phase):** if the real schema diverges materially from the staged files, if a template has guards that would be overwritten, or if any tax figure can't be reconciled — pause and ask Scott rather than guessing.
