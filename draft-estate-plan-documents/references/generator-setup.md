# Generator Setup

The document generator is bundled at `assets/generator/` inside this skill. It is a
complete copy of the firm's `aubreylaw-docgeneration` repository: the
`al-generator.py` engine, all packages, clauses, MA state rules, schema, example
data, the firm's real form-based `.docx` templates, the `source-forms/` originals,
the template-conversion tools, and the test suite.

## One-time setup (per environment)

From `assets/generator/`:

```bash
pip install -r requirements.txt --break-system-packages   # docxtpl, python-docx, jinja2
```

That's it. The real firm templates ship in `templates/`, so all six packages work
out of the box — no template-building step is required.

Optional sanity check (runs the repo's own tests):

```bash
python3 -m unittest discover -s tests
```

## Templates (already bundled)

Every package's templates are present in `assets/generator/templates/`:

| Package | Templates used |
| --- | --- |
| `core-estate` | will, revocable-trust, durable-power-of-attorney, health-care-proxy, living-will, hipaa-authorization, ancillary-execution |
| `incapacity-documents` | durable-power-of-attorney, health-care-proxy, living-will, hipaa-authorization |
| `pourover-will` | pourover-will |
| `joint-trust-simplified` | joint-trust-simplified |
| `trust-individual-single` | trust-individual-single |

These are the firm's full legal forms (Aubrey Law letterhead, complete clause
language), not simplified starters.

## Rebuilding templates from source forms (only if forms change)

If the firm updates a source form, rebuild the affected template from
`source-forms/` using the matching converter in `tools/`, then re-run the tests:

- `python3 tools/convert_incapacity_docs.py` (POA, HCP, living will, HIPAA)
- `python3 tools/convert_pourover_will.py`
- `python3 tools/convert_joint_trust.py`
- `python3 tools/convert_joint_trust_simplified.py`
- `python3 tools/convert_trust_individual_single.py`
- `python3 tools/create_sample_templates.py` (simplified core-estate starters)

Do not hand-edit compiled templates; change the source form and re-convert so the
placeholder mapping stays consistent.

## Critical operational rule

`al-generator.py` computes output paths relative to the generator root, so the
`--out` directory **must be inside `assets/generator/`** (e.g. `--out output/smith`).
A path outside the root raises `ValueError: ... is not in the subpath of ...`.
