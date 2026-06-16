#!/usr/bin/env python3
"""
send_engagement.py — Orchestrator helper for the send-estate-planning-engagement
skill. Handles:
  - Lead folder creation under OneDrive
  - File save (with collision-safe naming)
  - DocuSeal template name and submitter list construction

This script is intended to be called by Claude as part of the skill flow.
Claude calls the DocuSeal REST API directly via `scripts/docuseal_upload.py`
and then DocuSeal:load_template / DocuSeal:send_documents via MCP — this
script does NOT call those.

Usage:
    # After render_engagement.py has produced a .docx in a scratch path:
    python3 send_engagement.py prepare \
        --rendered /tmp/engagement_render.docx \
        --inputs /tmp/inputs.json \
        --out-json /tmp/send_plan.json

The output JSON includes:
  - final_path: where the .docx was saved in OneDrive
  - docuseal_template_name: e.g. "Engagement Agreement — Smith — 2026-05-19"
  - submitters: list of {role, name, email, phone} for DocuSeal:send_documents
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path


ONEDRIVE_ROOT = Path(
    "/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/"
    "Aubrey Law Clients/Estate Planning"
)


def build_lead_folder_name(inputs: dict, today: dt.date | None = None) -> str:
    """
    Lead folder name. Flat structure under Estate Planning/ (no year subfolder).
    Year is baked into the folder name itself.

      EP (flat fee):
        YYYY-EP-LastName, FirstName [& SpouseFirst | & SpouseFirst-SpouseLast]
        e.g. "2026-EP-Doe, John & Jane"

      EP-LP (legal insurance plan):
        YYYY-EP-LP-LastName, FirstName [& SpouseFirst | & SpouseFirst-SpouseLast]
        e.g. "2026-EP-LP-Smith, Sean & Sara"

    Both variants use "-" (dash) between the prefix and the last name. The
    only difference is whether the practice-area prefix is "EP" or "EP-LP".
    This matches Scott's existing OneDrive naming convention.
    """
    today = today or dt.date.today()
    year = today.year
    last = inputs["client_last_name"].strip()
    first = inputs["client_first_name"].strip()

    prefix = "EP-LP" if inputs.get("legal_plan") else "EP"
    base = f"{year}-{prefix}-{last}, {first}"

    if not inputs.get("couple"):
        return base
    s_first = inputs["spouse_first_name"].strip()
    s_last = inputs["spouse_last_name"].strip()
    if s_last and s_last.lower() != last.lower():
        return f"{base} & {s_first}-{s_last}"
    return f"{base} & {s_first}"


def build_filename(inputs: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    return f"Engagement Agreement - {inputs['client_last_name'].strip()} - {today.isoformat()}.docx"


def collision_safe(path: Path) -> Path:
    """If path exists, append -2, -3, ... before the .docx extension."""
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


def ensure_lead_folder(inputs: dict, today: dt.date | None = None) -> Path:
    """
    Create the lead folder directly under the Estate Planning root. The year
    is part of the lead folder name (e.g. "2026-EP-Doe, John & Jane"), so
    there is no intermediate year folder.
    """
    today = today or dt.date.today()
    if not ONEDRIVE_ROOT.exists():
        raise SystemExit(
            f"ERROR: OneDrive Estate Planning root not found at {ONEDRIVE_ROOT}.\n"
            "Check that OneDrive is mounted and the folder exists. The skill "
            "expects this exact path."
        )
    lead_folder = ONEDRIVE_ROOT / build_lead_folder_name(inputs, today=today)
    lead_folder.mkdir(parents=True, exist_ok=True)
    return lead_folder


def save_to_lead_folder(rendered: Path, inputs: dict, today: dt.date | None = None) -> Path:
    lead_folder = ensure_lead_folder(inputs, today=today)
    final_name = build_filename(inputs, today=today)
    final_path = collision_safe(lead_folder / final_name)
    shutil.copy2(rendered, final_path)
    return final_path


def build_docuseal_template_name(inputs: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    return f"Engagement Agreement — {inputs['client_last_name'].strip()} — {today.isoformat()}"


def build_submitters(inputs: dict) -> list[dict]:
    """Build the DocuSeal:send_documents submitters list."""
    client = {
        "role": "Client",
        "name": f"{inputs['client_first_name']} {inputs['client_last_name']}".strip(),
        "email": inputs["client_email"].strip(),
    }
    if inputs.get("client_phone"):
        client["phone"] = inputs["client_phone"].strip()
    out = [client]
    if inputs.get("couple"):
        spouse = {
            "role": "Spouse",
            "name": f"{inputs['spouse_first_name']} {inputs['spouse_last_name']}".strip(),
            "email": inputs["spouse_email"].strip(),
        }
        if inputs.get("spouse_phone"):
            spouse["phone"] = inputs["spouse_phone"].strip()
        out.append(spouse)
    return out


def cmd_prepare(args):
    inputs = json.loads(Path(args.inputs).read_text())

    final_path = save_to_lead_folder(Path(args.rendered), inputs)

    plan = {
        "final_path": str(final_path),
        "docuseal_template_name": build_docuseal_template_name(inputs),
        "submitters": build_submitters(inputs),
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(plan, indent=2))
    print(json.dumps(plan, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    prep = sub.add_parser("prepare", help="Save .docx to lead folder + build send plan")
    prep.add_argument("--rendered", required=True, help="Path to rendered .docx")
    prep.add_argument("--inputs", required=True, help="Path to inputs JSON used for the render")
    prep.add_argument("--out-json", required=True, help="Where to write the send plan JSON")
    prep.set_defaults(func=cmd_prepare)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
