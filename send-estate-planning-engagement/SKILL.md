---
name: send-estate-planning-engagement
description: >
  [OUTCOME]: Generates a fully populated Aubrey Law estate planning engagement
  agreement as a branded .docx, saves it to the lead's OneDrive folder
  (creating year/lead folders as needed), uploads it to SignWell via the API,
  and sends it for signature. Returns the SignWell document ID and signing URLs.
  [TRIGGER]: Activates when Scott says "send the engagement agreement to
  [client]", "send EP engagement to [client]", "engagement agreement for
  [client]", "send engagement for the [client] matter", "draft and send the
  engagement", "/send-estate-planning-engagement", or any request to send an
  estate planning engagement agreement to a new client or lead.
  [ANTI-TRIGGER]: Does NOT activate for trust drafting, will drafting, closing
  packages, deed drafting, intake questionnaires, the PMPS proposal flow,
  changing a matter stage, or sending payment links. Does NOT trigger for
  non-estate-planning engagement agreements (e.g., litigation matters).
---

# Send Estate Planning Engagement Agreement

## Purpose

Produce a customized Aubrey Law estate planning engagement agreement and send
it to the client(s) for signature via SignWell in one workflow. Save a Word
copy to the lead's OneDrive folder for the file.

## What this skill does, in order

1. Confirm firm context exists; if `firm-context.md` is missing in the working
   directory, create it from defaults below.
2. Gather per-matter inputs (see Step 1 below). Manual entry — do not assume
   from prior conversation unless Scott explicitly says "use the info above."
3. Select the correct template from `assets/` and render the engagement Word
   doc via `scripts/render_engagement.py`.
4. Ensure the lead's OneDrive folder exists (year folder + lead folder per
   naming convention below); save the rendered .docx there.
5. Upload the .docx to SignWell and send for signature in a single API call
   (see `signwell-workflow.md`). Primary path uses the SharePoint share-link;
   fallback reads the file directly as base64.
6. Return the SignWell document ID, signing URLs per recipient, and the
   OneDrive file path.

Each step requires explicit Scott confirmation before the next.

## Templates in `assets/`

| File | When to use |
| --- | --- |
| `Engagement_Agreement_C_Trust.docx` | Flat-fee, couple, trust plan |
| `Engagement_Agreement_C-LP_Trust.docx` | Legal plan, couple, trust plan |

Template selection is automatic via `scripts/render_engagement.py` based on
`legal_plan` and `plan_type` inputs. Will-only templates are not yet bundled
— flag to Scott and draft manually if needed.

**Placeholders in templates** (replaced at render time):
- `[Client Full Name]` → full client name
- `[Spouse Full Name]` → full spouse name (couple only)
- `[flat-fee]` → formatted fee, e.g. "$5,500" (flat-fee template only)
- `[Legal Plan]` → plan name, e.g. "MetLife" (LP template only)

**SignWell text tags** (already in templates — do not remove):
- `{{signature}}` — client signature (signer 1)
- `{{signature:2:n}}` — spouse signature (signer 2, couple template)
- `{{signature:1:n}}` — client initials for optional services election (LP template)
- `{{autofill_date_signed}}` — auto-filled date

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
| Flat fee amount (digits only, e.g. 5500) | text | if NOT legal plan |
| CST addendum? | bool | if legal plan + couple |

## Step 2 — Render the Word doc

Write inputs to `/tmp/inputs.json`, then call:

```bash
python3 scripts/render_engagement.py \
  --inputs /tmp/inputs.json \
  --out /tmp/engagement_render.docx
```

The script selects the correct template from `assets/` and replaces all
`[Placeholder]` text throughout the document.

Show Scott a short confirmation summary:
- Client(s) name and email(s)
- Plan type (trust vs. will)
- Fee structure (flat fee $X or legal insurance plan Y)
- CST addendum (if applicable)
- Deed clause (if applicable)

Ask: "Open the rendered doc and review before we proceed to upload?"
If Scott opens it and requests changes, correct inputs and re-render.

## Step 3 — Save to OneDrive lead folder

OneDrive root:
`/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning`

Lead folder naming (flat, directly under Estate Planning — no year subfolder):
- Flat fee: `YYYY-EP-LastName, FirstName & SpouseFirst`
  — e.g. `2026-EP-Doe, John & Jane`
- Legal plan: `YYYY-EP-LP-LastName, FirstName & SpouseFirst`
  — e.g. `2026-EP-LP-Smith, Sean & Sara`

File name: `Engagement Agreement - LastName - YYYY-MM-DD.docx`

Run `scripts/send_engagement.py prepare` to create the folder, save the
.docx collision-safely, and attempt the share-link webhook.

## Step 4 — Send via SignWell

See `signwell-workflow.md` for full details. Summary:

Run `scripts/send_engagement.py send` with `--plan /tmp/send_plan.json`
and `--api-key <signwell_api_key from firm-context.md>`.

**Primary path (SharePoint URL):**
- If prepare returned `share_link_ok: true`, pass `--plan` only.
- SignWell fetches the .docx, parses text tags, creates and sends.

**Fallback path (base64):**
- If `share_link_ok: false`, pass `--use-base64`.
- The script reads the .docx from OneDrive, base64-encodes, and POSTs directly.

Before running `send`, show Scott a confirmation summary:

```
About to send for signature via SignWell:
  Document: Engagement Agreement — Smith — 2026-05-19
  Signers:
    1. Client: John Smith <john@example.com>
    2. Spouse: Jane Smith <jane@example.com>  (if couple)
  Reminders: on (days 3, 6, 10)

Confirm? (yes / no / edit)
```

Only on explicit "yes" — run the send command.

## Step 5 — Return results

From the send result JSON, return to Scott:
- SignWell document ID
- Signing URL(s) per recipient (for reference if email doesn't arrive)
- OneDrive file path of the saved .docx
- Reminder to move the matter stage in Lawmatics if applicable (this skill
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
- `signwell_api_key` — SignWell API key for document sending
- `make_share_link_webhook` — URL for the Make.com SharePoint share-link
  scenario (optional; base64 fallback works without it)
- `flat_fee_default` — optional default fee if Scott wants a starting point

If any required firm-context field is missing, prompt Scott to add it
before proceeding.
