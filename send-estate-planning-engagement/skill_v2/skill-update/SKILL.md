---
name: send-estate-planning-engagement
description: >
  [OUTCOME]: Generates a fully populated Aubrey Law estate planning engagement
  agreement as a branded .docx, saves it to the Signwell Engagement Agreements
  folder, uploads it to SignWell via the API (base64), and sends it for
  signature. Returns the SignWell document ID and signing URLs.
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
copy to the Signwell Engagement Agreements folder.

## What this skill does, in order

1. Confirm firm context exists; if `firm-context.md` is missing in the working
   directory, use the copy bundled in this skill folder.
2. Gather per-matter inputs (see Step 1 below). Manual entry — do not assume
   from prior conversation unless Scott explicitly says "use the info above."
3. Select the correct template from `assets/` and render the engagement Word
   doc via `scripts/render_engagement.py`. Will Plan + legal plan matters use
   the LP trust template with Schedule A adjusted automatically (see below).
4. Save the rendered .docx to the save folder (see Step 3 below).
5. Upload the .docx to SignWell (base64) and send for signature in a single
   API call (see `signwell-workflow.md`).
6. Return the SignWell document ID, signing URLs per recipient, and the
   saved file path.

Each step requires explicit Scott confirmation before the next.

## Templates in `assets/`

| File | When to use |
| --- | --- |
| `Engagement_Agreement_C_Trust.docx` | Flat-fee, trust plan |
| `Engagement_Agreement_C-LP_Trust.docx` | Legal plan, trust plan OR will plan |

Template selection is automatic via `scripts/render_engagement.py` based on
`legal_plan` and `plan_type` inputs. Will-only flat-fee (non-legal-plan)
templates are not yet bundled — flag to Scott and draft manually if needed.

**Will Plan + legal plan** (`plan_type: "will"`, `legal_plan: true`) renders
from the LP trust template with these automatic Schedule A edits:
- "Revocable Trust" and "Deed" removed from the covered-documents bullets
- "Revocable Trust" added to the not-covered bullets
- "Credit Shelter Planning" and "Deed Recording" rows removed from the
  Optional Services table

**Individual (non-couple) clients** render from the couple template with
automatic edits: spouse placeholders and signer-2 signature blocks removed,
and the Joint Representation section deleted. Always tell Scott an
individual render was adapted from the couple template so he reviews it
with extra care.

**Placeholders in templates** (replaced at render time):
- `[Client Full Name]` → full client name
- `[Spouse Full Name]` → full spouse name (couple only)
- `[flat-fee]` → formatted fee, e.g. "$5,500" (flat-fee template only)
- `[Legal Plan]` → plan name, e.g. "MetLife" (LP template only)

**SignWell text tags** (already in templates — do not remove):
- `{{signature:1:y}}` — client signature (signer 1, required)
- `{{signature:2:y}}` — spouse signature (signer 2, required; couple only)
- `{{c:1:n}}` — client checkboxes for optional services election (LP template)
- `{{signature:1:n}}` / `{{signature:2:n}}` — optional-services signatures
- `{{autofill_date_signed}}` — auto-filled date

## Step 1 — Gather inputs

Ask for these fields. Use the AskUserQuestion tool for choices.
Do NOT proceed until all required fields are answered.

| Field | Type | Required when |
| --- | --- | --- |
| Client name (first, last) | text | always |
| Client email | text | always |
| Spouse name (first, last) | text | if couple |
| Spouse email | text | if couple |
| Will Plan or Trust Plan? | choice | always |
| Legal insurance plan? | bool | always |
| Plan name (ARAG / MetLife / Hyatt / LegalShield / LegalEASE / Other) | choice | if legal plan |
| Flat fee amount (digits only, e.g. 5500) | text | if NOT legal plan |

If client and spouse info arrive together (e.g., as command arguments), treat
that as provided — only ask for the fields still missing.

## Step 2 — Render the Word doc

Write inputs to an `inputs.json` in the working directory, then call:

```bash
python3 scripts/render_engagement.py \
  --inputs inputs.json \
  --out engagement_render.docx
```

The script selects the correct template from `assets/`, replaces all
`[Placeholder]` text, and applies will-plan / individual-client structural
edits as needed.

Show Scott a short confirmation summary:
- Client(s) name and email(s)
- Plan type (trust vs. will)
- Fee structure (flat fee $X or legal insurance plan Y)
- Any structural edits applied (will-plan Schedule A, individual adaptation)

Ask: "Open the rendered doc and review before we proceed to upload?"
If Scott opens it and requests changes, correct inputs and re-render.

## Step 3 — Save to the engagement agreements folder

Save location (host path):
`/Users/aubreylawmacmini/Desktop/Claude Cowork Mini/Signwell Engagement Agreements`

In a Cowork sandbox this folder must be connected/mounted; pass its mounted
path to the script with `--save-root`. If the folder is not connected, ask
Scott to connect it (request_cowork_directory) before saving.

Files save flat into this folder (no year/lead subfolders).
File name: `Engagement Agreement - LastName - YYYY-MM-DD.docx`
(collision-safe: `-2`, `-3`, ... appended if the name exists).

Run `python3 send_engagement.py prepare --rendered <docx> --inputs
<inputs.json> --save-root "<mounted folder path>" --out-json send_plan.json`.

## Step 4 — Send via SignWell

See `signwell-workflow.md` for full details. Summary:

Run `python3 send_engagement.py send --plan send_plan.json
--api-key <signwell_api_key from firm-context.md> --use-base64
--out-json send_result.json`.

Base64 upload is the standard path: the script reads the saved .docx,
base64-encodes it, and POSTs directly to SignWell. (A SharePoint share-link
webhook path still exists for legacy use but is not required.)

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
- Saved file path
- Reminder to move the matter stage in Lawmatics if applicable (this skill
  does NOT change Lawmatics stages; suggest `change-matter-stage` if needed)

## Legal compliance guardrails

- Cite specific document sections from the rendered .docx if Scott asks
  about content; do not summarize from memory.
- Flag any uncertainty about plan-name normalization, fee amounts, or
  template fit, rather than guessing. Ask Scott.
- The engagement agreement is a contract — output requires Scott's explicit
  review before sending. The skill must never send without confirmation.
- Preserve all original template language; only fill placeholders and apply
  the defined structural edits (will-plan Schedule A, individual
  adaptation). Do not rewrite, summarize, or modify any clause text.
- Individual-client renders are adapted from the couple template — always
  flag this for Scott's careful review.
- Final disclaimer to Scott: "This is a template-generated draft. You are
  responsible for reviewing the entire document before sending for
  signature. The skill does not validate fee amounts, plan eligibility, or
  the suitability of the chosen plan type."

## Learnings

Check `learnings.md` at session start; apply any rules. After completion,
ask Scott: "Anything to log for next time?" — append useful items.

## Firm context

This skill reads `firm-context.md` (working directory first, then the copy
bundled in this skill folder) for:

- Firm name, contact info, MA jurisdiction
- Document standards (Garamond 12pt, Navy/Teal, TR-prefixed styles)
- `signwell_api_key` — SignWell API key for document sending
- Save folder path for engagement agreements

If any required firm-context field is missing, prompt Scott to add it
before proceeding.
