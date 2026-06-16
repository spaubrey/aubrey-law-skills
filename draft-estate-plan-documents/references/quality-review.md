# Quality Review (Sub-Agent Reviewer)

Estate-plan documents are client-facing final deliverables. Per firm preference
("Only for court filings and client-facing"), this review runs by default before
delivery. Launch a FRESH sub-agent so the review is independent of the drafting
context.

## Inputs to give the reviewer

1. The client JSON used for generation (`<data.json>`).
2. The `generation-report.json` from the `--out` directory.
3. The generated `.docx` files (extract their text for review).
4. The chosen package config `assets/generator/packages/<package>.json`.

## Checklist

The reviewer confirms, citing the specific document and field for each finding:

- [ ] **Completeness** — every document listed in the package config was produced
      (`output_files` count matches `documents` count).
- [ ] **No unresolved markers** — `unresolved_markers` is empty; no `{{ }}`,
      `{% %}`, or `[BRACKET]` text remains in any document.
- [ ] **Name accuracy** — client, spouse, children, fiduciaries, beneficiaries, and
      trust name in the documents match the client JSON exactly (allowing for the
      automatic UPPERCASE rendering).
- [ ] **Conditional correctness** — guardian provisions appear only with minor
      children; spouse language appears only when a spouse exists; blended-family,
      disinheritance, TPP method, descendant-distribution method, and co-trustee
      manner-of-acting match the data.
- [ ] **Execution block** — if `signing_scheduled: true`, dates/county/notary show
      real values; if false, they show blank lines (and that is intended).
- [ ] **Formatting** — body text Garamond 12pt, footer 10pt.
- [ ] **No fabricated legal text** — all legal language traces to bundled templates
      and approved clauses; nothing was invented or paraphrased.

## Output

The reviewer returns a short report:
- **PASS** — all checks satisfied; ready for attorney review.
- **ISSUES FOUND** — list each issue with the document name, the field/section, the
  expected value (from client JSON), and the observed value. For legal-text
  concerns, flag "[REQUIRES VERIFICATION]" and do NOT auto-edit document language;
  surface to the attorney instead.

Do not deliver to the client until issues are resolved or the attorney has signed
off. All output still carries the [REQUIRES ATTORNEY REVIEW] header regardless of
review outcome.
