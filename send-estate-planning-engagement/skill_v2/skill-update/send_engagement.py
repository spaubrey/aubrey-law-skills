#!/usr/bin/env python3
"""
send_engagement.py — Orchestrator helper for the send-estate-planning-engagement
skill. Handles:
  - Lead folder creation under OneDrive
  - File save (with collision-safe naming)
  - SharePoint share-link generation via Make.com webhook
  - SignWell API call to create and send document for signature

This script is intended to be called by Claude as part of the skill flow.

Usage:
    # Prepare: save to OneDrive + fetch share link
    python3 send_engagement.py prepare \
        --rendered /tmp/engagement_render.docx \
        --inputs /tmp/inputs.json \
        --webhook https://hook.us2.make.com/abc \
        --out-json /tmp/send_plan.json

    # Send via SignWell (URL path)
    python3 send_engagement.py send \
        --plan /tmp/send_plan.json \
        --api-key SW_KEY_HERE \
        --out-json /tmp/send_result.json

    # Send via SignWell (base64 fallback — no share URL needed)
    python3 send_engagement.py send \
        --plan /tmp/send_plan.json \
        --api-key SW_KEY_HERE \
        --use-base64 \
        --out-json /tmp/send_result.json

The send output JSON includes:
  - document_id: SignWell document ID
  - status: document status from SignWell
  - sign_urls: {name: url} per recipient
  - recipients: full recipient list from response
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import shutil
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# Default save location (host path). In a Cowork sandbox, pass --save-root
# with the mounted path for this folder instead.
SAVE_ROOT = Path(
    "/Users/aubreylawmacmini/Desktop/Claude Cowork Mini/"
    "Signwell Engagement Agreements"
)

SIGNWELL_API_BASE = "https://www.signwell.com/api/v1"


# ---------------------------------------------------------------------------
# Folder / file helpers (unchanged from original)
# ---------------------------------------------------------------------------

def build_filename(inputs: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    return f"Engagement Agreement - {inputs['client_last_name'].strip()} - {today.isoformat()}.docx"


def collision_safe(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    n = 2
    while True:
        candidate = parent / f"{stem}-{n}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def save_to_folder(rendered: Path, inputs: dict, save_root: Path,
                   today: dt.date | None = None) -> Path:
    if not save_root.exists():
        raise SystemExit(
            f"ERROR: Save folder not found at {save_root}.\n"
            "Connect/mount the Signwell Engagement Agreements folder, or pass "
            "--save-root with the correct path."
        )
    final_path = collision_safe(save_root / build_filename(inputs, today=today))
    shutil.copy2(rendered, final_path)
    return final_path


# ---------------------------------------------------------------------------
# Share-link helper (unchanged)
# ---------------------------------------------------------------------------

def fetch_share_link(webhook_url: str, file_path: Path, timeout: int = 15) -> dict:
    body = json.dumps({
        "file_path": str(file_path),
        "share_type": "view",
        "share_scope": "anonymous",
    }).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            if "share_url" not in data:
                return {"ok": False, "error": f"webhook returned no share_url: {raw[:200]}"}
            return {"ok": True, "share_url": data["share_url"],
                    "expires_at": data.get("expires_at")}
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return {"ok": False, "error": f"webhook request failed: {e}"}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"webhook response not valid JSON: {e}"}


# ---------------------------------------------------------------------------
# SignWell helpers
# ---------------------------------------------------------------------------

def build_document_name(inputs: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    return f"Engagement Agreement \u2014 {inputs['client_last_name'].strip()} \u2014 {today.isoformat()}"


def build_recipients(inputs: dict) -> list[dict]:
    """
    SignWell recipients list. Client is always signer 1, Spouse signer 2.
    Signer numbers in text tags must match this order.
    """
    client = {
        "id": "client",
        "name": f"{inputs['client_first_name']} {inputs['client_last_name']}".strip(),
        "email": inputs["client_email"].strip(),
        "placeholder_name": "Client",
    }
    out = [client]
    if inputs.get("couple"):
        spouse = {
            "id": "spouse",
            "name": f"{inputs['spouse_first_name']} {inputs['spouse_last_name']}".strip(),
            "email": inputs["spouse_email"].strip(),
            "placeholder_name": "Spouse",
        }
        out.append(spouse)
    return out


def signwell_send(
    api_key: str,
    document_name: str,
    file_name: str,
    recipients: list[dict],
    file_url: str | None = None,
    file_base64: str | None = None,
    test_mode: bool = False,
) -> dict:
    """
    POST to SignWell /api/v1/documents to create and send in one call.
    Provide either file_url or file_base64, not both.
    Returns parsed JSON response or raises SystemExit on error.
    """
    if not file_url and not file_base64:
        raise SystemExit("ERROR: must supply either file_url or file_base64")

    # SignWell requires the key "name" here (422 otherwise).
    file_entry: dict = {"name": file_name}
    if file_url:
        file_entry["file_url"] = file_url
    else:
        file_entry["file_base64"] = file_base64

    payload = {
        "test_mode": test_mode,
        "name": document_name,
        "subject": "Your Aubrey Law Engagement Agreement",
        "message": (
            "Please review and sign your estate planning engagement agreement "
            "at your earliest convenience. Let me know if you have any questions."
        ),
        "text_tags": True,
        "reminders": True,
        "apply_signing_order": False,
        "files": [file_entry],
        "recipients": recipients,
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{SIGNWELL_API_BASE}/documents",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"ERROR: SignWell API returned {e.code}: {error_body[:400]}"
        )
    except (urllib.error.URLError, TimeoutError) as e:
        raise SystemExit(f"ERROR: SignWell API request failed: {e}")


def extract_sign_urls(response: dict) -> dict:
    """Return {recipient_name: sign_url} from the SignWell response."""
    urls = {}
    for r in response.get("recipients", []):
        name = r.get("name", r.get("id", "Unknown"))
        url = r.get("sign_url")
        if url:
            urls[name] = url
    return urls


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_prepare(args):
    inputs = json.loads(Path(args.inputs).read_text())
    today = dt.date.today()

    final_path = save_to_folder(Path(args.rendered), inputs,
                                Path(args.save_root), today=today)

    if args.webhook:
        time.sleep(args.sync_wait)
        share_result = fetch_share_link(args.webhook, final_path, timeout=args.timeout)
    else:
        share_result = {"ok": False, "error": "no webhook URL provided"}

    plan = {
        "final_path": str(final_path),
        "file_name": Path(final_path).name,
        "share_link_ok": share_result["ok"],
        "share_url": share_result.get("share_url"),
        "share_link_error": share_result.get("error"),
        "document_name": build_document_name(inputs, today=today),
        "recipients": build_recipients(inputs),
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(plan, indent=2))
    print(json.dumps(plan, indent=2))


def cmd_send(args):
    plan = json.loads(Path(args.plan).read_text())

    file_url = None
    file_base64_str = None

    if args.use_base64 or not plan.get("share_link_ok"):
        # Base64 fallback: read the saved .docx directly
        docx_path = Path(plan["final_path"])
        if not docx_path.exists():
            raise SystemExit(f"ERROR: .docx not found at {docx_path}")
        file_base64_str = base64.b64encode(docx_path.read_bytes()).decode("ascii")
        print(f"Using base64 upload from {docx_path}", file=sys.stderr)
    else:
        file_url = plan["share_url"]
        print(f"Using SharePoint URL: {file_url}", file=sys.stderr)

    response = signwell_send(
        api_key=args.api_key,
        document_name=plan["document_name"],
        file_name=plan["file_name"],
        recipients=plan["recipients"],
        file_url=file_url,
        file_base64=file_base64_str,
        test_mode=args.test_mode,
    )

    sign_urls = extract_sign_urls(response)

    result = {
        "document_id": response.get("id"),
        "status": response.get("status"),
        "document_name": response.get("name"),
        "sign_urls": sign_urls,
        "recipients": response.get("recipients", []),
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    # prepare subcommand
    prep = sub.add_parser("prepare", help="Save .docx to OneDrive + fetch share link")
    prep.add_argument("--rendered", required=True, help="Path to rendered .docx")
    prep.add_argument("--inputs", required=True, help="Path to inputs JSON")
    prep.add_argument("--webhook", default="", help="Make.com share-link webhook URL")
    prep.add_argument("--out-json", required=True, help="Where to write the send plan JSON")
    prep.add_argument("--save-root", default=str(SAVE_ROOT),
                      help="Folder to save the engagement .docx into")
    prep.add_argument("--sync-wait", type=int, default=0, help="Seconds to wait before webhook (legacy)")
    prep.add_argument("--timeout", type=int, default=15, help="Webhook timeout in seconds")
    prep.set_defaults(func=cmd_prepare)

    # send subcommand
    send = sub.add_parser("send", help="Send document via SignWell API")
    send.add_argument("--plan", required=True, help="Path to send plan JSON from prepare step")
    send.add_argument("--api-key", required=True, help="SignWell API key")
    send.add_argument("--use-base64", action="store_true",
                      help="Force base64 upload even if share URL is available")
    send.add_argument("--test-mode", action="store_true",
                      help="Send in test mode (does not count toward billing)")
    send.add_argument("--out-json", required=True, help="Where to write the result JSON")
    send.set_defaults(func=cmd_send)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
