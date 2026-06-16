#!/usr/bin/env python3
"""
docuseal_upload.py — Upload a rendered .docx directly to DocuSeal via REST API.

The DocuSeal MCP `create_template` tool only accepts a public URL for the
file, which historically forced this skill through either a Make.com
SharePoint webhook OR a manual editor drag-and-drop. This script bypasses
that constraint by using DocuSeal's native `POST /templates/docx` endpoint,
which accepts the file as base64-encoded JSON.

The result is a fully automated upload: no Make, no SharePoint share links,
no manual editor step. Just one HTTPS POST from Scott's Mac.

Token resolution (in priority order):
  1. DOCUSEAL_API_TOKEN environment variable
  2. `docuseal_api_token: <value>` line in firm-context.md

The token is sensitive — never log it, never print it, never write it to
the output JSON.

Usage:
    python3 docuseal_upload.py \
        --file "/path/to/Engagement Agreement - Smith - 2026-05-22.docx" \
        --name "Engagement Agreement — Smith — 2026-05-22" \
        --token-from-context "/path/to/firm-context.md" \
        --out-json /tmp/upload_result.json

Output JSON (on success):
    {
      "ok": true,
      "template_id": 3789044,
      "template_name": "Engagement Agreement — Smith — 2026-05-22",
      "roles": ["Client", "Spouse"],
      "fields": [
        {"name": "Client Signature", "type": "signature", "role": "Client"},
        {"name": "Client Date",      "type": "date",      "role": "Client"},
        ...
      ],
      "edit_url": "https://docuseal.com/templates/3789044/edit"
    }

Output JSON (on failure):
    {
      "ok": false,
      "error": "HTTP 401: ...",
      "status": 401
    }
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DOCUSEAL_ENDPOINT = "https://api.docuseal.com/templates/docx"

# Placeholder values that should be treated as "not set."
_PLACEHOLDER_TOKENS = {
    "<paste token here>",
    "<paste docuseal token here>",
    "<paste>",
    "paste",
    "...",
    "",
}


def read_token_from_context(context_path: Path) -> str:
    """Parse firm-context.md for `docuseal_api_token: <value>`.

    Raises SystemExit if the field is missing or holds a placeholder.
    """
    if not context_path.exists():
        raise SystemExit(f"firm-context.md not found at {context_path}")
    text = context_path.read_text()
    m = re.search(r"docuseal_api_token:\s*(\S+)", text)
    if not m:
        raise SystemExit(
            "docuseal_api_token not found in firm-context.md. "
            "Add a line like `docuseal_api_token: <your-token>` under the "
            "DocuSeal section."
        )
    token = m.group(1).strip()
    if token.lower() in _PLACEHOLDER_TOKENS:
        raise SystemExit(
            "docuseal_api_token in firm-context.md is still a placeholder. "
            "Replace it with your real token from "
            "https://docuseal.com/settings/api"
        )
    return token


def upload(file_path: Path, name: str, token: str, timeout: int = 30) -> dict:
    """POST the .docx to DocuSeal. Returns either {ok: True, response: ...}
    or {ok: False, error: ..., status?: ...}.
    """
    if not file_path.exists():
        return {"ok": False, "error": f"file not found: {file_path}"}

    payload = json.dumps({
        "name": name,
        "documents": [{
            "name": file_path.stem,
            "file": base64.b64encode(file_path.read_bytes()).decode("ascii"),
        }],
    }).encode("utf-8")

    req = urllib.request.Request(
        DOCUSEAL_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Auth-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {"ok": True, "response": body}
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            err_body = ""
        return {"ok": False, "error": f"HTTP {e.code}: {err_body}", "status": e.code}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"network error: {e.reason}"}
    except TimeoutError:
        return {"ok": False, "error": f"timeout after {timeout}s"}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"response not valid JSON: {e}"}


def _resolve_role(field: dict, response: dict) -> str:
    """Map a field's submitter_uuid to the role name from response.submitters."""
    target = field.get("submitter_uuid")
    if not target:
        return ""
    for s in response.get("submitters", []):
        if s.get("uuid") == target:
            return s.get("name", "")
    return ""


def summarize(response: dict) -> dict:
    """Extract the bits SKILL.md Step 4c needs to validate against, plus a
    convenience edit_url. Designed to be small and reviewable in chat.
    """
    template_id = response.get("id")
    return {
        "ok": True,
        "template_id": template_id,
        "template_name": response.get("name"),
        "roles": [s.get("name") for s in response.get("submitters", []) if s.get("name")],
        "fields": [
            {
                "name": f.get("name"),
                "type": f.get("type"),
                "role": _resolve_role(f, response),
                "required": bool(f.get("required")),
            }
            for f in response.get("fields", [])
        ],
        "edit_url": (
            f"https://docuseal.com/templates/{template_id}/edit"
            if template_id else None
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", required=True, help="Path to the rendered .docx")
    p.add_argument("--name", required=True, help="DocuSeal template name")
    p.add_argument("--token-from-context",
                   help="Path to firm-context.md (reads docuseal_api_token). "
                        "Ignored if DOCUSEAL_API_TOKEN env var is set.")
    p.add_argument("--out-json", required=True,
                   help="Where to write the result JSON")
    p.add_argument("--timeout", type=int, default=30,
                   help="HTTP timeout in seconds (default 30)")
    args = p.parse_args()

    # Token resolution: env var wins for ad-hoc / testing; firm-context.md is
    # the production path.
    token = os.environ.get("DOCUSEAL_API_TOKEN", "").strip()
    if not token:
        if not args.token_from_context:
            raise SystemExit(
                "No DocuSeal API token: set DOCUSEAL_API_TOKEN env var, or "
                "pass --token-from-context pointing at firm-context.md."
            )
        token = read_token_from_context(Path(args.token_from_context))

    result = upload(Path(args.file), args.name, token, timeout=args.timeout)

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)

    if not result["ok"]:
        # Persist the error for the skill to surface; exit nonzero so the
        # caller can detect failure without parsing JSON.
        out.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    summary = summarize(result["response"])
    out.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
