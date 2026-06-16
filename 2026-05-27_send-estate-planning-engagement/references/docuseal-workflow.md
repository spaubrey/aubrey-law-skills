# DocuSeal Upload & Send Workflow

## Goal

Take the rendered .docx (saved to the lead's OneDrive folder), get it into
DocuSeal as a new per-client template, validate the detected fields, and
send for signature. Each phase has explicit checkpoints — the skill never
silently advances past a failure.

## Pre-check — duplicate template guard

Before creating anything, call `DocuSeal:search_templates` with the
proposed name (`Engagement Agreement — LastName — YYYY-MM-DD`).

```
q: "Engagement Agreement — Smith — 2026-05-22"
limit: 10
```

Inspect the returned list for an exact-name match (case-sensitive). If
found:

```
Existing template found:
  #3789012  "Engagement Agreement — Smith — 2026-05-22"  created 2026-05-22T14:03:00Z

Options:
  reuse    — skip create; load the existing template_id and send against
             it (only safe if the .docx content is unchanged)
  v2       — create a new template with name suffixed " — v2" (then v3, ...)
  abort    — stop the skill; Scott handles manually
```

Never silently create a duplicate. Default to `v2` only if Scott picks
neither `reuse` nor `abort`.

If no exact-name match, proceed to create.

## Primary path — direct REST API upload

The skill uses `scripts/docuseal_upload.py` to POST the .docx file
directly to DocuSeal's `POST /templates/docx` endpoint. The MCP
`create_template` tool only accepts a public URL for the file, so this
script bypasses that constraint by sending the file as base64-encoded
JSON via DocuSeal's native API.

### Prerequisites

- `firm-context.md` contains a valid `docuseal_api_token` (not a
  placeholder). Get it from https://docuseal.com/settings/api.
- The .docx has been saved to its final lead-folder location (per
  `references/lead-folder.md`).

### Steps

1. **Run the upload script:**

   ```bash
   python3 scripts/docuseal_upload.py \
     --file "/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning/2026-EP-Smith, John & Jane/Engagement Agreement - Smith - 2026-05-22.docx" \
     --name "Engagement Agreement — Smith — 2026-05-22" \
     --token-from-context firm-context.md \
     --out-json /tmp/docuseal_upload_result.json
   ```

   On success, the script writes (and prints) JSON like:

   ```json
   {
     "ok": true,
     "template_id": 3789044,
     "template_name": "Engagement Agreement — Smith — 2026-05-22",
     "roles": ["Client", "Spouse"],
     "fields": [
       {"name": "Client Signature", "type": "signature", "role": "Client", "required": true},
       {"name": "Client Date",      "type": "date",      "role": "Client", "required": true},
       {"name": "Spouse Signature", "type": "signature", "role": "Spouse", "required": true},
       {"name": "Spouse Date",      "type": "date",      "role": "Spouse", "required": true}
     ],
     "edit_url": "https://docuseal.com/templates/3789044/edit"
   }
   ```

   Capture `template_id` for the rest of the flow.

2. **On script failure**, the script exits non-zero and writes an error
   JSON like:

   ```json
   {
     "ok": false,
     "error": "HTTP 401: invalid token",
     "status": 401
   }
   ```

   - Surface the exact error to Scott, including HTTP status if present.
   - Offer the manual fallback below. Do NOT retry the REST call without
     Scott's go-ahead (a 401 means the token is wrong, retrying won't
     help; a 5xx may be worth one retry; a network error is the only
     thing where auto-retry is safe and the script does not auto-retry).

### Token security

- The token sits in `firm-context.md` on Scott's Mac. Don't commit that
  file to any repo or share it publicly.
- The script reads the token from either `DOCUSEAL_API_TOKEN` env var
  (priority) or `firm-context.md`. Env var is useful for one-off testing.
- The token is never written to the output JSON or printed by the script.
- If the token is compromised, rotate it at
  https://docuseal.com/settings/api (revoke + generate new).

## Fallback path — manual upload

Only used when the REST upload fails (bad token, network outage, DocuSeal
API down) or when no token is configured.

1. Call `DocuSeal:create_template` with `name` only (no `url`). The
   response includes an `edit_url`.
2. Output to Scott:

   ```
   Manual upload required (REST API path unavailable).
   Local file:       /Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/...
   DocuSeal editor:  <edit_url>

   Drag the .docx into the editor. The fields {{Client Signature}},
   {{Client Date}} (and spouse equivalents) should auto-detect on upload.
   Reply "uploaded" when done.
   ```

3. Wait for Scott's explicit "uploaded" reply. Then continue to
   validation.

## Validate the created template

Always call `DocuSeal:load_template` with the returned `template_id` —
do not skip this step, even when the upload script already returned the
field list. Treat the upload-script summary as informational; treat
`load_template` as authoritative.

Check explicitly. A successful 200 response is not enough; inspect the
fields/roles in the response body:

| Scenario | Expected roles | Expected field types per role |
| --- | --- | --- |
| Single client | `Client` only | one `signature`, one `date` |
| Couple | `Client` AND `Spouse` | one `signature`, one `date` each |
| `credit_shelter=true` | (above) + `checkbox` on `Client` | as above plus one `checkbox` |

If anything is off, name the specific gap rather than logging a generic
"validation failed":

- "expected `Spouse` role, got only `Client`"
- "no `signature` field detected on `Client`"
- "expected `checkbox` field for CST election on `Client`, none found"

When validation fails:

1. Surface the specific gap to Scott.
2. If the primary REST upload was used, the .docx is already in DocuSeal —
   offer to delete that template (via the DocuSeal UI, no MCP delete tool)
   and re-run after Scott fixes the underlying issue (often a render-script
   bug or an outdated source template).
3. If the manual path was used, offer to reopen the editor URL so Scott
   can fix the field placement.
4. Do NOT call `send_documents` against a half-detected template — it
   will either error on a missing role, or worse, send with the wrong
   signing flow.

## Sending for signature

After validation passes, present a send summary in this exact form:

```
About to send for signature:
  Template:           Engagement Agreement — Smith — 2026-05-22 (#3789044)
  Submitters:
    Client:  John Smith <john@example.com>[, +15551234567]
    Spouse:  Jane Smith <jane@example.com>[, +15551234568]
  Fields prefilled:   NONE

Confirm? (yes / no / edit emails)
```

Only on explicit "yes", call `DocuSeal:send_documents`:

```json
{
  "template_id": 3789044,
  "submitters": [
    {
      "role": "Client",
      "name": "John Smith",
      "email": "john@example.com"
    },
    {
      "role": "Spouse",
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ]
}
```

Return the response to Scott — it includes the signing URLs per submitter,
which Scott may want to forward directly if the auto-send email fails.

If Scott says "edit emails," correct in-conversation and re-show the
summary before sending. If Scott says "no," stop — leave the template in
DocuSeal for later use, and report the template_id so Scott can resume
manually.

## Important notes

- **Never pass the `fields` array on `send_documents`.** The MCP tool
  treats any value in `fields` (even an empty list, in some clients) as a
  prefill. Prefilled fields are locked readonly, which defeats the entire
  signing workflow. The render step already embeds the field markers in
  the .docx so DocuSeal auto-detects them; signers fill them at signing
  time.

- **One template per client.** Do not reuse the master template — each
  client gets a unique per-client template because the document content
  (names, fees, plan type, CST) varies. This matches Scott's existing
  pattern. The pre-check above guards against accidental same-day
  duplicates for the *same* client.

- **Signature field markers.** DocuSeal recognizes `{{Field Name;type=...;
  role=...}}` syntax in uploaded DOCX files. The render script ensures
  these are literal text in the output (wrapped in Jinja2 `{% raw %}`
  blocks during render). Confirmed working with .docx uploads via both
  URL and direct base64 POST.

- **Role names must match exactly.** When sending, the `role` value in
  each submitter object must exactly match a role defined in the template.
  The template defines `Client` and `Spouse`. Case-sensitive. The
  validation step above catches mismatches before they reach
  `send_documents`.

- **Phone numbers are optional.** If passed in E.164 format
  (`+15551234567`), DocuSeal sends SMS reminders. If omitted, only email
  notifications go out.

- **DocuSeal converts the DOCX to a PDF** on upload. The original .docx
  stays in Scott's OneDrive lead folder as the authoritative editable
  copy.
