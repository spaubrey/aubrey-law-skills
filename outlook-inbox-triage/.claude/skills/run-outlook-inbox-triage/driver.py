#!/usr/bin/env python3
"""
driver.py — smoke harness for the outlook-inbox-triage CLI (scripts/graph_triage.py).

The CLI's only real work is Microsoft Graph + Supabase I/O, so driving it for
real would write categories, move mail, and create drafts in a LIVE law-firm
mailbox. This harness instead stands up a local mock that serves BOTH the Graph
+ token endpoints and the Supabase PostgREST RPC, points the real CLI at it via
GRAPH_BASE / GRAPH_TOKEN_URL (and a mock supabase_url in the context file), and
runs the full triage flow end to end:

    auth-check -> ensure-categories -> ensure-folder -> fetch
              -> identify (Supabase client/lead lookup)
              -> apply (labels + a Notification move) -> draft (+ triage_draft tag)

It then asserts on what the CLI actually sent: the fetch query, the
triage_match_sender RPC calls + the identified.json it writes (client/lead/
unknown), the single-element category PATCH, the /move for the Notification
item, the createReply + HTML-converted body, and the
["Client-Urgent","triage_draft"] tag on the original. Real argv, real
load_context, real requests calls — only the Graph + Supabase hosts are faked.

The real Supabase RPC (triage_match_sender) is verified separately against the
live project; see SKILL.md "Direct invocation". This driver mocks it so the run
is reproducible and touches no real data.

Run from the skill's working directory (the one holding scripts/ and
triage-context.md):

    python3 .claude/skills/run-outlook-inbox-triage/driver.py

Exit 0 + "ALL CHECKS PASSED" = the CLI drives Graph correctly. Non-zero = a step
broke; the failing assertion is printed.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

# --- locate the CLI relative to this driver (skill lives under <unit>/.claude/...)
UNIT = Path(__file__).resolve().parents[3]
CLI = UNIT / "scripts" / "graph_triage.py"
USER = "scott@aubreylegal.com"

# Every request the CLI makes is recorded here for post-run assertions.
CALLS = []  # list of (method, path, query, body-dict-or-text)
# Stateful category store: PATCH writes here, GET reads back — so the CLI's
# set_categories_verified() read-back behaves like a real mailbox.
MESSAGE_CATS = {}  # msg_id -> [categories]

FAKE_MESSAGES = [
    {"id": "msg-client-1", "subject": "Can't access my case portal",
     "from": {"emailAddress": {"name": "Dana Cole", "address": "dana@client.com"}},
     "receivedDateTime": "2026-06-11T14:00:00Z", "bodyPreview": "I can't log in — urgent",
     "conversationId": "c1", "webLink": "http://x"},
    {"id": "msg-lead-1", "subject": "Question about your estate planning services",
     "from": {"emailAddress": {"name": "Pat Lee", "address": "pat@prospect.com"}},
     "receivedDateTime": "2026-06-11T13:30:00Z", "bodyPreview": "considering a trust",
     "conversationId": "c4", "webLink": "http://x"},
    {"id": "msg-note-1", "subject": "Your receipt from Stripe",
     "from": {"emailAddress": {"name": "Stripe", "address": "noreply@stripe.com"}},
     "receivedDateTime": "2026-06-11T13:00:00Z", "bodyPreview": "payment confirmation",
     "conversationId": "c2", "webLink": "http://x"},
    {"id": "msg-fyi-1", "subject": "Bar Association weekly digest",
     "from": {"emailAddress": {"name": "MA Bar", "address": "news@massbar.org"}},
     "receivedDateTime": "2026-06-11T12:00:00Z", "bodyPreview": "this week in law",
     "conversationId": "c3", "webLink": "http://x"},
]

# Mock Supabase triage_match_sender RPC results, keyed by lower(email).
FAKE_CONTACTS = {
    "dana@client.com": {"kind": "client", "display_name": "Dana Cole", "status": "active"},
    "pat@prospect.com": {"kind": "lead", "display_name": "Pat Lee", "status": "consult_booked"},
}


class MockGraph(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence default stderr logging
        pass

    def _send(self, code, obj=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if obj is not None:
            self.wfile.write(json.dumps(obj).encode())

    def _record(self, method):
        u = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode() if length else ""
        body = raw
        if raw and "application/json" in (self.headers.get("Content-Type") or ""):
            try:
                body = json.loads(raw)
            except Exception:
                body = raw
        CALLS.append((method, u.path, u.query, body))
        return u, body

    def do_POST(self):
        u, body = self._record("POST")
        p = u.path
        if p.endswith("/oauth2/v2.0/token"):
            return self._send(200, {"access_token": "fake-token", "expires_in": 3600})
        if p.endswith("/rest/v1/rpc/triage_match_sender"):
            email = (body or {}).get("p_email", "").lower().strip()
            hit = FAKE_CONTACTS.get(email)
            return self._send(200, [hit] if hit else [])  # [] == unknown
        if p.endswith("/outlook/masterCategories"):
            return self._send(201, {"id": "cat-x", "displayName": body.get("displayName")})
        if p.endswith("/mailFolders"):
            return self._send(201, {"id": "folder-notifications",
                                    "displayName": body.get("displayName")})
        if p.endswith("/move"):
            return self._send(201, {"id": "moved-" + p.split("/messages/")[1].split("/")[0]})
        if p.endswith("/createReply"):
            mid = p.split("/messages/")[1].split("/")[0]
            return self._send(201, {"id": f"draft-of-{mid}"})
        return self._send(404, {"error": "unhandled POST " + p})

    def do_GET(self):
        u, _ = self._record("GET")
        p = u.path
        if re.search(r"/users/[^/]+$", p):  # mailbox info (auth-check)
            return self._send(200, {"displayName": "Scott Aubrey", "mail": USER})
        if p.endswith("/outlook/masterCategories"):
            return self._send(200, {"value": []})  # none exist yet -> CLI creates all
        if p.endswith("/mailFolders"):  # folder lookup -> empty so CLI creates it
            return self._send(200, {"value": []})
        if p.endswith("/mailFolders/Inbox/messages"):
            return self._send(200, {"value": FAKE_MESSAGES})
        m = re.search(r"/messages/([^/?]+)$", p)  # category read-back verify
        if m:
            mid = m.group(1)
            return self._send(200, {"id": mid, "categories": MESSAGE_CATS.get(mid, [])})
        return self._send(404, {"error": "unhandled GET " + p})

    def do_PATCH(self):
        u, body = self._record("PATCH")
        m = re.search(r"/messages/([^/?]+)$", u.path)
        if m and isinstance(body, dict) and "categories" in body:
            MESSAGE_CATS[m.group(1)] = body["categories"]  # persist like a mailbox
        return self._send(200, {"id": u.path.split("/")[-1]})


def run_cli(env, *cli_args):
    proc = subprocess.run([sys.executable, str(CLI), *cli_args],
                          cwd=env["_CWD"], env=env, capture_output=True, text=True)
    print(f"$ graph_triage.py {' '.join(cli_args)}")
    if proc.stdout.strip():
        print("  " + proc.stdout.strip().replace("\n", "\n  "))
    if proc.returncode != 0:
        print("  STDERR: " + proc.stderr.strip().replace("\n", "\n  "))
        raise SystemExit(f"FAIL: CLI exited {proc.returncode} for {cli_args}")
    return proc


def find(method, path_substr):
    return [c for c in CALLS if c[0] == method and path_substr in c[1]]


def main():
    if not CLI.exists():
        raise SystemExit(f"FAIL: CLI not found at {CLI}")

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockGraph)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    threading.Thread(target=server.serve_forever, daemon=True).start()

    work = Path(tempfile.mkdtemp(prefix="triage-smoke-"))
    (work / "triage-context.md").write_text(
        "tenant_id: test-tenant\n"
        "client_id: test-client\n"
        "client_secret: test-secret\n"
        f"user_id: {USER}\n"
        f"supabase_url: {base}\n"           # mock PostgREST lives on the same host
        "supabase_key: test-publishable\n"
        "notifications_folder: Notifications\n"
        "default_count: 50\n"
    )

    env = dict(os.environ)
    env["GRAPH_BASE"] = f"{base}/v1.0"
    env["GRAPH_TOKEN_URL"] = f"{base}/test-tenant/oauth2/v2.0/token"
    env["_CWD"] = str(work)

    # 1. Full happy-path flow against the mock.
    run_cli(env, "auth-check")
    run_cli(env, "ensure-categories")
    run_cli(env, "ensure-folder")
    run_cli(env, "fetch", "--count", "50")
    run_cli(env, "identify")

    # Agent classification step (done by Claude in production) — simulate it,
    # applying the identity rules: known lead -> Client-Urgent; known client +
    # question/problem -> Client-Urgent; unknown -> classify on content.
    classified = [
        {"id": "msg-client-1", "subject": "Can't access my case portal",
         "category": "Client-Urgent"},   # client + problem
        {"id": "msg-lead-1", "subject": "Question about your estate planning services",
         "category": "Client-Urgent"},   # known lead -> Client-Urgent
        {"id": "msg-note-1", "subject": "Your receipt from Stripe",
         "category": "Notification"},
        {"id": "msg-fyi-1", "subject": "Bar Association weekly digest",
         "category": "FYI-Read"},
    ]
    (work / "classified.json").write_text(json.dumps(classified))
    run_cli(env, "apply", "--input", "classified.json")

    body = work / "reply.txt"
    body.write_text("Hi Dana,\n\nThanks for reaching out.\n\nBest,\nScott")
    run_cli(env, "draft", "--message-id", "msg-client-1", "--body-file", str(body))

    # ---- assertions on what the CLI actually sent ----
    checks = []

    def check(name, cond):
        checks.append((name, cond))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    print("\n== assertions ==")
    # fetch sent the right OData query
    fetches = find("GET", "/mailFolders/Inbox/messages")
    q = fetches[0][2] if fetches else ""
    check("fetch filters isRead eq false", "isRead+eq+false" in q or "isRead eq false" in q)
    check("fetch orders newest first", "DESC" in q)

    # messages.json written
    mj = work / "triage-run" / "messages.json"
    check("messages.json written with 4 msgs",
          mj.exists() and len(json.loads(mj.read_text())) == 4)

    # identify: Supabase RPC called per unique sender, identified.json correct
    rpc_calls = find("POST", "/rest/v1/rpc/triage_match_sender")
    check("RPC called once per unique sender (4)", len(rpc_calls) == 4)
    idf = work / "triage-run" / "identified.json"
    by_id = {r["id"]: r for r in json.loads(idf.read_text())} if idf.exists() else {}
    check("identified.json written for all 4", len(by_id) == 4)
    check("known client identified as client",
          by_id.get("msg-client-1", {}).get("kind") == "client")
    check("known lead identified as lead",
          by_id.get("msg-lead-1", {}).get("kind") == "lead")
    check("unknown sender marked unknown",
          by_id.get("msg-fyi-1", {}).get("kind") == "unknown")
    check("identity carries display_name",
          by_id.get("msg-client-1", {}).get("display_name") == "Dana Cole")

    # ensure-categories created the 4 originals + triage_draft + client + lead = 7
    cat_posts = [c for c in find("POST", "/outlook/masterCategories")]
    cat_names = {c[3].get("displayName") for c in cat_posts}
    check("triage_draft category created", "triage_draft" in cat_names)
    check("client + lead categories created",
          "client" in cat_names and "lead" in cat_names)
    check("7 master categories created", len(cat_posts) == 7)

    # Notification item was MOVED, not labelled
    moves = find("POST", "/messages/msg-note-1/move")
    check("notification message moved to folder", len(moves) == 1)
    check("move targets the Notifications folder id",
          bool(moves) and moves[0][3].get("destinationId") == "folder-notifications")
    note_patches = [c for c in find("PATCH", "/messages/msg-note-1")]
    check("notification message NOT category-PATCHed", len(note_patches) == 0)

    # unknown sender -> single-element array (no identity tag)
    fyi_patch = find("PATCH", "/messages/msg-fyi-1")
    check("unknown FYI labelled single-element array",
          bool(fyi_patch) and fyi_patch[0][3].get("categories") == ["FYI-Read"])

    # known client -> triage category + "client" identity tag
    client_apply = find("PATCH", "/messages/msg-client-1")
    check("client msg apply-tagged Client-Urgent + client",
          bool(client_apply) and
          set(client_apply[0][3].get("categories", [])) == {"Client-Urgent", "client"})

    # known lead -> Client-Urgent + "lead" identity tag
    lead_patch = find("PATCH", "/messages/msg-lead-1")
    check("lead msg labelled Client-Urgent + lead",
          bool(lead_patch) and
          set(lead_patch[0][3].get("categories", [])) == {"Client-Urgent", "lead"})

    # draft: createReply on the original; the DRAFT gets the body + triage_draft
    replies = find("POST", "/messages/msg-client-1/createReply")
    check("createReply called on client msg", len(replies) == 1)
    draft_patches = [c for c in find("PATCH", "/messages/draft-of-msg-client-1")
                     if isinstance(c[3], dict)]
    body_patch = next((c for c in draft_patches if "body" in c[3]), None)
    html = body_patch[3]["body"]["content"] if body_patch else ""
    check("draft body converted newlines to <br>", "<br>" in html and "\n" not in html)
    draft_cats = next((c[3]["categories"] for c in draft_patches
                       if "categories" in c[3]), None)
    check("DRAFT tagged triage_draft + client",
          draft_cats is not None and set(draft_cats) == {"triage_draft", "client"})
    check("draft category set as its OWN patch (not bundled with body)",
          body_patch is not None and "categories" not in body_patch[3])
    check("CLI reads back draft categories to verify they stuck",
          len(find("GET", "/messages/draft-of-msg-client-1")) >= 1)
    # the inbox message is ALSO marked triage_draft (last categories PATCH to it)
    orig_cat_patches = [c[3]["categories"] for c in find("PATCH", "/messages/msg-client-1")
                        if isinstance(c[3], dict) and "categories" in c[3]]
    check("inbox message tagged Client-Urgent + triage_draft + client",
          bool(orig_cat_patches) and
          set(orig_cat_patches[-1]) == {"Client-Urgent", "triage_draft", "client"})

    # 2. --no-drafts skips draft creation entirely (re-run guard)
    before = len(find("POST", "/createReply"))
    run_cli(env, "draft", "--message-id", "msg-client-1",
            "--body-file", str(body), "--no-drafts")
    after = len(find("POST", "/createReply"))
    check("--no-drafts creates no new draft", before == after)

    server.shutdown()

    failed = [n for n, ok in checks if not ok]
    print()
    if failed:
        print(f"{len(failed)} CHECK(S) FAILED: {failed}")
        sys.exit(1)
    print(f"ALL CHECKS PASSED ({len(checks)} assertions)")


if __name__ == "__main__":
    main()
