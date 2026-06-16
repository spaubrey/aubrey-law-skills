---
name: send-estate-planning-engagement
description: >
  [OUTCOME]: Generates a fully populated Aubrey Law estate planning engagement
  agreement as a branded .docx, saves it to the lead's OneDrive folder
  (creating year/lead folders as needed), uploads it to DocuSeal as a new
  per-client template, and sends it for signature. Returns the DocuSeal
  signing URL(s) for the client(s).
  [TRIGGER]: Activates when Scott says "send the engagement agreement to
  [client]", "send EP engagement to [client]", "engagement agreement for
  [client]", "send engagement for the [client] matter", "draft and send the
  engagement", "/send-estate-planning-engagement", or any request to send an
  estate planning engagement agreement via DocuSeal to a new client or lead.
  [ANTI-TRIGGER]: Does NOT activate for trust drafting, will drafting, closing
  packages, deed drafting, intake questionnaires, the PMPS proposal flow,
  changing a matter stage, or sending payment links. Does NOT trigger for
  non-estate-planning engagement agreements (e.g., litigation matters).
---

# Send Estate Planning Engagement Agreement

## Purpose

Produce a customized Aubrey Law estate planning engagement agreement and send
it to the client(s) for signature via DocuSeal in one workflow. Save a Word
copy to the lead's OneDrive folder for the file.

## What this skill does, in order

1. Confirm firm context exists; if `firm-context.md` is missing in the working
   directory, create it from defaults below.
2. Gather per-matter inputs (see Step 1 below). Manual entry — do not assume
   from prior conversation unless Scott explicitly says "use the info above."
3. Render the engagement Word doc from `assets/engagement_template.docx`
   using `scripts/render_engagement.py`.
4. Ensure the lead's OneDrive folder exists (year folder + lead folder per
   `references/lead-folder.md`); save the rendered .docx there.
5. Upload the .docx to DocuSeal as a new template via the direct REST API
   (`scripts/docuseal_upload.py` + `references/docuseal-workflow.md`); fall
   back to manual editor upload only if the REST call fails.
6. Send the template to the client(s) for signature; return signing URLs and
   the OneDrive file path.

Each step requires explicit Scott confirmation before the next.

## Step 1 — Gather inputs

Ask for these fields. Use the ask_user_input_v0 tool for the boolean choices.
Do NOT proceed until all required fields are answered.

| Field | Type | Required when |
| --- | --- | --- |
| Client first name, last name | text | always |
| Client email | text | always |
| Client phone (E.164) | text | optional |
| Couple? | bool | always |
| Spouse first name, last name | text | if couple |
| Spouse email | text | if couple |
| Spouse phone (E.164) | text | optional |
| Trust plan or will plan? | choice | always |
| Trust type (joint / separate / individual) | choice | if trust plan |
| Includes a deed transfer? | bool | if trust plan |
| Legal insurance plan? | bool | always |
| Plan name (ARAG / MetLife / Hyatt / LegalShield / LegalEASE / Other) | choice | if legal plan |
| Flat fee amount (no $, no commas in form; e.g., 5500) | text | if NOT legal plan |
| Credit Shelter (CST) addendum? | bool | if legal plan + couple |

See `references/template-fields.md` for the full variable map and how trust
labels are derived from trust type + couple status + legal plan status. Plan
name normalization (e.g., stripping " Legal" suffix to avoid "MetLife Legal
Legal Insurance Plan") is handled in the render script.

## Step 2 — Render the Word doc

Call `scripts/render_engagement.py` with the collected inputs. It outputs a
.docx with the firm-branded engagement agreement, all conditional sections
resolved, and DocuSeal field markers (signature/date/checkbox) embedded so
DocuSeal auto-detects them on upload.

Show Scott the rendered doc path and a short confirmation summary:
- Client(s) name and email(s)
- Plan type (trust vs. will)
- Fee structure (flat fee $X or legal insurance plan Y)
- CST addendum (if applicable)
- Deed clause (if applicable)

Ask: "Open the rendered doc and review before we proceed to upload?"
If Scott opens it and requests changes, re-render with corrected inputs.

## Step 3 — Save to OneDrive lead folder

See `references/lead-folder.md` for the full naming and creation logic.
Summary:

- Parent: `/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning`
- Lead folder (flat, directly under Estate Planning — no year subfolder):
  - Flat fee (EP): `YYYY-EP-LastName, FirstName & SpouseFirst`
    — e.g. `2026-EP-Doe, John & Jane`
  - Legal plan (EP-LP): `YYYY-EP-LP-LastName, FirstName & SpouseFirst`
    — e.g. `2026-EP-LP-Smith, Sean & Sara`
- Prefix branch (`EP` vs `EP-LP`) is keyed off `legal_plan`.
- Spouse with different surname: `& SpouseFirst-SpouseLast`.
- File: `Engagement Agreement - LastName - YYYY-MM-DD.docx`

The script `scripts/send_engagement.py` creates missing folders with
`mkdir -p` and saves the rendered .docx there. Do not overwrite an existing
file with the same name — append a numeric suffix (`-2`, `-3`, ...) instead.

## Step 4 — Upload to DocuSeal

See `references/docuseal-workflow.md` for full details. The flow has four
sub-steps. Each requires Scott's explicit go-ahead before the next.

### 4a. Check for an existing template (duplicate guard)

Before creating anything in DocuSeal, call `DocuSeal:search_templates` with
the proposed name (`Engagement Agreement — LastName — YYYY-MM-DD`). If an
exact-name match exists:

- Surface the existing template (id, created date) to Scott.
- Ask: **reuse the existing template** / **append a version suffix**
  (`— v2`, then `— v3`, ...) / **abort**.
- Default to "append version suffix" only if Scott picks neither "reuse"
  nor "abort." Never silently create a duplicate.

If no exact-name match, proceed to 4b.

### 4b. Create the template

**Primary path — direct REST API upload (`scripts/docuseal_upload.py`):**

1. Confirm `docuseal_api_token` is set in `firm-context.md` and is not a
   placeholder.
2. Run the helper script:

   ```bash
   python3 scripts/docuseal_upload.py \
     --file "<path to saved .docx>" \
     --name "Engagement Agreement — LastName — YYYY-MM-DD" \
     --token-from-context firm-context.md \
     --out-json /tmp/docuseal_upload_result.json
   ```

   On success, the script's output JSON contains `template_id`,
   `template_name`, `roles`, `fields`, and `edit_url`. Capture
   `template_id` for steps 4c and 5.

3. If the script exits non-zero (network error, 4xx/5xx, malformed
   response), read the error from `out-json` and surface it to Scott
   verbatim, including HTTP status if present. Then offer the manual
   fallback below.

**Fallback path — manual upload (only if REST upload fails or token is
absent):**

1. Call `DocuSeal:create_template` with `name` only (no `url`). The
   response includes `edit_url`.
2. Show Scott the local .docx path and the `edit_url`; instruct him to
   drag the file into the DocuSeal editor. Wait for explicit "uploaded"
   confirmation before continuing to 4c.

The Make.com SharePoint share-link path has been retired. The setup notes
remain in `references/make-webhook-setup.md` for reference only — do not
use that route without explicit instruction from Scott.

### 4c. Validate the created template

Call `DocuSeal:load_template` with the returned `template_id`. Check
explicitly — do not just confirm the call returned 200:

- **Single client:** exactly one role named `Client`, with at least one
  field of `type=signature` and one of `type=date` assigned to it.
- **Couple:** roles `Client` AND `Spouse` both present, each with its own
  signature + date fields.
- **If `credit_shelter` is true:** a `type=checkbox` field on the `Client`
  role for CST election.

If validation fails, report the specific gap to Scott (e.g., "expected
`Spouse` role, got only `Client`" or "no signature field on `Client`") and
fall through to manual upload (4b fallback). Do NOT call `send_documents`
against a half-detected template.

### 4d. Confirm before send

Show Scott a send summary in this exact form:

```
Template: <name> (#<template_id>)
Submitters:
  Client: <name> <email>[, +1...]
  Spouse: <name> <email>[, +1...]    ← only if couple
Fields prefilled: NONE

Confirm? (yes / no / edit emails)
```

Never call `send_documents` without an explicit "yes." If Scott says "edit
emails," correct them in-conversation and re-show this summary before
sending.

## Step 5 — Send for signature

Only after the Step 4d "yes" confirmation, call `DocuSeal:send_documents`
with `template_id` and submitters:

- Single: one submitter with role `Client`
- Couple: two submitters — `Client` for primary, `Spouse` for partner

Each submitter object includes `email`, `name`, `role`, and optionally
`phone` (E.164 format).

**Never pass the `fields` array** — not even an empty `[]`. The MCP tool
treats any value in `fields` as a prefill, which locks that field as
readonly. The clients must fill their own signature, date, and any CST
checkbox at signing time. If a future workflow appears to require
prefilling a field, stop and ask Scott — do not add a `fields` array
without him changing this rule.

Return to Scott:
- DocuSeal template name and ID
- Submitter list with status
- The OneDrive file path of the saved .docx
- A reminder to move the matter stage in Lawmatics if applicable (this skill
  does NOT change Lawmatics stages; suggest `change-matter-stage` if needed)

## Legal compliance guardrails

- Cite specific document sections from the rendered .docx if Scott asks
  about content; do not summarize from memory.
- Flag any uncertainty about plan-name normalization, fee amounts, or
  whether CST is applicable, rather than guessing. Ask Scott.
- The engagement agreement is a contract — output requires Scott's explicit
  review before sending. The skill must never send without confirmation.
- Preserve all original template language; only fill placeholders. Do not
  rewrite, summarize, or modify any clause text.
- Final disclaimer to Scott: "This is a template-generated draft. You are
  responsible for reviewing the entire document before sending for
  signature. The skill does not validate fee amounts, plan eligibility, or
  the suitability of the chosen plan type."

## Learnings

Check `learnings.md` at session start; apply any rules. After completion,
ask Scott: "Anything to log for next time?" — append useful items.

## Firm context

This skill reads `firm-context.md` in the working directory for:

- Firm name, contact info, MA jurisdiction
- Document standards (Garamond 12pt, Navy/Teal, TR-prefixed styles)
- `docuseal_api_token` — DocuSeal API token used by
  `scripts/docuseal_upload.py` for direct REST uploads. Get this from
  https://docuseal.com/settings/api. Keep it out of any committed repo.
- `flat_fee_default` — optional default fee if Scott wants a starting point

If `docuseal_api_token` is missing or still a placeholder, the skill skips
the REST upload and goes straight to the manual fallback (4b). Prompt
Scott to set the token rather than silently degrading.
