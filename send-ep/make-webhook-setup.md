# Make.com SharePoint Share-Link Webhook — One-Time Setup

> **DEPRECATED — kept for reference only.**
>
> As of 2026-05-22, the send-estate-planning-engagement skill uploads
> directly to DocuSeal via its REST API (see
> `scripts/docuseal_upload.py` and the "Primary path" section of
> `docuseal-workflow.md`). The Make.com SharePoint share-link approach
> is no longer part of the active flow.
>
> These notes remain in case Scott ever wants to revive the route — for
> example, if DocuSeal's API access is unavailable and a SharePoint
> share link is the only way to get a file URL.

This scenario lets the skill convert a local OneDrive file path into a
DocuSeal-fetchable HTTPS URL without needing Graph API tokens in the skill.

## Scenario design

**Trigger:** Custom Webhook
- Method: `POST`
- Body: JSON with `file_path`, `share_type` (default `view`),
  `share_scope` (default `anonymous`)

**Module 1 — Microsoft 365 OneDrive: "Search for files/folders"**
- Search by file path. Input: `{{1.file_path}}` (mapped from webhook body)
- Important: Make's OneDrive module expects SharePoint-relative paths, not
  the local sync path. Translate by:
  1. Strip the prefix
     `/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/`
  2. Use the remaining path
     (e.g., `Aubrey Law Clients/Estate Planning/2026-EP/.../file.docx`)

**Module 2 — Microsoft 365 OneDrive: "Make an HTTP request"** (Graph API)
- Method: `POST`
- URL: `https://graph.microsoft.com/v1.0/me/drive/items/{{1.fileId}}/createLink`
- Body:
  ```json
  {
    "type": "{{1.share_type}}",
    "scope": "{{1.share_scope}}"
  }
  ```
- This returns `{ link: { webUrl: "..." } }`.

**Module 3 — Tools: Set variable**
- Name: `direct_download_url`
- Value: `{{2.link.webUrl}}?download=1`
  - SharePoint's anonymous share URLs are previewer URLs by default. The
    `?download=1` (also accepts `?download=true`) parameter forces a direct
    file response, which is what DocuSeal needs.

**Module 4 — Webhook response**
- Status: `200`
- Body:
  ```json
  {
    "share_url": "{{3.direct_download_url}}",
    "expires_at": "{{2.link.expirationDateTime}}"
  }
  ```

## Save the webhook URL

After saving the scenario in Make, copy the trigger webhook URL and add it
to `firm-context.md`:

```yaml
make_share_link_webhook: https://hook.us2.make.com/abc123xyz...
```

## Testing the scenario

Test from a terminal:

```bash
curl -X POST <webhook-url> \
  -H 'Content-Type: application/json' \
  -d '{"file_path":"/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning/test.docx","share_type":"view","share_scope":"anonymous"}'
```

Expected: 200 with `share_url` and `expires_at`. Open the URL in a browser
— it should download the file directly (no SharePoint preview UI).

## Security considerations

- Anonymous links to engagement agreements with client names and fees are
  sensitive. Limit `expirationDateTime` to a short window (24 hours is
  enough — DocuSeal fetches immediately on `create_template`).
- Set the scenario's webhook to require a secret in the request body or
  header. The skill should send this secret from `firm-context.md`.
- After successful DocuSeal upload, optionally call a second Make endpoint
  to revoke the share link. (Optional polish — DocuSeal has already
  fetched the file by then.)

## Fallback if Make is unavailable

The skill's primary path tolerates this: if the webhook returns non-200 or
times out, the skill falls back to manual DocuSeal upload (Scott drags the
.docx into the DocuSeal editor URL).
