#!/usr/bin/env python3
"""
matter_to_config.py — bridge for trust-drafting (and other skills)
==================================================================
Converts a trust-drafting style matter/client data object into a
trust-structure-flowchart config dict, then (optionally) generates the chart.

This lets trust-drafting produce the explainer flowchart automatically from the
same data it already collected, with no duplicate data entry.

USAGE (from another skill or a wrapper script)
----------------------------------------------
    from matter_to_config import build_config, generate

    cfg = build_config(matter)        # matter = trust-drafting data dict
    generate(cfg)                     # writes <Last>_Trust_Structure_Flowchart.{svg,pdf}

Or standalone, reading a matter JSON:
    python3 matter_to_config.py matter.json

EXPECTED matter FIELDS (all optional; sensible fallbacks applied)
-----------------------------------------------------------------
    matter_type            "joint" | "individual"   (inferred from spouse if absent)
    last_name / family     -> matter_last + title
    grantor1: { first, last, trust_label }           OR  client_first/client_last
    grantor2: { first, last, trust_label }           OR  spouse_first/spouse_last
    children: [ { name }, ... ]  OR  list of strings
    common_trust_age, withdrawal_age
    trustee_succession: [ ... ]
    show_merge_option
"""

import json
import sys
import os


def _initials_trust_label(first, last):
    fi = (first or "").strip()[:1].upper()
    li = (last or "").strip()[:1].upper()
    return f"{fi}{li} Trust" if (fi or li) else "Trust"


def _norm_children(children):
    out = []
    for c in (children or []):
        if isinstance(c, str):
            out.append({"name": c})
        elif isinstance(c, dict):
            nm = c.get("name") or " ".join(
                x for x in [c.get("first"), c.get("last")] if x
            ).strip()
            out.append({"name": nm or "Child"})
    return out


def build_config(matter):
    """Map a trust-drafting matter dict to a flowchart config dict."""
    m = matter or {}

    # --- Grantors ---
    g1 = m.get("grantor1") or {}
    g2 = m.get("grantor2") or {}

    g1_first = g1.get("first") or m.get("client_first") or m.get("client_first_name")
    g1_last = g1.get("last") or m.get("client_last") or m.get("last_name") or m.get("family")
    g2_first = g2.get("first") or m.get("spouse_first") or m.get("spouse_first_name")
    g2_last = g2.get("last") or m.get("spouse_last") or m.get("last_name") or m.get("family")

    has_spouse = bool(g2_first or g2_last or m.get("spouse_full_name"))
    matter_type = m.get("matter_type") or ("joint" if has_spouse else "individual")

    family = m.get("family") or m.get("last_name") or g1_last or "Matter"

    cfg = {
        "matter_type": matter_type,
        "matter_last": family,
        "common_trust_age": m.get("common_trust_age", 23),
        "withdrawal_age": m.get("withdrawal_age", 30),
        "show_merge_option": m.get("show_merge_option", True),
        "trustee_succession": m.get("trustee_succession", []),
        "children": _norm_children(m.get("children")),
        "children_display": m.get("children_display", "individual"),
        "summary_threshold": m.get("summary_threshold", 5),
        "firm_footer": m.get(
            "firm_footer",
            "Draft for discussion — Aubrey Law LLC · 1329 Highland Ave Suite 1, Needham MA · (781) 474-3450",
        ),
    }

    g1_label = g1.get("trust_label") or _initials_trust_label(g1_first, g1_last)
    cfg["grantors"] = {
        "grantor1": {
            "name": g1_first or "Grantor",
            "trust_label": g1_label,
            "phase1_note": f"Fully revocable · {g1_first}'s assets" if g1_first else "Fully revocable",
        }
    }

    if matter_type == "joint":
        g2_label = g2.get("trust_label") or _initials_trust_label(g2_first, g2_last)
        cfg["grantors"]["grantor2"] = {
            "name": g2_first or "Grantor 2",
            "trust_label": g2_label,
            "phase1_note": f"Fully revocable · {g2_first}'s assets" if g2_first else "Fully revocable",
        }
        cfg["title"] = m.get("title") or f"{family} Family Trust Structure"
        sub_bits = []
        if g1_first and g1_last:
            sub_bits.append(f"{g1_first} {g1_last} ({g1_label})")
        if g2_first and g2_last:
            sub_bits.append(f"{g2_first} {g2_last} ({g2_label})")
        if sub_bits:
            cfg["subtitle"] = " & ".join(sub_bits) + " — Separate Mirrored Trusts"
        cfg["phase1_caption"] = "Each spouse keeps full control over their own trust while both are living."
    else:
        cfg["title"] = m.get("title") or f"{family} Trust Structure"
        if g1_first and g1_last:
            cfg["subtitle"] = f"{g1_first} {g1_last} Revocable Trust — Individual Plan"
        cfg["phase1_caption"] = f"{g1_first or 'The grantor'} keeps full control of the trust during life."

    return cfg


def generate(cfg, basename=None, outdir="."):
    """Write config + generate the flowchart using generate_flowchart.build_svg."""
    # Import the generator from the same skill folder
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from generate_flowchart import build_svg

    last = cfg.get("matter_last", "Matter")
    base = basename or f"{last}_Trust_Structure_Flowchart"
    base = os.path.join(outdir, base)

    svg = build_svg(cfg)
    with open(f"{base}.svg", "w") as f:
        f.write(svg)
    try:
        import cairosvg
        cairosvg.svg2pdf(url=f"{base}.svg", write_to=f"{base}.pdf")
        return f"{base}.svg", f"{base}.pdf"
    except ImportError:
        return f"{base}.svg", None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 matter_to_config.py matter.json")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        matter = json.load(f)
    cfg = build_config(matter)
    svg, pdf = generate(cfg, outdir="/mnt/user-data/outputs")
    print(f"Wrote {svg}" + (f" and {pdf}" if pdf else ""))
    # Echo the derived config so the caller can eyeball the mapping
    print(json.dumps(cfg, indent=2))
