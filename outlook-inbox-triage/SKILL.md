---
name: outlook-inbox-triage
description: >
  Runs Scott's Email Triage SOP on the most recent unread messages in his
  Outlook inbox. Reads the last N unread messages via Microsoft Graph,
  classifies each into one of five buckets (Client-Urgent, Internal-Task,
  FYI-Read, Archive, Notification), applies the matching Outlook category to
  each message — except Notification-type mail, which is MOVED to a
  "Notifications" folder — produces a bulleted summary table of the
  Client-Urgent items, and creates initial draft replies for the Client-Urgent
  items in the Drafts folder, tagging each drafted message with a triage_draft
  category. Identifies each sender against the firm's Supabase database
  (known client vs lead vs unknown) to make the urgent/lead classification
  data-driven rather than guessed.
  Triggers: "run my email triage", "triage my inbox", "run the triage SOP",
  "triage the last 50 unread", "sort my unread emails", "categorize my inbox",
  "do inbox triage for me", "/outlook-inbox-triage", or any request to
  classify, sort, summarize, or draft replies for unread Outlook mail.
  Use whenever Scott wants his unread inbox sorted into categories and/or
  Client-Urgent drafts prepared, even if he doesn't name the SOP.
  Does NOT trigger for sending email, calendar scheduling, OneDrive/document
  drafting, engagement agreements, billing, or any non-inbox workflow.
compatibility: >
  Requires Cowork on the Mac mini with a Microsoft 365 / Entra app
  registration that has Mail.ReadWrite and MailboxSettings.ReadWrite
  application (or delegated) permission. Uses direct Microsoft Graph REST
  calls — no ms365 connector write access needed. Sender identification
  additionally needs a Supabase project URL + publishable key in
  triage-context.md and the triage_match_sender RPC (see
  references/supabase-setup.md).
---

# Outlook Inbox Triage

## Purpose

Act as Scott's executive assistant for inbox triage. Given the last N unread
messages in his main Inbox, classify each one, label it in Outlook, summarize
the urgent ones, and pre-draft replies to the urgent ones — so Scott opens
Outlook to a sorted inbox and ready-to-review drafts instead of a wall of
unread mail.

All write actions (apply category, create draft) run through direct Microsoft
Graph API calls. Reads run through Graph too, so the whole flow lives in one
script and one auth path.

## Before you start

1. Confirm `triage-context.md` exists in the working directory. It holds the
   Graph credentials and Scott's standing preferences (calendar link, signoff,
   default message count). If it's missing, create it from
   `references/triage-context.example.md` and prompt Scott to fill in the
   secrets. **Never** print the client secret back to the chat.
2. Confirm the message count. If Scott named a number ("last 50"), use it.
   Otherwise use `default_count` from `triage-context.md` (50 if unset).

## What this skill does, in order

1. **Authenticate** to Microsoft Graph (`scripts/graph_triage.py auth-check`).
2. **Ensure categories exist.** Verify the seven Outlook categories
   (Client-Urgent, Internal-Task, FYI-Read, Archive, triage_draft, client,
   lead) exist on the mailbox; create any that are missing with their assigned
   colors (`scripts/graph_triage.py ensure-categories`). See the color map
   below.
3. **Ensure the Notifications folder exists** for notification-type mail
   (`scripts/graph_triage.py ensure-folder`). Creates a top-level
   "Notifications" mail folder if it isn't already there.
4. **Fetch** the last N unread messages from the Inbox, newest first
   (`scripts/graph_triage.py fetch --count N`). This writes the raw messages
   to `triage-run/messages.json`.
5. **Identify senders** against Supabase (`scripts/graph_triage.py identify`).
   Looks up each sender's email via the `triage_match_sender` RPC and writes
   `triage-run/identified.json` — one row per message tagging the sender as
   `client`, `lead`, or `unknown` (with display name + status). One Supabase
   call per unique sender; a failed lookup degrades to `unknown` rather than
   aborting the run.
6. **Classify** each message into exactly one bucket using the rules in
   the **Classification rules** section, **reading `identified.json` as a
   primary signal** (a known lead or a known client with a question is
   Client-Urgent — see the rules). Write the decisions (message id, sender,
   subject, category, one-line rationale) to `triage-run/classified.json`.
7. **Apply the triage decisions** (`scripts/graph_triage.py apply --input
   triage-run/classified.json`). For ordinary categories this is one Graph
   PATCH per message setting its `categories` array — and `apply` automatically
   reads `identified.json` and **appends a `client` or `lead` tag** to the array
   for known senders (e.g. `["FYI-Read", "client"]`). For any message classified
   **Notification**, the message is **moved** to the Notifications folder (Graph
   `/move`) instead of being labelled — it leaves the Inbox.
8. **Draft replies** for every Client-Urgent message. Generate the reply body
   per the **Draft reply template**, then create a reply draft in the Drafts
   folder (`scripts/graph_triage.py draft --message-id <id> --body-file
   <path>`). Drafts are created as proper replies (threaded to the original),
   never sent. Creating the draft tags **both** the draft (in the Drafts folder)
   and the original inbox message with `triage_draft` (each also keeps its
   `client`/`lead` identity tag): the draft becomes `["triage_draft", "client"]`
   and the inbox message becomes `["Client-Urgent", "triage_draft", "client"]` —
   so Scott can spot triage-generated drafts in the Drafts folder *and* see which
   urgent inbox items already have a draft waiting. The draft's body and
   categories are set in **separate** Graph PATCHes (body first), and the command
   **reads the categories back** to confirm they stuck — if Graph drops a tag it
   prints `WARN: … categories did not stick` instead of failing silently. To skip
   draft creation on a re-run, pass `--no-drafts` (see **Re-run handling**).
9. **Summarize.** Print a bulleted summary table of the Client-Urgent items to
   the chat (see **Summary output format**), and a one-line count of how many
   landed in each category.

Auto-apply is the default: categories, moves, and drafts are written without
pausing for per-item approval. Drafts are never *sent* — Scott reviews and
sends from Outlook. If Scott says "show me the plan first," stop after step 6
and print the classification table for approval before writing anything
(moving Notification mail out of the Inbox is the one step worth previewing if
he's cautious).

## Classification rules

Assign each message to **exactly one** bucket. When two could apply, use the
priority order Client-Urgent > Internal-Task > FYI-Read > Archive >
Notification (a real client question outranks an automated-looking footer,
etc. — a human asking something is never a Notification just because it has a
noreply-looking header).

**Use `triage-run/identified.json` first.** It tells you, per message, whether
the sender is a known `client`, `lead`, or `unknown`. Apply these identity
rules before falling back to content signals:

- **Sender is a known `lead`** → **Client-Urgent**, always. A prospect reaching
  out is revenue; respond fast and draft a reply. (Leads do not get a separate
  bucket — they ride the Client-Urgent flow.)
- **Sender is a known `client`** → **Client-Urgent only if the email also has a
  question or problem signal** (a question mark; "error," "not working," "can't
  access," "urgent," a deadline). A known client's bare "thanks, all set!" is
  **not** urgent — classify it on content (FYI-Read / Archive / Internal-Task).
- **Sender is `unknown`** → classify purely on the content rules below; identity
  adds nothing.

- **Client-Urgent** — A known lead (any email), or a known client / named human
  on a client matter asking a question or reporting an error/problem that needs
  a response within 24 hours. Signals: a question mark, words like "error," "not
  working," "can't access," "urgent," "ASAP," or a deadline. A genuine client or
  lead request always beats a generic-looking signature block.
- **Internal-Task** — From a team member or an internal system, requiring Scott
  to update a spreadsheet or complete an administrative task. Signals: "please
  update," "can you add," "needs your sign-off," task-tracker notifications,
  internal tool alerts that imply an action.
- **FYI-Read** — Newsletters, industry updates, or low-priority company
  announcements that require zero reply. Signals: bulk/marketing headers, "no
  reply needed," digest formatting, unsubscribe links on editorial content.
- **Archive** — Resolved or already-handled human threads you want to keep but
  needn't act on. Signals: "this ticket has been resolved," "thanks, all set,"
  closed loops from a real person. Labelled gray; stays in the Inbox.
- **Notification** — Pure machine-generated mail with no human on the other
  end: receipts, payment/booking confirmations, `noreply@`/`no-reply@` senders,
  delivery and read receipts, calendar accept/decline notices, automated system
  alerts. These are **moved to the Notifications folder** (out of the Inbox),
  not labelled. When automated-but-keepable (a receipt) overlaps with Archive,
  prefer Notification — the goal is to get machine mail out of the Inbox.

Edge handling: if a message is ambiguous, prefer the higher-priority bucket
and note the uncertainty in the rationale field. Do not invent a sixth bucket.

## Outlook category color map

When creating categories, use these presets (Graph `preset` values):

| Category       | Color label | Graph preset  |
|----------------|-------------|---------------|
| Client-Urgent  | Red         | preset0       |
| Internal-Task  | Yellow      | preset4       |
| FYI-Read       | Green       | preset3       |
| Archive        | Gray        | preset8       |
| triage_draft   | Blue        | preset5       |
| client         | Teal        | preset7       |
| lead           | Orange      | preset1       |

`triage_draft` marks every message that got a draft — applied to **both** the
draft (in the Drafts folder) and its original inbox message. `client` and `lead`
are **identity tags** layered on top of the triage category for every inbox
message whose sender Supabase identified as a known client or lead (from
`identified.json`). So a known-client urgent message ends up
`["Client-Urgent", "triage_draft", "client"]` in the inbox, with its draft
tagged `["triage_draft", "client"]` in the Drafts folder; a lead's non-drafted
message is `["Client-Urgent", "lead"]`. **Notification** is not in this table —
it has no category; those messages are moved to the Notifications mail folder
instead (and machine mail has no client/lead identity anyway).

If a category already exists under the same name with a different color, leave
it as-is — do not overwrite Scott's existing setup.

## Draft reply template

For **every** Client-Urgent message, draft a reply in a polite, professional,
helpful tone. **Pick the tone from the sender's identity** in
`triage-run/identified.json`:

- `kind: "client"` (or `unknown`) → **existing-client tone** (this section):
  you're already engaged, so acknowledge the request and commit to a turnaround.
- `kind: "lead"` → **lead tone** (the "Lead tone" subsection below): they're a
  prospect, not yet a client, so the goal is to welcome them and get them onto a
  consultation — not to promise work on a matter that doesn't exist yet.

**Shared rules (both tones):** stay **under 150 words**; use clear line breaks
between the greeting, body, offer, and signoff (not one dense paragraph);
personalize the greeting with the sender's first name when it's parseable; close
with the signoff from `triage-context.md` (field `signoff`); keep the firm's
voice — warm and competent, no jargon.

### Existing-client tone (`client` / `unknown`)

In addition to the shared rules, the reply MUST:

1. Acknowledge receipt of their request.
2. Commit to a **2 business day** turnaround, phrased to match the email:
   - If the client reported an **error/problem** ("can't access," "not
     working," "broken"), say the **fix** will be completed within two
     business days.
   - If the client asked a **question** (no error — just needs an answer or
     clarification), say you'll **have an answer for them** within two
     business days. Don't promise a "fix" when there's nothing broken.
3. Offer the calendar link (from `triage-context.md`, field `calendar_link`)
   for a follow-up call.

**Example shape — ERROR/problem report (adapt wording; do not copy verbatim):**

```
Hi [First name],

Thank you for reaching out — I've received your note and we're on it.

We expect to have the fix completed within two business days, and I'll follow
up as soon as it's resolved.

If it would help to talk it through sooner, you're welcome to grab a time here:
[calendar_link]

Best,
[signoff]
```

**Example shape — QUESTION (no error; client just needs an answer):**

```
Hi [First name],

Thanks for the question — I've got it, and I'm looking into it now.

I'll have an answer back to you within two business days so you're set before
your [deadline/closing/signing].

If you'd rather talk it through, you're welcome to grab a time here:
[calendar_link]

Best,
[signoff]
```

### Lead tone (`kind: "lead"`)

A lead is a **prospective** client — there's no engagement or matter yet, so do
**not** acknowledge "your request," promise a "fix," or commit to a 2-business-
day turnaround on work. The job of this reply is to make them feel welcomed and
move them toward a consultation. In addition to the shared rules above, the
reply MUST:

1. Warmly thank them for their **interest in the firm** / for reaching out.
2. Briefly affirm you can help with what they raised (estate planning, probate,
   etc.) — without giving specific legal advice over email.
3. Make booking a **consultation the primary call to action**, using the
   `calendar_link` from `triage-context.md` (it points at the discovery-call
   booking page). Frame the link as the next step, not a fallback.
4. Invite them to reply with any questions in the meantime.

Keep it inviting and low-pressure — no deadlines, no "turnaround." If the
lead's `status` in `identified.json` is already `consult_booked` (or similar),
acknowledge the upcoming call instead of asking them to book again.

**Example shape — LEAD (adapt wording; do not copy verbatim):**

```
Hi [First name],

Thank you for reaching out — I'd be glad to help you with [their topic, e.g.
your estate planning].

The best next step is a short consultation so I can understand your situation
and walk you through how we'd approach it. You can grab a time that works here:
[calendar_link]

In the meantime, feel free to reply with any questions at all.

Best,
[signoff]
```

Write the body to a file and pass it to the `draft` command so formatting and
line breaks survive intact. (The draft is still tagged `triage_draft` + `lead`
on both the draft and the inbox message, exactly as for clients.)

## Summary output format

After everything is written, print to the chat:

```
## Client-Urgent — needs a reply within 24h  (drafts created in Drafts folder)

- **[Sender name]** ([client]/[lead]) — [Subject] — [one-line gist of the ask]
- **[Sender name]** ([client]/[lead]) — [Subject] — [one-line gist of the ask]

## Triage counts
Client-Urgent: X · Internal-Task: Y · FYI-Read: Z · Archive: W · Notification: V   (N total)
```

Tag each urgent line with its Supabase identity — `(client)` or `(lead)` from
`identified.json` — so Scott can see at a glance which urgent items are
existing clients vs new prospects. Omit the tag for `unknown` senders.

If there are zero Client-Urgent items, say so plainly and still print the
counts. Don't pad the table with the other categories — the summary is
deliberately just the urgent ones, since those are the ones Scott acts on now.

## Notes & guardrails

- **Never deletes, marks-as-read, or sends.** The only mutations are: set
  categories, **move** Notification-type mail to the Notifications folder, and
  create unsent drafts. It never empties the Inbox of human mail or sends
  anything.
- **Moving is limited to Notification mail.** Only messages classified
  Notification leave the Inbox, and only into the Notifications folder. Nothing
  else is moved. The move is reversible — Scott can drag anything back.
- **Drafts are threaded replies.** Use Graph's `createReply` so the draft sits
  on the original conversation, with the client already in the To line.
- **Categories stack deterministically, recomputed every run.** An inbox
  message's array is the triage category plus the `client`/`lead` identity tag
  if Supabase knew the sender, plus `triage_draft` once it has a draft: an
  unknown FYI is `["FYI-Read"]`, a known-client FYI is `["FYI-Read", "client"]`,
  a drafted client-urgent inbox item is `["Client-Urgent", "triage_draft",
  "client"]`, and that item's draft (in the Drafts folder) is
  `["triage_draft", "client"]`. Because `apply`/`draft` recompute and
  **replace** the whole array each run (never append blindly), re-running
  overwrites cleanly instead of growing the list.
- **Idempotent labels/moves, additive drafts.** Re-running re-classifies and
  overwrites categories cleanly, and re-moving an already-moved message is a
  no-op miss (it's no longer in the Inbox fetch). It will, however, create a
  *second* draft per Client-Urgent item, since Graph has no way to know a prior
  draft exists.

### Re-run handling

Before drafting on any run, check whether this looks like a re-run of an
inbox you've already triaged (same messages still unread, drafts likely
already sitting in the Drafts folder). If so, **ask Scott** whether to:

- **Skip drafting** — re-apply categories only. Pass `--no-drafts` so no new
  drafts are created (labels still get refreshed).
- **Re-draft anyway** — proceed, and remind him to clear the earlier drafts
  from the Drafts folder so he isn't choosing between duplicates.

Default to asking rather than silently creating duplicate drafts. Category
re-application is always safe to repeat.
- **Secrets stay local.** `triage-context.md` is never echoed. If auth fails,
  report the Graph error text but never the secret.
- **Supabase is read-only and degrades gracefully.** `identify` only *reads*
  via the `triage_match_sender` RPC — it never writes to the firm database. If
  Supabase is unreachable or a sender errors, that sender is marked `unknown`
  and triage proceeds on content signals alone; it never blocks the run.
- **Identity is a signal, not PII to leak.** Use `kind`/`display_name` to
  classify and to label the summary; don't dump raw client/lead records into
  the chat.

See `references/graph-setup.md` for the one-time app-registration steps,
`references/supabase-setup.md` for the sender-identification RPC, and the
exact permissions required.
