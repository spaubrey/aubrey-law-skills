# Add-on for trust-drafting/SKILL.md

Paste the section below into `trust-drafting/SKILL.md`, immediately AFTER
"## Step 5: Output and Deliver" and BEFORE "## Legal Compliance Guardrails".

This wires the trust-structure-flowchart skill so the explainer diagram is
produced from the same matter data trust-drafting already collected — no
re-entry of names, children, or succession.

Prerequisite: the `trust-structure-flowchart` skill folder must be installed
alongside the other skills (in the Cowork `skills/` directory).

---------------------------------------------------------------------------
## Step 6: Offer the Trust Structure Flowchart (optional)

After delivering the trust documents, offer to generate the client-facing
trust-structure flowchart:

> "Want me to also generate the trust structure flowchart for the [Family]
>  matter to send with these? (the phased marital/family-trust diagram)"

If yes, reuse the matter data you already built in Steps 1–3 — do NOT re-ask
for names, children, or succession.

1. Assemble a `matter` dict from the data already collected:
   ```json
   {
     "matter_type": "joint",            // or "individual" — same as the drafting run
     "family": "<last name>",
     "grantor1": { "first": "<client first>", "last": "<client last>" },
     "grantor2": { "first": "<spouse first>", "last": "<spouse last>" },  // joint only
     "children": ["<child 1>", "<child 2>", ...],   // real names, not placeholders
     "trustee_succession": ["survivor", "<successor 1>", "<successor 2>"],
     "withdrawal_age": 30,
     "common_trust_age": 23
   }
   ```
   Pull `trustee_succession`, `withdrawal_age`, and `common_trust_age` from the
   trust terms you just drafted so the chart matches the documents exactly.
   If any of these is ambiguous, insert a `[VERIFY: ...]` value rather than guessing.

2. Generate from the flowchart skill folder:
   ```bash
   pip install cairosvg --break-system-packages -q   # first run only
   python3 /path/to/trust-structure-flowchart/matter_to_config.py matter.json
   ```
   This writes `<Last>_Trust_Structure_Flowchart.{svg,pdf}` to
   `/mnt/user-data/outputs/` and prints the derived config for review.

3. Visually verify the PNG render (no overlapping arrows/text; names correct),
   then present the PDF (primary) and SVG (editable).

4. In the delivery summary, list the flowchart alongside the trust documents and
   note any `[VERIFY: ...]` placeholders still pending Scott's confirmation.

**Consistency rule:** The flowchart's withdrawal age, common-trust age, trustee
succession, and joint/individual structure MUST match the executed trust terms.
If you change trust terms after generating the chart, regenerate the chart.
---------------------------------------------------------------------------
