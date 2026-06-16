#!/usr/bin/env python3
"""
graph_triage.py — Microsoft Graph helper for the Outlook inbox triage skill.

Subcommands:
  auth-check          Verify credentials and print the signed-in mailbox.
  ensure-categories   Create the triage categories if missing.
  ensure-folder       Create the "Notifications" mail folder if missing; print id.
  fetch --count N     Fetch last N unread Inbox messages -> triage-run/messages.json
  identify            Look up each sender in Supabase (client vs lead vs unknown)
                        via the triage_match_sender RPC -> triage-run/identified.json
  apply --input F     Apply the triage decision per message from a classified.json:
                        - category == "Notification"  -> MOVE to Notifications folder
                        - any other category          -> set that single category
  draft --message-id ID --body-file F   Create a threaded reply draft (unsent),
                        then tag BOTH the draft and the original message with the
                        triage_draft category (plus the client/lead identity tag).

Auth: reads triage-context.md (key: value lines) for tenant_id, client_id,
client_secret, and (for delegated flows) user_id / mailbox. Uses the
client-credentials flow by default. Never prints the client secret.

Endpoints are overridable for testing via GRAPH_BASE and GRAPH_TOKEN_URL env
vars — production reads the real Graph/login hosts when those are unset.

This script is deliberately dependency-light: only `requests`.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

# Overridable so a test harness can point the CLI at a local mock Graph server.
GRAPH = os.environ.get("GRAPH_BASE", "https://graph.microsoft.com/v1.0")
RUN_DIR = Path("triage-run")

# Outlook master categories this skill manages. Notification-type mail is moved
# to a folder rather than labelled, so it has no category here.
CATEGORY_PRESETS = {
    "Client-Urgent": "preset0",  # Red
    "Internal-Task": "preset4",  # Yellow
    "FYI-Read": "preset3",       # Green
    "Archive": "preset8",        # Gray
    "triage_draft": "preset5",   # Blue — marks messages that already have a draft
    "client": "preset7",         # Teal — sender is a known client (Supabase)
    "lead": "preset1",           # Orange — sender is a known lead (Supabase)
}

NOTIFICATION_CATEGORY = "Notification"  # classification bucket -> move, not label
IDENTITY_TAGS = {"client", "lead"}      # additive tags from the identify step


def load_context(path="triage-context.md"):
    """Parse simple 'key: value' lines from the context file."""
    ctx = {}
    p = Path(path)
    if not p.exists():
        sys.exit(f"ERROR: {path} not found. Create it from "
                 f"references/triage-context.example.md first.")
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        ctx[key.strip()] = val.strip()
    return ctx


def get_token(ctx):
    tenant = ctx.get("tenant_id")
    client_id = ctx.get("client_id")
    secret = ctx.get("client_secret")
    if not all([tenant, client_id, secret]):
        sys.exit("ERROR: tenant_id, client_id, and client_secret are required "
                 "in triage-context.md.")
    url = (os.environ.get("GRAPH_TOKEN_URL")
           or f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token")
    data = {
        "client_id": client_id,
        "client_secret": secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    r = requests.post(url, data=data, timeout=30)
    if r.status_code != 200:
        # Surface Graph's error description, but never the secret we sent.
        sys.exit(f"ERROR: token request failed ({r.status_code}): {r.text}")
    return r.json()["access_token"]


def mailbox_base(ctx):
    """Application flows must target a specific user; delegated can use /me."""
    user = ctx.get("user_id") or ctx.get("mailbox")
    return f"{GRAPH}/users/{user}" if user else f"{GRAPH}/me"


def headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# --- Supabase sender identification ----------------------------------------

def match_sender(ctx, email):
    """Classify a sender via the Supabase triage_match_sender RPC.

    Returns {"kind": "client"|"lead"|"unknown", "display_name": str|None,
    "status": str|None}. Uses the publishable key — the RPC is SECURITY DEFINER
    and only returns a classification, so no service-role secret is needed.
    A failed lookup degrades to "unknown" rather than aborting the whole run.
    """
    url = ctx.get("supabase_url")
    key = ctx.get("supabase_key")
    if not url or not key:
        sys.exit("ERROR: supabase_url and supabase_key are required in "
                 "triage-context.md for the identify step.")
    try:
        r = requests.post(
            f"{url}/rest/v1/rpc/triage_match_sender",
            headers={"apikey": key, "Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            data=json.dumps({"p_email": email}), timeout=30)
        if r.status_code != 200:
            print(f"WARN: identify lookup failed for {email}: "
                  f"{r.status_code} {r.text}")
            return {"kind": "unknown", "display_name": None, "status": None}
        rows = r.json()
    except requests.RequestException as exc:
        print(f"WARN: identify lookup error for {email}: {exc}")
        return {"kind": "unknown", "display_name": None, "status": None}
    if rows:
        row = rows[0]
        return {"kind": row.get("kind", "unknown"),
                "display_name": row.get("display_name"),
                "status": row.get("status")}
    return {"kind": "unknown", "display_name": None, "status": None}


def ensure_notifications_folder(ctx, token, base):
    """Resolve the Notifications mail folder id, creating it if missing."""
    name = ctx.get("notifications_folder", "Notifications")
    r = requests.get(f"{base}/mailFolders",
                     headers=headers(token),
                     params={"$filter": f"displayName eq '{name}'", "$top": "1"},
                     timeout=30)
    if r.status_code != 200:
        sys.exit(f"ERROR: folder lookup failed ({r.status_code}): {r.text}")
    found = r.json().get("value", [])
    if found:
        return found[0]["id"], name
    cr = requests.post(f"{base}/mailFolders",
                       headers=headers(token),
                       data=json.dumps({"displayName": name}),
                       timeout=30)
    if cr.status_code not in (200, 201):
        sys.exit(f"ERROR: folder create failed ({cr.status_code}): {cr.text}")
    return cr.json()["id"], name


# ---------------------------------------------------------------------------

def cmd_auth_check(ctx, args):
    token = get_token(ctx)
    base = mailbox_base(ctx)
    r = requests.get(f"{base}?$select=displayName,mail,userPrincipalName",
                     headers=headers(token), timeout=30)
    if r.status_code != 200:
        sys.exit(f"ERROR: auth check failed ({r.status_code}): {r.text}")
    info = r.json()
    print(f"OK — authenticated for: {info.get('displayName')} "
          f"<{info.get('mail') or info.get('userPrincipalName')}>")


def cmd_ensure_categories(ctx, args):
    token = get_token(ctx)
    base = mailbox_base(ctx)
    r = requests.get(f"{base}/outlook/masterCategories",
                     headers=headers(token), timeout=30)
    r.raise_for_status()
    existing = {c["displayName"] for c in r.json().get("value", [])}
    created = []
    for name, preset in CATEGORY_PRESETS.items():
        if name in existing:
            continue
        body = {"displayName": name, "color": preset}
        cr = requests.post(f"{base}/outlook/masterCategories",
                           headers=headers(token), data=json.dumps(body),
                           timeout=30)
        if cr.status_code in (200, 201):
            created.append(name)
        elif cr.status_code == 409:
            pass  # CategoryNameExists — already present (race or case), fine
        else:
            print(f"WARN: could not create '{name}': {cr.status_code} {cr.text}")
    if created:
        print(f"Created categories: {', '.join(created)}")
    else:
        print("All triage categories already present.")


def cmd_ensure_folder(ctx, args):
    token = get_token(ctx)
    base = mailbox_base(ctx)
    folder_id, name = ensure_notifications_folder(ctx, token, base)
    print(f"Notifications folder ready: '{name}' ({folder_id})")


def cmd_fetch(ctx, args):
    token = get_token(ctx)
    base = mailbox_base(ctx)
    RUN_DIR.mkdir(exist_ok=True)
    params = {
        "$filter": "isRead eq false",
        "$top": str(args.count),
        "$orderby": "receivedDateTime DESC",
        "$select": "id,subject,from,receivedDateTime,bodyPreview,"
                   "conversationId,webLink",
    }
    r = requests.get(f"{base}/mailFolders/Inbox/messages",
                     headers=headers(token), params=params, timeout=60)
    if r.status_code != 200:
        sys.exit(f"ERROR: fetch failed ({r.status_code}): {r.text}")
    msgs = r.json().get("value", [])
    out = RUN_DIR / "messages.json"
    out.write_text(json.dumps(msgs, indent=2))
    print(f"Fetched {len(msgs)} unread message(s) -> {out}")


def cmd_identify(ctx, args):
    """Annotate each fetched message's sender as client / lead / unknown."""
    src = RUN_DIR / "messages.json"
    if not src.exists():
        sys.exit(f"ERROR: {src} not found. Run `fetch` first.")
    msgs = json.loads(src.read_text())
    cache = {}  # email -> match result, so we only hit Supabase once per sender
    results = []
    for m in msgs:
        addr = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "")
        key = addr.lower().strip()
        if not key:
            info = {"kind": "unknown", "display_name": None, "status": None}
        else:
            if key not in cache:
                cache[key] = match_sender(ctx, addr)
            info = cache[key]
        results.append({
            "id": m.get("id"), "subject": m.get("subject"), "email": addr,
            "kind": info["kind"], "display_name": info["display_name"],
            "status": info["status"],
        })
    out = RUN_DIR / "identified.json"
    out.write_text(json.dumps(results, indent=2))
    n_client = sum(1 for r in results if r["kind"] == "client")
    n_lead = sum(1 for r in results if r["kind"] == "lead")
    n_unknown = len(results) - n_client - n_lead
    print(f"Identified {len(results)} sender(s): {n_client} client, "
          f"{n_lead} lead, {n_unknown} unknown -> {out}")


def set_categories_verified(token, base, msg_id, cats, label="message"):
    """PATCH a message's categories, then GET them back to confirm they stuck.

    Setting categories on a draft created via createReply can silently no-op on
    some mailboxes, so we read the value back and WARN loudly if the tag we
    intended (notably triage_draft) is missing — turning a silent failure into a
    visible one. Returns True if the read-back matches.
    """
    pr = requests.patch(f"{base}/messages/{msg_id}",
                        headers=headers(token),
                        data=json.dumps({"categories": cats}), timeout=30)
    if pr.status_code != 200:
        print(f"WARN: setting categories on {label} failed "
              f"({pr.status_code}): {pr.text}")
        return False
    vr = requests.get(f"{base}/messages/{msg_id}?$select=categories",
                      headers=headers(token), timeout=30)
    if vr.status_code != 200:
        print(f"WARN: could not verify {label} categories ({vr.status_code})")
        return False
    got = vr.json().get("categories", []) or []
    missing = [c for c in cats if c not in got]
    if missing:
        print(f"WARN: {label} categories did not stick — wanted {cats}, "
              f"got {got} (missing {missing}). The category may need to exist in "
              f"the mailbox master list first: run `ensure-categories`.")
        return False
    return True


def load_identity():
    """Map message id -> 'client'|'lead' from a prior identify run, if present."""
    idf = RUN_DIR / "identified.json"
    if not idf.exists():
        return {}
    out = {}
    for r in json.loads(idf.read_text()):
        kind = r.get("kind")
        if kind in IDENTITY_TAGS and r.get("id"):
            out[r["id"]] = kind
    return out


def cmd_apply(ctx, args):
    token = get_token(ctx)
    base = mailbox_base(ctx)
    items = json.loads(Path(args.input).read_text())
    identity = load_identity()
    label_cats = set(CATEGORY_PRESETS)
    ok, moved, fail = 0, 0, 0
    folder_id = None  # resolved lazily, only if a Notification item appears
    for it in items:
        cat = it["category"]
        if cat == NOTIFICATION_CATEGORY:
            if folder_id is None:
                folder_id, _ = ensure_notifications_folder(ctx, token, base)
            mr = requests.post(f"{base}/messages/{it['id']}/move",
                               headers=headers(token),
                               data=json.dumps({"destinationId": folder_id}),
                               timeout=30)
            if mr.status_code in (200, 201):
                moved += 1
            else:
                fail += 1
                print(f"WARN: move failed for {it.get('subject')}: "
                      f"{mr.status_code} {mr.text}")
            continue
        if cat not in label_cats:
            print(f"WARN: skipping unknown category '{cat}' for {it.get('subject')}")
            fail += 1
            continue
        # Triage category plus the sender identity tag (client/lead) if known.
        cats = [cat]
        tag = identity.get(it["id"])
        if tag and tag not in cats:
            cats.append(tag)
        body = {"categories": cats}  # full array recomputed each run — never stacks
        pr = requests.patch(f"{base}/messages/{it['id']}",
                            headers=headers(token), data=json.dumps(body),
                            timeout=30)
        if pr.status_code == 200:
            ok += 1
        else:
            fail += 1
            print(f"WARN: apply failed for {it.get('subject')}: "
                  f"{pr.status_code} {pr.text}")
    print(f"Applied categories: {ok} labelled, {moved} moved to Notifications, "
          f"{fail} failed.")


def cmd_draft(ctx, args):
    if getattr(args, "no_drafts", False):
        print("--no-drafts set: skipping draft creation for this message.")
        return
    token = get_token(ctx)
    base = mailbox_base(ctx)
    body_text = Path(args.body_file).read_text()
    # Create a reply draft threaded to the original, then patch in our body.
    cr = requests.post(f"{base}/messages/{args.message_id}/createReply",
                       headers=headers(token), timeout=30)
    if cr.status_code not in (200, 201):
        sys.exit(f"ERROR: createReply failed ({cr.status_code}): {cr.text}")
    draft_id = cr.json()["id"]
    ident_tag = load_identity().get(args.message_id)

    # 1) Set the draft body. Convert plain-text line breaks to HTML so the
    #    formatting survives.
    html = "<br>".join(body_text.split("\n"))
    pr = requests.patch(f"{base}/messages/{draft_id}",
                        headers=headers(token),
                        data=json.dumps({"body": {"contentType": "HTML",
                                                  "content": html}}),
                        timeout=30)
    if pr.status_code != 200:
        sys.exit(f"ERROR: draft body update failed ({pr.status_code}): {pr.text}")

    # 2) Tag the DRAFT (in the Drafts folder) with triage_draft + the sender
    #    identity. This is a SEPARATE PATCH from the body: a combined
    #    body+categories PATCH on a createReply draft can silently drop the
    #    categories, so we set them on their own and then verify.
    draft_cats = ["triage_draft"] + ([ident_tag] if ident_tag else [])
    set_categories_verified(token, base, draft_id, draft_cats, label="draft")

    # 3) Also mark the ORIGINAL inbox message triage_draft, so Scott can see at a
    #    glance which urgent items already have a draft waiting (preserving its
    #    Client-Urgent + identity tags).
    orig_cats = ["Client-Urgent", "triage_draft"] + ([ident_tag] if ident_tag else [])
    set_categories_verified(token, base, args.message_id, orig_cats,
                            label="inbox message")
    print(f"Draft created (unsent): {draft_id}; draft tagged {'+'.join(draft_cats)}, "
          f"inbox message tagged {'+'.join(orig_cats)}")


def main():
    ap = argparse.ArgumentParser(description="Outlook triage Graph helper")
    ap.add_argument("--context", default="triage-context.md")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth-check")
    sub.add_parser("ensure-categories")
    sub.add_parser("ensure-folder")
    sub.add_parser("identify")

    f = sub.add_parser("fetch")
    f.add_argument("--count", type=int, default=50)

    a = sub.add_parser("apply")
    a.add_argument("--input", required=True)

    d = sub.add_parser("draft")
    d.add_argument("--message-id", required=True)
    d.add_argument("--body-file", required=True)
    d.add_argument("--no-drafts", action="store_true",
                   help="Skip draft creation (used on re-runs to avoid duplicates).")

    args = ap.parse_args()
    ctx = load_context(args.context)

    dispatch = {
        "auth-check": cmd_auth_check,
        "ensure-categories": cmd_ensure_categories,
        "ensure-folder": cmd_ensure_folder,
        "identify": cmd_identify,
        "fetch": cmd_fetch,
        "apply": cmd_apply,
        "draft": cmd_draft,
    }
    dispatch[args.cmd](ctx, args)


if __name__ == "__main__":
    main()
