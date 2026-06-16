---
name: matter-ops-board
description: >
  Builds Scott's weekly matter ops board — one view to run the practice from.
  Pulls the next 7–14 days of Outlook calendar events, enumerates active
  matter and lead folders in OneDrive/SharePoint, lists each matter's
  documents, and cross-references email last-touch dates to produce a board
  with: this week's client meetings, deadlines/dates, missing client documents
  by matter, and matters that have gone quiet too long.
  Triggers: "matter ops board", "weekly ops board", "build my weekly board",
  "what needs attention this week", "run the practice view", "which matters
  have gone quiet", "what client docs are missing", "weekly matter review",
  "/matter-ops-board", or any request for a consolidated weekly view across
  calendar + client folders.
  Does NOT trigger for inbox triage (use outlook-inbox-triage), drafting
  documents, sending engagement letters, or single-matter deep dives.
compatibility: >
  Folder/document steps run primarily on the LOCAL OneDrive sync at
  /Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw (Mac mini),
  via Bash — with the Microsoft 365 MCP connector
  (sharepoint_folder_search / sharepoint_search) as fallback for headless
  sessions. Calendar and email steps always use the MCP connector
  (outlook_calendar_search, outlook_email_search) authenticated as
  scott@aubreylegal.com. Read-only throughout. All commands and queries
  were run and verified live on 2026-06-11.
---

# Weekly Matter Ops Board

## Purpose

One board, four sections, built from live data:

1. **This week** — client meetings and firm commitments from Outlook calendar.
2. **Deadlines & dates** — date-bearing items found in calendar + matter docs.
3. **Missing client docs** — per active matter, what the folder should contain
   at its stage but doesn't.
4. **Gone quiet** — active matters with no document activity AND no email
   traffic in 14+ days.

The "driver" for this skill is the Microsoft 365 MCP connector. Every tool
call below is a verified recipe — run them as written, then assemble the
board. If a tool is in the deferred list, load it first with ToolSearch
(`select:` the exact names).

## Where things live (verified 2026-06-11, local + tenant)

Scott's OneDrive is synced locally at
`/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/` — **use the
local filesystem for all folder enumeration and inventory** (complete,
instant, immune to the Graph 500s that plague `sharepoint_folder_search`).
The same paths appear in Graph under `Documents/` on
`aubreylegal-my.sharepoint.com/personal/scott_aubreylegal_com`.

| Path under the OneDrive root | What it is |
|---|---|
| `Aubrey Law/Matters/<Last, First — YYYY>/` | **NEW canonical matter root** — numbered stage folders `01 - Intake`, `02 - Design`, `03 - Drafts`, `04 - Signed Documents`, `05 - Correspondence`. Migration in progress: most are empty scaffolds; a few (Duchin, Mello, O'Connell) already hold the CURRENT drafts — check here FIRST, it can be newer than the old root |
| `Aubrey Law/Leads/<Last, First — YYYY>/` | New lead root. Contains junk entries `FOLDER, TEST — 2026` and `Aubrey, Scott — 2026` — skip those |
| `Active Clients/<matter>/` | OLD matter root, still holds most content. Naming: `2026-EPLP-RONDEAU`, `2026_Cohen, Marc & Sharon`, `202500078-DALY` |
| `Leads/<matter>/` | Old lead root (`2026-EPLP-…`, plus `2026-PR-…` probate, `2026-EP-…`) |
| `Clio/<Last, First>/`, `Lawmatics/` | Legacy per-client folders (423 and 522 entries — never enumerate; check by name only) |
| `Archived Clients/`, `ARCHIVE/` paths | Closed/old — exclude |

**A matter can live in up to three places at once** (new root, old root, old
lead folder) — e.g. Duchin exists in all three, with the newest drafts in the
NEW root. Dedupe by client surname and take the newest file across all
copies before declaring anything missing or stale.

Old-root subfolders: `Drafts`, `Design`, `Financial`, `Correspondence`,
`Proposal`, `Final`, `Signed Estate Plan`, `Miscellaneous`.

## Step 1 — Calendar (meetings + deadline dates)

```
outlook_calendar_search
  query: "*"
  afterDateTime: "today"
  beforeDateTime: "in 14 days"
  order: "oldest"
  limit: 25
```

Paginate with `offset` if the final item has `nextOffset`. Classify each event:

- **Client meeting** — summary contains `Matter Phone:` or a
  `app.lawmatics.com/booking/.../reschedule` link, or subject matches the
  firm's session names ("Peace of Mind Planning Session", "Draft Review",
  "Signing"). Attendee email identifies the client.
- **Vendor/CLE** — organizer is not `scott@aubreylegal.com` (e.g. Zoom
  webinars). List in a one-line "FYI" row at most.
- **Personal** — no attendees and non-matter subject (haircuts, graduations,
  `BLOCK` holds). Show BLOCK holds as capacity; omit the rest from the board.

The subject's trailing name ("… - Steven R. Maxwell") is the matter key used
to join against folders and email in later steps.

## Step 2 — Enumerate active matters and leads (LOCAL — primary path)

```bash
cd "/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw"
ls "Aubrey Law/Matters"; ls "Aubrey Law/Leads"   # new roots (canonical names)
ls -t "Active Clients" | head -30                # old root, newest-first
ls -t "Leads" | head -20                         # old lead root
```

This is the complete matter universe in four instant commands — no
pagination, no 500s. Drop junk (`untitled folder`, `FOLDER, TEST — 2026`,
`Aubrey, Scott — 2026`, `Review`, loose files).

## Step 3 — Per-matter activity + document inventory (LOCAL)

Newest file per matter across roots (the real activity signal — folder
mtimes don't bubble up from files):

```bash
cd "/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw"
for d in "Aubrey Law/Matters"/*/ "Active Clients"/*/; do
  newest=$(find "$d" -type f -not -name '.DS_Store' -exec stat -f '%m %N' {} + 2>/dev/null | sort -rn | head -1)
  echo "$(basename "$d") :: $(date -r ${newest%% *} '+%Y-%m-%d' 2>/dev/null) ${newest#* }"
done
```

An empty date = scaffold-only folder (check the OLD root for that client
before calling it inactive). Full inventory of one matter:

```bash
find "Aubrey Law/Matters/Duchin, Ran — 2026" -type f -not -name '.DS_Store'
```

OneDrive Files-On-Demand caveat: names and mtimes are always present
locally, but cloud-only files have no content on disk — fine for the board
(names + dates are all it needs); don't try to read/parse them without
letting OneDrive download first.

### Graph fallback (headless / cloud sessions without the Mac mini)

If the local path doesn't exist, fall back to the MCP connector:
`sharepoint_folder_search name:"Active Clients"` (paginate via `nextOffset`;
~222 results mixing matter folders and subfolders — keep only those whose
webUrl parent is the root itself), and
`sharepoint_search query:"*" folderName:"<exact matter folder>"` per matter.
If pagination gets killed by transient 500s, don't stall: page 1 plus matter
names visible in subfolder paths yields ~20 matters — proceed, note the
coverage gap in the board footer, and spend the budget on Step 4 instead.

### Missing-docs analysis (applies to either path)

Prioritize every matter with a meeting this week, plus every quiet suspect.
Compare each matter's inventory against the expected estate-plan set by
stage. New-root stage folders map directly: `01 - Intake` → intake/organizer,
`02 - Design` → design + client financials, `03 - Drafts` → draft set,
`04 - Signed Documents` → executed plan.

| Stage signal | Expected in folder |
|---|---|
| Engaged (any) | `Organizer Summary`, proposal PDF, signed engagement agreement |
| Pre-draft | Design / Financial contents (client-provided asset docs) |
| Drafting | Drafts: Will, Trust, HCP, DPOA, HIPAA, Advance Directive, PPM, Assignment of Personal Property, Certificate of Trust, Deed (if real estate) — **for BOTH spouses on a couple's matter** (verified gap: Ran's ancillaries drafted, Ofra's missing) |
| Post-signing | Signed Documents contents, recorded deed |

An empty Financial/Intake folder or no client-provided documents weeks
after engagement = "missing client docs" — that's the chase list.

## Step 4 — Gone quiet (cross-reference email)

For each matter whose newest file is >14 days old, check email last-touch:

```
outlook_email_search  query: "<client last name>"  limit: 5
```

Newest `receivedDateTime` across results = last email touch. A matter is
**gone quiet** only if BOTH document activity and email are >14 days old
(verified: searching "Maxwell" surfaced both calendar invites and client
threads with dates). Use 7 days for leads — pipeline cools faster.

Three refinements from live runs (2026-06-11):

- **Count only HUMAN messages for last-touch.** Lawmatics sends automated
  stage emails ("Your estate plan: Drafting / Client Review / Design") from
  Scott's own address — they reset the naive last-touch date without anyone
  actually talking. A matter showing only stage emails since the client's
  last real message IS quiet (e.g. client sent draft feedback 5/21, only
  automation after → 21 days quiet, not 9).
- **Ball-in-whose-court matters more than the date.** If the LAST human
  message is FROM the client (a question, draft feedback, "what are next
  steps?"), flag it red regardless of age — the client is waiting. If the
  last message is from Scott, it's amber (nudge) territory.
- **Money paid + no doc movement = its own flag.** A Lawmatics
  "Invoice Payment Success" email with no Drafts activity since means a
  client has paid and is waiting on work product. Surface it under Missing
  Docs even though it's neither quiet nor doc-missing in the strict sense.

Also surface any UNREAD client emails (`isRead: false`) found during these
checks — e.g. a client confirming Monday's meeting overnight.

## Step 5 — Assemble the board

Render in chat as markdown, sections in this order, most actionable first:

1. **🔴 Gone quiet** — matter, days silent, last touch (doc/email), suggested next move
2. **📄 Missing client docs** — matter, what's missing, who owes it
3. **📅 This week** — day-by-day client meetings (with the matter folder's
   readiness: e.g. "Draft Review Mon — all 9 drafts present ✓")
4. **⏳ Deadlines & dates** — anything date-bearing from calendar/docs
5. **🌱 Pipeline** — leads with folder activity dates

Keep client details to name + matter stage; don't reproduce document
contents or attendee lists on the board. End with an **"If you do three
things"** closer — the three highest-leverage actions across all sections
(reply to the oldest client-waiting thread beats everything else). Add a
one-line coverage note if enumeration was incomplete. Offer to save as a
dated md/docx under the firm's output conventions (see
`Aubrey Law — Firm Context.md`) only if Scott asks.

## Gotchas (all hit live, 2026-06-11)

- **Graph search lags / misses the local truth.** The new
  `Aubrey Law/Matters` root held Duchin drafts dated 6/10 while Graph
  surfaced only the old root's 6/8 copies — a Graph-only run produced a
  stale missing-docs list, and Graph pagination never reached several real
  matters (O'Connell, Shen, Berenson, Floyd, Ayotte). When the local sync is
  available, treat it as the source of truth for folders and files.

- **`sharepoint_folder_search` 500s on broad generic terms.** `name: "clients"`
  returned `INTERNAL_ERROR` / Graph 500 twice in a row; `name: "Active Clients"`,
  `"Leads"`, and surnames (`"Maxwell"`) work fine. If you get a 500, narrow the
  term — retrying the same term fails again.
- **SharePoint search 500s also come in transient bursts** (seen 2026-06-11):
  a whole parallel batch of folder/document searches failed with Graph 500 —
  including queries that succeeded minutes earlier — then recovered ~1 minute
  later. Outlook mail/calendar endpoints were unaffected. When a batch 500s,
  switch to Outlook-side work (email last-touch checks), then retry SharePoint
  serially. Don't burn retries back-to-back.
- **Empty output from a folder-scoped listing = genuinely empty folder.**
  `query: "*" folderName: "Maxwell, Steven"` returned no output — that matter
  folder has no files. Distinguish that from a 500 error before concluding
  docs are missing, and content-search the surname to check whether the
  client's documents live in an ARCHIVE path instead.
- **`read_resource` on a folder URI is nearly useless** — returns only bare
  child *names* (no URIs, no dates), and empty output for an empty folder.
  Always use `sharepoint_search query:"*" folderName:...` to list a folder.
- **Timestamps lie on relevance searches.** Content searches (e.g.
  `query: "estate plan"`) return `lastModifiedDateTime: 1900-01-01` on many
  hits. Folder-scoped `query: "*"` listings return real dates. Trust dates
  only from folder listings or `afterDateTime`-filtered searches.
- **`folderName` is a partial match.** `folderName: "Drafts"` would match every
  matter's Drafts subfolder — always pass the full matter folder name
  (`"2026-EPLP-RONDEAU"`), which is unique.
- **Don't enumerate `Clio/`** — 911 folders and `offset` caps at 1000; you
  can't page it all and most are inactive. Query it by surname only when a
  specific client doesn't appear under Active Clients.
- **Recurring CLE noise:** "Estate Planning with KC" (organizer
  `hello@2hourlifestylelawyer.com`) recurs weekly with ~85 attendees — never
  echo its attendee list; classify as FYI.
- **A matter can exist in multiple roots simultaneously** (e.g. Korboe and
  Goss-Plata appear under both `Leads/` and `Active Clients/`) — dedupe by
  client name, prefer the Active Clients copy.
- **Same-name folder collisions:** generic searches for a surname also hit
  `ARCHIVE/` copies of the same client (Maxwell exists in 4 places). Filter
  ARCHIVE first, then dedupe.
- **`sharepoint_search` with `query: "*"` + `afterDateTime`** is a fast
  whole-drive "what moved this week" sweep (~325 results for 2 weeks), but
  it includes template edits and OneDrive sync noise (`SyncEngine` content)
  — use it as a hint list, not as the board's source of truth.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `INTERNAL_ERROR ... graphErrorCode: InternalServerError` on folder search | Term too generic — use "Active Clients", "Leads", or a surname |
| Folder listing returns names but you need dates/URIs | You used `read_resource` on a folder — switch to `sharepoint_search query:"*" folderName:<name>` |
| Every doc shows 1900-01-01 modified date | Relevance-ranked content search — re-query folder-scoped or with `afterDateTime` |
| Calendar search returns relevance-ordered jumble | Pass `order: "oldest"` to force chronological + date-bounded mode |
| Client has meeting but no Active Clients folder | Check both lead roots, then `sharepoint_folder_search name:"<surname>"` (catches Clio/legacy locations) |
