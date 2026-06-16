#!/usr/bin/env python3
"""
render_engagement.py — Generate a customized Aubrey Law estate planning
engagement agreement from inputs.

Usage:
    python3 render_engagement.py --inputs inputs.json --out path/to/output.docx

Inputs JSON schema (all fields required unless marked optional):
{
    "client_first_name": "John",
    "client_last_name": "Smith",
    "client_email": "john@example.com",
    "client_phone": "+15551234567",          # optional, E.164 format
    "couple": true,
    "spouse_first_name": "Jane",             # required if couple=true
    "spouse_last_name": "Smith",             # required if couple=true
    "spouse_email": "jane@example.com",      # required if couple=true
    "spouse_phone": "+15551234568",          # optional
    "trust_plan": true,
    "trust_type": "joint",                   # joint | separate | individual
    "deed": true,
    "legal_plan": false,
    "legal_plan_name": null,                 # required if legal_plan=true
    "flat_fee_amount": 5500,                 # required if legal_plan=false
    "credit_shelter": false
}

The script enforces all validation rules from references/template-fields.md
and raises a SystemExit with a structured error message if inputs are
invalid.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from docxtpl import DocxTemplate
except ImportError:
    print("ERROR: docxtpl not installed. Run: pip install docxtpl", file=sys.stderr)
    sys.exit(2)


TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "engagement_template.docx"


def normalize_plan_name(name: str) -> str:
    """Strip ' Legal' suffix from common plan names to avoid awkward output."""
    if not name:
        return name
    n = name.strip()
    if n.lower().endswith(" legal"):
        return n[: -len(" Legal")].rstrip()
    return n


def normalize_fee_amount(raw) -> str:
    """Accept int, float, or string. Return formatted '5,500' style."""
    if raw is None:
        return ""
    if isinstance(raw, (int, float)):
        n = int(raw) if raw == int(raw) else raw
    else:
        cleaned = str(raw).replace(",", "").replace("$", "").strip()
        try:
            n = int(cleaned) if cleaned.isdigit() else float(cleaned)
        except ValueError:
            raise ValueError(f"flat_fee_amount '{raw}' is not a number")
    if n <= 0:
        raise ValueError(f"flat_fee_amount must be positive (got {n})")
    if isinstance(n, int):
        return f"{n:,}"
    return f"{n:,.2f}"


def derive_trust_labels(trust_type: str, couple: bool) -> tuple[str, str]:
    """Return (trust_label, trust_label_lp) — see references/template-fields.md."""
    if trust_type == "joint":
        if not couple:
            raise ValueError("trust_type 'joint' requires couple=true")
        return "Joint Revocable Trust", "Joint Revocable Trust (No Tax Planning)"
    if trust_type == "separate":
        if not couple:
            raise ValueError("trust_type 'separate' requires couple=true")
        return (
            "Two Revocable Trusts (one per spouse)",
            "Two Revocable Trusts (No Tax Planning, one per spouse)",
        )
    if trust_type == "individual":
        if couple:
            raise ValueError("trust_type 'individual' implies a single client, but couple=true")
        return "Revocable Trust", "Revocable Trust (No Tax Planning)"
    raise ValueError(f"trust_type must be joint|separate|individual (got {trust_type!r})")


def validate_inputs(d: dict) -> list[str]:
    """Return a list of validation errors. Empty list means valid."""
    errors = []
    required = ["client_first_name", "client_last_name", "client_email", "couple",
                "trust_plan", "legal_plan"]
    for f in required:
        if d.get(f) in (None, ""):
            errors.append(f"missing required field: {f}")

    if d.get("couple"):
        for f in ["spouse_first_name", "spouse_last_name", "spouse_email"]:
            if d.get(f) in (None, ""):
                errors.append(f"missing required field for couple: {f}")

    if d.get("trust_plan") and not d.get("trust_type"):
        errors.append("missing required field: trust_type (because trust_plan=true)")

    if d.get("legal_plan"):
        if not d.get("legal_plan_name"):
            errors.append("missing required field: legal_plan_name (because legal_plan=true)")
        if d.get("credit_shelter") and not d.get("couple"):
            errors.append("credit_shelter only meaningful for couples — set credit_shelter=false or couple=true")
    else:
        if d.get("flat_fee_amount") in (None, ""):
            errors.append("missing required field: flat_fee_amount (because legal_plan=false)")

    # Email format sanity
    email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    for f in ["client_email", "spouse_email"]:
        v = d.get(f)
        if v and not email_re.match(v):
            errors.append(f"{f} is not a valid email: {v!r}")

    return errors


def build_render_context(d: dict) -> dict:
    """Translate inputs to template variables."""
    couple = bool(d["couple"])
    trust_plan = bool(d["trust_plan"])
    legal_plan = bool(d["legal_plan"])

    client_name = f"{d['client_first_name']} {d['client_last_name']}".strip()
    spouse_name = (
        f"{d['spouse_first_name']} {d['spouse_last_name']}".strip()
        if couple else ""
    )

    if trust_plan:
        trust_label, trust_label_lp = derive_trust_labels(d["trust_type"], couple)
    else:
        trust_label, trust_label_lp = "", ""

    return {
        "client_name": client_name,
        "spouse_name": spouse_name,
        "couple": couple,
        "trust_plan": trust_plan,
        "trust_label": trust_label,
        "trust_label_lp": trust_label_lp,
        "legal_plan": legal_plan,
        "legal_plan_name": normalize_plan_name(d.get("legal_plan_name", "")) if legal_plan else "",
        "deed": bool(d.get("deed", False)) and trust_plan,  # deed forced off when no trust
        "flat_fee_amount": normalize_fee_amount(d.get("flat_fee_amount")) if not legal_plan else "",
        "credit_shelter": bool(d.get("credit_shelter", False)) and legal_plan and couple,
    }


def render(inputs_path: Path, output_path: Path) -> dict:
    inputs = json.loads(inputs_path.read_text())
    errors = validate_inputs(inputs)
    if errors:
        return {"ok": False, "errors": errors}

    context = build_render_context(inputs)

    if not TEMPLATE_PATH.exists():
        return {"ok": False, "errors": [f"template missing at {TEMPLATE_PATH}"]}

    doc = DocxTemplate(str(TEMPLATE_PATH))
    doc.render(context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))

    return {"ok": True, "output": str(output_path), "context": context}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inputs", required=True, help="Path to inputs JSON")
    p.add_argument("--out", required=True, help="Path for output .docx")
    args = p.parse_args()

    result = render(Path(args.inputs), Path(args.out))
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
