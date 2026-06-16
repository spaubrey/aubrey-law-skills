# Running the Generator

All commands run from inside `assets/generator/`. Save the client JSON wherever
convenient, but put `--out` INSIDE the generator directory.

## 1. Report (dry run — no documents written)

Use this first to confirm data and clause selection:

```bash
python3 al-generator.py report --data <data.json> --package <package> --state MA
```

The JSON output to confirm:
- `missing_fields`: must be empty. If populated, the named dotted-path fields are
  absent — add them to the client JSON.
- `errors`: must be empty. Errors name the document and the cause (missing field,
  unapproved clause, missing template).
- `included_clauses`: the clauses that will appear — confirm expected ones are
  present (e.g. guardian clause only when there are minor children).
- `skipped_clauses`: clauses correctly omitted because their condition was false.

## 2. Generate (writes .docx + report)

```bash
python3 al-generator.py generate --data <data.json> --package <package> --state MA --out output/<client-run>
```

- `--out` MUST be a path inside `assets/generator/` (e.g. `output/smith-2026`).
  Outside the root raises `ValueError: ... is not in the subpath of ...`.
- On success: `errors` empty AND `unresolved_markers` empty. Unresolved markers
  mean a placeholder or bracketed marker survived rendering — investigate the
  template/data before delivering.
- Output files and `generation-report.json` are written to the `--out` directory.
- Body text is forced to Garamond 12pt, footers to 10pt, automatically.

## 3. Validate a single template (optional)

```bash
python3 al-generator.py validate --data <data.json> --template templates/<file>.docx --state MA
```
Lists the placeholders and logic tags found in that template.

## Common issues

- **`Unsupported state`** — the generator is MA only; pass `--state MA`.
- **`Template not found`** — supply the firm-form template (see
  `generator-setup.md`).
- **`Clause ... is marked 'draft'`** — a clause is unapproved. Do NOT pass
  `--allow-draft` for client deliverables; resolve the clause's review status.
- **Missing execution fields when `signing_scheduled: true`** — the generator also
  requires `doc_date`, `ordinal_doc_date`, signing county, and notary commission.
  For an unscheduled signing set `signing_scheduled: false` instead.
- **Stopped after the first file** — on a render error the generator records the
  error and stops; read `errors` in the report, fix, and re-run.

## Interpreting the generation report

Always read the report after generating. A clean run shows empty `missing_fields`,
empty `errors`, empty `unresolved_markers`, the expected `included_clauses`, and a
complete `output_files` list matching the package's document count.
