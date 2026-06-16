# SignWell Upload & Send Workflow

## Overview

SignWell uses a **single-call** model: upload the .docx (as base64 or URL),
define recipients and field positions, and send — all in one POST to
`/api/v1/documents`. There is no separate "create template then send" step
for per-client documents.

Authentication: `X-Api-Key: <api_key>` header. Key is stored in
`firm-context.md` as `signwell_api_key`.

Base URL: `https://www.signwell.com/api/v1`

---

## How fields work — Text Tags

SignWell detects field positions from **text tags** embedded in the .docx as
literal visible text. The render script writes these into the document in
white text (invisible to the client but parsed by SignWell on upload).

Text tag format:
```
[[type|signer_number|required|label]]
```

Examples used in the engagement template:

| Tag in docx | Meaning |
| --- | --- |
| `[[s\|1\|y\|Client Signature]]` | Signature, signer 1 (Client), required |
| `[[d\|1\|y\|Client Date]]` | Date, signer 1 (Client), required |
| `[[s\|2\|y\|Spouse Signature]]` | Signature, signer 2 (Spouse), required |
| `[[d\|2\|y\|Spouse Date]]` | Date, signer 2 (Spouse), required |
| `[[c\|1\|n\|CST Election]]` | Checkbox, signer 1 (Client), optional |

Signer numbers correspond to the **order of recipients** in the API request
(1 = first recipient = Client, 2 = second = Spouse).

Pass `text_tags: true` in the API request body to enable text tag parsing.

---

## API call — Create & Send Document

```
POST https://www.signwell.com/api/v1/documents
X-Api-Key: <signwell_api_key>
Content-Type: application/json
```

Body structure:

```json
{
  "test_mode": false,
  "name": "Engagement Agreement — Smith — 2026-05-19",
  "subject": "Your Aubrey Law Engagement Agreement",
  "message": "Please review and sign your estate planning engagement agreement at your earliest convenience. Let me know if you have any questions.",
  "text_tags": true,
  "reminders": true,
  "files": [
    {
      "file_url": "<anonymous SharePoint download URL>",
      "file_name": "Engagement Agreement - Smith - 2026-05-19.docx"
    }
  ],
  "recipients": [
    {
      "id": "client",
      "name": "John Smith",
      "email": "john@example.com",
      "placeholder_name": "Client"
    }
  ]
}
```

For couples, add a second recipient:
```json
{
  "id": "spouse",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "placeholder_name": "Spouse"
}
```

### File delivery options

**Option A — URL (preferred, same SharePoint share-link path as before):**
- Use the Make.com webhook to get an anonymous SharePoint download URL.
- Pass as `file_url` in the `files` array.
- The URL must be a direct download link (append `?download=1` if needed).

**Option B — base64 (fallback):**
- Read the .docx from the local OneDrive path.
- Base64-encode it.
- Pass as `file_base64` instead of `file_url` (not both).
- No Make.com webhook needed for the fallback — Claude reads the file
  directly via bash_tool and encodes it.

---

## API response (201 Created)

```json
{
  "id": "72f42382-9984-472e-af81-002b410ae85e",
  "status": "sent",
  "name": "Engagement Agreement — Smith — 2026-05-19",
  "recipients": [
    {
      "id": "client",
      "name": "John Smith",
      "email": "john@example.com",
      "status": "sent",
      "sign_url": "https://www.signwell.com/sign/abc123..."
    }
  ]
}
```

Return `id` (document ID) and `sign_url` per recipient to Scott.

---

## Fallback — base64 upload

If the Make.com share-link webhook is unavailable or fails:

1. Claude reads the .docx from the final OneDrive path using bash_tool:
   ```bash
   base64 -i "/Users/aubreylawmacmini/.../Engagement Agreement - Smith - 2026-05-19.docx"
   ```
2. Pass the base64 string as `file_base64` in the files array (omit `file_url`).
3. This eliminates the SharePoint sync wait and Make webhook dependency.
4. No manual upload step needed — the document goes directly to SignWell.

The base64 fallback is actually simpler than the DocuSeal fallback (no
editor URL, no waiting for Scott to drag-and-drop). Prefer it if the
webhook is slow or unavailable.

---

## Confirmation before sending

Before calling the API, show Scott:

```
About to send for signature via SignWell:
  Document: Engagement Agreement — Smith — 2026-05-19
  Signers:
    1. Client: John Smith <john@example.com>
    2. Spouse: Jane Smith <jane@example.com>  (if couple)
  Reminders: on (days 3, 6, 10)
  File source: SharePoint URL / base64 fallback

Confirm? (yes / no / edit)
```

Only on explicit "yes" — call the API.

---

## Important notes

- **No persistent templates.** Each engagement is a fresh document upload.
  SignWell does support reusable templates, but for per-client engagement
  agreements the content varies enough that one-time upload is correct.
- **Signer order matters.** Text tag signer numbers map to recipient order.
  Client is always signer 1; Spouse (if present) is signer 2.
- **No `apply_signing_order`.** Both parties can sign in any order (parallel
  signing). Set `apply_signing_order: false` (default).
- **Document ID for follow-up.** Save the returned `id` — it is needed to
  send manual reminders (`POST /api/v1/documents/{id}/remind`) or check
  status (`GET /api/v1/documents/{id}`).
- **Free tier.** Under 25 documents/month via API = $0. No seat fee required
  for API-only usage. Keep a running monthly count if volume approaches limit.
