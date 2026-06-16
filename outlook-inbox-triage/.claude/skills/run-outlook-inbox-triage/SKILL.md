---
name: run-outlook-inbox-triage
description: >
  Build, run, smoke-test, and verify the outlook-inbox-triage skill's CLI
  (scripts/graph_triage.py) without touching the live mailbox or database. Use
  when asked to run, launch, test, smoke-test, drive, debug, or verify the inbox
  triage tool, its auth/fetch/identify/apply/move/draft flow, the Supabase
  client/lead sender lookup, or a change to graph_triage.py. Drives the real CLI
  against a local mock Microsoft Graph + Supabase server via
  .claude/skills/run-outlook-inbox-triage/driver.py.
---

# Run / drive the outlook-inbox-triage CLI

The "app" here is a CLI: `scripts/graph_triage.py`, whose only real work is
Microsoft Graph I/O (auth, fetch unread mail, apply categories, move
Notification mail, create draft replies) and a Supabase lookup (`identify` —
classify each sender as client/lead/unknown via the `triage_match_sender` RPC).
Driving it for real would label, move, and draft in Scott's **live law-firm
mailbox**. So the agent path drives the *real CLI* against a **local mock that
serves both Graph and Supabase** — every code path runs, nothing reaches
Microsoft or the firm database.

The harness is `.claude/skills/run-outlook-inbox-triage/driver.py`. It starts
the mock, points the CLI at it with `GRAPH_BASE` / `GRAPH_TOKEN_URL` (and a mock
`supabase_url` in the temp context file), runs the full flow as real
subprocesses, and asserts on what the CLI sent over the wire.

All paths below are relative to the unit dir (the one holding `scripts/` and
`triage-context.md`): `skills/outlook-inbox-triage/`.

## Prerequisites

Python 3 and `requests`. On this Mac mini both are already present (verified
Python 3.14.5, requests 2.34.2). If `requests` is missing:

```bash
python3 -m pip install requests
```

No `apt-get`, no display, no network — the mock server is in-process.

## Run (agent path) — the driver

From the unit dir:

```bash
python3 .claude/skills/run-outlook-inbox-triage/driver.py
```

Expected tail:

```
ALL CHECKS PASSED (25 assertions)
```

Exit 0 = the CLI authenticates, fetches, writes `triage-run/messages.json`,
runs `identify` (one Supabase RPC per unique sender → `identified.json` tagging
client/lead/unknown), creates 7 master categories (incl. `triage_draft`,
`client`, `lead`), creates the Notifications folder, **labels** mail with the
triage category **plus a `client`/`lead` identity tag** for known senders,
**moves** the Notification message to the folder (not labelled), creates a
threaded reply draft with newlines converted to `<br>` and tags **both** the
draft (`["triage_draft","client"]`) and the inbox message
(`["Client-Urgent","triage_draft","client"]`), and honours `--no-drafts`. The
driver prints each subprocess invocation and a PASS/FAIL line per assertion; any
non-zero exit names the failing check.

The driver works in a fresh temp dir, so it leaves the unit dir clean (no
`triage-run/` artifacts).

### What the driver covers

The mock records every HTTP call the CLI makes, so the assertions check the
real wire behavior — the layer any change to `graph_triage.py` touches:

- `fetch` sends `$filter=isRead eq false` + `receivedDateTime DESC`
- `identify` POSTs `/rest/v1/rpc/triage_match_sender` once per unique sender and
  writes `identified.json` with the right `kind` (client/lead/unknown) + name
- `apply` PATCHes the triage category **plus a `client`/`lead` identity tag** for
  known senders (e.g. `["Client-Urgent","lead"]`); unknown senders stay single
- `apply` POSTs `/move` (not a category PATCH) for `Notification` items
- `draft` POSTs `/createReply`, PATCHes the draft **body**, then in a
  **separate** PATCH sets the draft's `["triage_draft", <identity>]`, then
  GETs the draft back to verify the tag stuck; finally PATCHes the **inbox
  message** to `["Client-Urgent","triage_draft", <identity>]`
- the mock is **stateful** for categories (PATCH stores, GET returns), so the
  CLI's read-back verification runs against realistic state
- `--no-drafts` creates no new draft

To exercise a new subcommand or a different classification mix, edit
`FAKE_MESSAGES` / `FAKE_CONTACTS` / the `classified` list in `driver.py` and add
a `check(...)`.

## Direct invocation (one subcommand, real Graph host)

To run a single subcommand against the real mailbox (needs a populated
`triage-context.md` with valid Entra creds — see `references/graph-setup.md`):

```bash
python3 scripts/graph_triage.py auth-check
```

`auth-check` is read-only (prints the mailbox display name). `ensure-*`,
`apply`, `move`, and `draft` mutate the live mailbox — do not run them as a
test. Verified error paths (no live creds needed):

```bash
# missing context file -> clean error, exit 1
cd "$(mktemp -d)" && python3 .../scripts/graph_triage.py auth-check
#   ERROR: triage-context.md not found. Create it from ...

# bad creds -> surfaces the AADSTS error, never the secret, exit 1
#   ERROR: token request failed (400): {"error":"invalid_request",
#   "error_description":"AADSTS900021: Requested tenant identifier ... not valid ...
```

### `identify` against real Supabase (read-only, safe)

`identify` only *reads* the firm DB via the `triage_match_sender` RPC, so it is
safe to run live. Verified this session with safe (`@example.invalid`) senders —
no Graph creds needed, just `supabase_url` + the **publishable** key:

```bash
W="$(mktemp -d)" && cd "$W" && mkdir triage-run
printf 'supabase_url: https://wxjwpoiesylggjgoixjz.supabase.co\nsupabase_key: sb_publishable_YOUR_KEY_HERE\n' > triage-context.md
printf '[{"id":"m1","subject":"hi","from":{"emailAddress":{"address":"nobody@example.invalid"}}}]\n' > triage-run/messages.json
python3 /path/to/scripts/graph_triage.py identify
#   Identified 1 sender(s): 0 client, 0 lead, 1 unknown -> triage-run/identified.json
```

The RPC itself is verified directly with `curl` (HTTP 200, `[]` = unknown) — see
`references/supabase-setup.md`.

## Run (human path)

There is no GUI and no long-running server. A human runs the same subcommands
by hand in order: `auth-check` → `ensure-categories` → `ensure-folder` →
`fetch --count N` → `identify` → (classify) → `apply --input <file>` →
`draft ...`. Useless to "just launch" — each subcommand does one operation and
exits.

## Gotchas

- **Never smoke-test against real Graph.** `apply`/`move`/`draft` write to a
  live mailbox (categories, moved mail, drafts). The driver exists precisely so
  you don't. Only `auth-check` is safe to run live.
- **The CLI hardcodes the Graph + login hosts**; the driver redirects them with
  `GRAPH_BASE` and `GRAPH_TOKEN_URL` env vars (added to `graph_triage.py` for
  exactly this). Without those env vars the CLI hits `graph.microsoft.com` /
  `login.microsoftonline.com` for real.
- **`timeout` is not installed on this macOS host.** Don't wrap commands in
  `timeout 8 ...` — it fails with `command not found`. The CLI's own 30s
  `requests` timeouts are the safety net.
- **Classification is the agent's job, not the CLI's.** `graph_triage.py` never
  classifies — Claude writes `classified.json`; the CLI only acts on it. The
  driver simulates that step inline.
- **Notification = move, not label.** A `Notification` item produces a `/move`
  call and **no** category PATCH. If you assert "every message got a category,"
  you'll wrongly fail the moved one.
- **`triage_draft` lands on BOTH the draft and the inbox message.** `draft`
  PATCHes `draft_id` (the reply in the Drafts folder) → `["triage_draft",
  <identity>]`, then PATCHes the original inbox message →
  `["Client-Urgent","triage_draft", <identity>]`. Assert on the right target.
- **Body and categories on a draft go in SEPARATE PATCHes, body first.** A
  combined `{"body":…, "categories":…}` PATCH on a `createReply` draft applies
  the body but can silently drop the categories — that was the real bug behind
  "triage_draft isn't on my drafts." `set_categories_verified()` sets categories
  on their own PATCH (after the body) and then **GETs them back**; it WARNs if
  the tag didn't stick. The mock stores PATCHed categories so the read-back
  passes; against real Graph that read-back is what tells you it worked.
- **Categories stack on purpose, recomputed and replaced each run.** `apply`
  writes `[triage_cat]` + `client`/`lead`; the draft step writes `triage_draft` +
  identity on the draft and `Client-Urgent` + `triage_draft` + identity on the
  original. Arrays are replaced, never appended, so re-runs don't grow them —
  don't "fix" them back to single-element.
- **Identity tags come from `identified.json`, not `classified.json`.** `apply`
  and `draft` both call `load_identity()` to read it. If you run `apply` without
  a prior `identify`, messages get the triage category with **no** client/lead
  tag — that's the graceful fallback, not a failure.
- **`identify` needs `triage-run/messages.json` to exist** — it reads, not
  fetches. Run `fetch` first (the driver does). Standalone, write a
  `messages.json` by hand (see the real-Supabase snippet above).
- **RLS forces the RPC, not table reads.** `leads`/`client_intake` have RLS on,
  so a publishable key reading them directly returns `[]`. The CLI calls the
  `SECURITY DEFINER` RPC instead — that's why the design uses an RPC and a
  publishable key, **never** a service-role secret in `triage-context.md`.
- **Supabase mock shares the host with Graph.** The driver routes Graph under
  `/v1.0/...` and Supabase under `/rest/v1/rpc/...` on one server; the CLI's
  `supabase_url` is the bare mock base, `GRAPH_BASE` is `<base>/v1.0`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: requests` | `python3 -m pip install requests` |
| `FAIL: CLI not found at .../scripts/graph_triage.py` | Run the driver from the unit dir; it locates the CLI via `parents[3]`. |
| Driver hangs | A `do_*` handler returned 404 for an unhandled path — check the last `$ graph_triage.py ...` line printed and add that route to the mock. |
| Live `auth-check` → `token request failed (400) AADSTS900021` | Placeholder/empty tenant in `triage-context.md`; fill in real Entra creds per `references/graph-setup.md`. |
| Live `auth-check` → 403 | Admin consent / permission grant didn't take (`Mail.ReadWrite`, `MailboxSettings.ReadWrite`). |
| `identify` → `supabase_url and supabase_key are required` | Add both to `triage-context.md` (publishable key — see `references/supabase-setup.md`). |
| Live `identify` returns everyone `unknown` | RPC missing (HTTP 404) or wrong key (401); re-check with the `curl` in `references/supabase-setup.md`. Note matches are also case-folded and cover spouse emails. |
| `identify` → `messages.json not found. Run fetch first.` | `identify` reads `triage-run/messages.json`; run `fetch` (or hand-write one). |
| Live run: `WARN: draft categories did not stick` | Real Graph dropped the tag. Confirm `ensure-categories` created `triage_draft` (it must exist in the mailbox master list), and that body/categories are set in separate PATCHes (they are now). The WARN prints the categories Graph actually returned. |
| `triage_draft` not visible on a draft in Outlook | Outlook's Drafts list may hide the Categories column — add it, or open the draft. The CLI's read-back WARN is the source of truth for whether the tag is actually set. |
