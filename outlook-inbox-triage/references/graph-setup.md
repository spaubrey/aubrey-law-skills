# Microsoft Graph setup — one-time

This skill writes to Outlook (categories + drafts), so it needs an Entra
(Azure AD) app registration with mail write permission. Do this once.

## 1. Register the app

1. Entra admin center → **App registrations** → **New registration**.
2. Name it e.g. "Aubrey Law — Inbox Triage". Single tenant is fine.
3. Copy the **Application (client) ID** and **Directory (tenant) ID** into
   `triage-context.md`.

## 2. Add a client secret

1. App → **Certificates & secrets** → **New client secret**.
2. Copy the secret **value** (not the ID) into `triage-context.md` as
   `client_secret`. You won't be able to see it again after you leave the page.

## 3. Grant permissions

Choose ONE model:

### Application permissions (recommended for unattended Cowork runs)
- API permissions → **Microsoft Graph** → **Application permissions**:
  - `Mail.ReadWrite`
  - `MailboxSettings.ReadWrite`  (needed to create master categories)
- Click **Grant admin consent**.
- Set `user_id` in `triage-context.md` to the mailbox to act on.
- Note: application Mail.ReadWrite grants access to *all* mailboxes in the
  tenant unless you scope it with an Application Access Policy in Exchange.
  For a solo firm that's fine; if you ever add staff, scope it.

### Delegated permissions (acts as the signed-in user)
- Use `Mail.ReadWrite` + `MailboxSettings.ReadWrite` delegated, with an
  interactive/device-code token flow. The bundled script uses the
  client-credentials (application) flow, so if you prefer delegated you'll
  need to adjust `get_token()` to a delegated flow. Application is simpler.

## 4. Verify

From the skill's working directory:

```bash
python scripts/graph_triage.py auth-check
```

You should see the mailbox display name and address. If you get a 403, the
permission grant or admin consent didn't take; re-check step 3.

## Permissions rationale

- `Mail.ReadWrite` — read unread Inbox messages, PATCH `categories`,
  `createReply` drafts, create the **Notifications** mail folder, and **move**
  notification-type messages into it. (Folder create + message move are both
  covered by `Mail.ReadWrite` — no extra permission needed.)
- `MailboxSettings.ReadWrite` — create the master categories if missing
  (Client-Urgent, Internal-Task, FYI-Read, Archive, triage_draft).

The skill never requests `Mail.Send`, so it structurally cannot send mail —
drafts only.
