# Engagement Agreement Template — Field Reference

## Source of truth

Canonical Mustache template (human-readable, editable in Word):
- SharePoint: `Estate Planning Templates/Engagement Agreement_ep.docx`

Skill's rendering template (Jinja2 + DocuSeal markers):
- `assets/engagement_template.docx` — produced by converting the Mustache
  template once via `scripts/convert_template.py`. If the SharePoint source
  changes, re-run the converter and re-deploy.

## Render variables

| Variable | Type | Notes |
| --- | --- | --- |
| `client_name` | string | "First Last" — primary client |
| `spouse_name` | string | "First Last" — only when `couple` is true; safe to pass `None` otherwise |
| `couple` | bool | If true, joint representation section appears and spouse signature block is added |
| `trust_plan` | bool | If true, trust-based document list shows; if false, will-based list shows |
| `trust_label` | string | First line of trust scope (non-LP path) — see "Trust label derivation" below |
| `trust_label_lp` | string | First line of trust scope (LP path) — appends " (No Tax Planning)" |
| `legal_plan` | bool | If true, LP scope + LP billing language appears; LP suppresses several lines from the non-LP scope list |
| `legal_plan_name` | string | Normalized plan name (see normalization below) |
| `deed` | bool | If true and trust_plan is true, the "(1) Quitclaim Deed" line appears in scope |
| `flat_fee_amount` | string | Formatted number without "$" sign, e.g. `5,500` — only used when legal_plan is false |
| `credit_shelter` | bool | If true and legal_plan is true, Addendum A (CST) is appended |

## DocuSeal field markers (literal, NOT render variables)

These appear in the rendered .docx as literal text and are detected by
DocuSeal on upload. Do not pass these as render variables.

| Marker | Field type | Role |
| --- | --- | --- |
| `{{Client Signature;type=signature;role=Client;required=true}}` | signature | Client |
| `{{Client Date;type=date;role=Client;required=true}}` | date | Client |
| `{{Spouse Signature;type=signature;role=Spouse;required=true}}` | signature | Spouse |
| `{{Spouse Date;type=date;role=Spouse;required=true}}` | date | Spouse |
| `{{CST Election;type=checkbox;role=Client;required=false}}` | checkbox | Client |

Spouse markers and CST marker only appear in the rendered output when their
respective conditionals are true (`couple` and `credit_shelter`).

## Trust label derivation

Derived in the render script from `trust_type` + `couple` + `legal_plan`:

| trust_type | couple | trust_label (non-LP) | trust_label_lp (LP) |
| --- | --- | --- | --- |
| `joint` | true | `Joint Revocable Trust` | `Joint Revocable Trust (No Tax Planning)` |
| `separate` | true | `Two Revocable Trusts (one per spouse)` | `Two Revocable Trusts (No Tax Planning, one per spouse)` |
| `individual` | false | `Revocable Trust` | `Revocable Trust (No Tax Planning)` |

If `trust_type=joint` but `couple=false`, the script raises a validation
error — joint trusts only make sense for couples.

## Plan name normalization

Common legal insurance plan names that include " Legal" in them produce
awkward output ("MetLife Legal Legal Insurance Plan") if passed raw.
The render script strips a trailing " Legal" from these inputs before
substitution. Final substituted form: `{name} Legal Insurance Plan`.

| User-entered name | Normalized form used in render | Output reads as |
| --- | --- | --- |
| `MetLife Legal` | `MetLife` | `MetLife Legal Insurance Plan` |
| `Hyatt Legal` | `Hyatt` | `Hyatt Legal Insurance Plan` |
| `ARAG` | `ARAG` | `ARAG Legal Insurance Plan` |
| `LegalEASE` | `LegalEASE` | `LegalEASE Legal Insurance Plan` |
| `LegalShield` | `LegalShield` | `LegalShield Legal Insurance Plan` |

Override possible by passing `legal_plan_name` explicitly to the script.

## Validation rules (the render script enforces these)

1. If `couple` is true, `spouse_name` and `spouse_email` are required.
2. If `legal_plan` is false, `flat_fee_amount` is required and must be a
   positive number (the script accepts `5500`, `5,500`, `5500.00` — all are
   normalized to `5,500`).
3. If `legal_plan` is true, `legal_plan_name` is required, `flat_fee_amount`
   is ignored, and `credit_shelter` is only honored when `couple` is true
   (single-client CST addendum is not meaningful in MA estate planning).
4. If `trust_plan` is false, `deed` is forced to false (a will plan has no
   trust to deed property into).

If validation fails, the script returns a structured error listing which
fields are missing or invalid — do not retry without addressing each item.
