# Master Prompt — Update pmps-prep & pmps-proposal for four plan structures + Clayton/QTIP

Paste this into a Cowork session on the Mac mini where the skill files live. Four supporting files are staged in the working area:

- `pmps_update_runbook.md` — the phase-by-phase runbook you will follow
- `pmps_planstructure_samples.js` — four SAMPLE data objects
- `pmps_empty_template.js` — blank EMPTY scaffold
- `pmps_planstructure_mapping.md` — structure-to-behavior reference

---

## The prompt

I need you to update my `pmps-prep` skill (and then mirror the changes to `pmps-proposal`) to support four distinct estate-plan structures and to incorporate Clayton election and Massachusetts-specific QTIP planning.

**Follow `pmps_update_runbook.md` exactly. Execute ONE phase per turn and stop at each checkpoint to wait for my explicit "go" before continuing. Do not batch phases.**

Key rules that apply to every phase:

1. **Snapshot before editing.** Confirm whether the skills directory is under git; if not, recommend initializing it. Make a dated backup of both `pmps-prep` and `pmps-proposal` before any edit.
2. **Tax figures are never authoritative.** Every dollar figure stays flagged as an estimate pending my M-706 verification. Stop after the tax-engine phase and let me confirm the methodology before anything else branches on it.
3. **Reconcile against the real schema.** The staged sample/empty files were reconstructed from SKILL.md — field names may differ from the real `Templates/pmps-data-schema.js`. Read the real schema first and fix any key mismatches (especially the `tax` intermediate fields and `fiduciaries` sub-keys) rather than trusting my reconstructions.
4. **Preserve what exists.** Keep all Aubrey Law conventions (Garamond; navy #1B3A6B/1B3A5C; teal 1A7A6D; decimal numbering; cantSplit tables; section order), the `[VERIFY: ...]` behavior, every legal-compliance guardrail, and the documented April/May 2026 pmps-proposal individual-client guards and removed sections. Do not overwrite them.

**The four structures** (new field `plan.planStructure`):

- `joint_outright` — Joint Trust, Outright to Spouse. No credit shelter funded; one $2M MA exemption used. Baseline/minimal-planning case; quantify the lost-exemption exposure.
- `joint_disclaimer` — Joint Trust, Disclaimer Planning. Single joint trust; survivor may disclaim into a credit shelter trust within 9 months. Explain the upside and the dependency/risk (survivor must disclaim correctly and timely or the planning fails).
- `separate_clayton` — Separate Revocable Trusts + Credit Shelter + Clayton Election. Two trusts; fiduciary-controlled election of the credit-shelter/marital (QTIP) division at the first death; both $2M exemptions preserved ($4M total). Premium, most reliable option.
- `individual_single` — Individual Trust for a single person. No marital/credit-shelter/Clayton/QTIP machinery; one $2M exemption; single-death tax scenario; no spouse references.

**Massachusetts content to incorporate** (couples; partial for individual): $2M exclusion, anti-cliff credit, rates to 16%, federalized base (IRC 12/31/2000), no portability, M-706 due 9 months; the state-only QTIP election independent of the federal election (TIR 86-4, M.G.L. c. 65C); the *Shaffer v. Commissioner of Revenue*, SJC-12812 (2020) election-coordination caution; and the 2025 Mass. Acts Ch. 9, §35 out-of-state-property computation (flag illiquid business interests for situs review).

**Critical tax fix:** the prior logic sheltered only $2M in the "with planning" column while the text claimed $4M. The "both exemptions preserved" scenario must reduce the second-death taxable estate by $4,000,000 and the rendered table must match the narrative.

**ILIT framing** (optional, all structures): drafting-only; a new ILIT-owned policy from inception avoids the IRC §2035 three-year lookback; engagement is drafting + one-time first-year Crummey notices; insurance procurement and ongoing annual Crummey notices excluded. One or two ILITs (concurrent-vs-deferred) for couples; one for an individual.

Use `pmps_planstructure_mapping.md` as the authority for how each structure toggles flags, tax logic, documents, and proposal/worksheet sections. Use the SAMPLE and EMPTY files for the schema work (after reconciling field names). Test all four structures to a scratch output folder before mirroring to `pmps-proposal`.

Begin with Phase 0 of the runbook and stop at the checkpoint.

---

## Quick-start checklist for Scott

1. [ ] Stage all five files (this prompt + four support files) in the Cowork working area
2. [ ] Confirm/initialize git on the skills directory
3. [ ] Paste the prompt above; let it run Phase 0; review the backup + schema field report
4. [ ] Phase 1 (tax engine) — **verify the numbers against your M-706 before "go"**
5. [ ] Phases 2–3 — schema + template branching
6. [ ] Phase 4 — open all four rendered sample packages and check them
7. [ ] Phase 5 — mirror to pmps-proposal
8. [ ] Phase 6 — learnings.md + commit
