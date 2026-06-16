#!/usr/bin/env python3
"""
Trust Structure Flowchart Generator — Aubrey Law LLC
=====================================================
Builds a phased revocable-trust structure flowchart (SVG + PDF) for any matter
from a JSON config. Mirrors the firm's branded style (Navy #1B3A6B, Teal #0F6E56,
Garamond, light-blue/green boxes).

USAGE
-----
    python3 generate_flowchart.py config.json [output_basename]

    - config.json      : matter-specific data (see config.example.json / schema in SKILL.md)
    - output_basename  : optional; defaults to "<MatterLast>_Trust_Structure_Flowchart"
                         Files are written to the current working directory.

DESIGN NOTES (learned the hard way — do not regress)
----------------------------------------------------
1. NO CSS <style> block. cairosvg ignores it, so the PDF diverges from the SVG.
   Every style is an INLINE attribute (fill=, font-size=, etc.).
2. Long caption lines WRAP in real PDF viewers (PDFelement), pushing labels into
   arrows. Captions are pre-split into explicit <text> lines — never one long line.
3. Arrows stop with a clear gap before the next box/heading; phase-transition
   labels ("first death", "second death") are centered between the two arrows.
4. The structure is data-driven but the *layout* is fixed (3 phases) because that
   is the firm's standard explainer. Joint vs. individual and merge options are
   toggled via config, not by moving geometry around.
"""

import json
import sys
import html
import os

NAVY = "#1B3A6B"
TEAL = "#0F6E56"
BOX_BLUE_FILL = "#EAF1F8"
BOX_GREEN_FILL = "#E3F0EB"
BLACK = "#000000"
GREY = "#999999"
FONT = "Garamond, Georgia, serif"


def esc(s):
    """XML-escape user-supplied strings."""
    return html.escape(str(s), quote=False)


def _wrap(s, width):
    """Greedy word-wrap into lines no longer than `width` chars."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def text(x, y, s, size=13, color=BLACK, weight="normal", italic=False, anchor="middle"):
    style = f' font-weight="{weight}"' if weight != "normal" else ""
    style += ' font-style="italic"' if italic else ""
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" '
            f'font-size="{size}"{style}>{esc(s)}</text>\n')


def box(x, y, w, h, fill, stroke):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>\n')


def arrow(x1, y1, x2, y2):
    return (f'  <path d="M{x1},{y1} L{x2},{y2}" stroke="{NAVY}" '
            f'stroke-width="2" fill="none" marker-end="url(#arrow)"/>\n')


def hline(y):
    return f'  <line x1="60" y1="{y}" x2="1040" y2="{y}" stroke="{TEAL}" stroke-width="1.5"/>\n'


def lines_block(x, y_start, lines, size=12, color=BLACK, italic=True, gap=18):
    """Render a list of caption lines as stacked centered <text> elements."""
    out = ""
    for i, ln in enumerate(lines):
        out += text(x, y_start + i * gap, ln, size=size, color=color, italic=italic)
    return out


def build_svg(cfg):
    g = cfg.get("grantors", {})
    g1 = g.get("grantor1", {})
    g2 = g.get("grantor2", {})
    is_joint = cfg.get("matter_type", "joint") == "joint"
    children = cfg.get("children", [])
    common_age = cfg.get("common_trust_age", 23)
    withdrawal_age = cfg.get("withdrawal_age", 30)
    succession = cfg.get("trustee_succession", [])
    merge_option = cfg.get("show_merge_option", True)
    firm = cfg.get("firm_footer",
                   "Draft for discussion — Aubrey Law LLC · 1329 Highland Ave Suite 1, Needham MA · (781) 474-3450")

    matter_title = cfg.get("title", "Trust Structure")

    s = (f'<svg viewBox="0 0 1100 1200" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="{FONT}">\n')
    s += '  <rect x="0" y="0" width="1100" height="1200" fill="#ffffff"/>\n'
    s += ('  <defs>\n'
          '    <marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" '
          'orient="auto" markerUnits="strokeWidth">\n'
          f'      <path d="M0,0 L8,3 L0,6 Z" fill="{NAVY}"/>\n'
          '    </marker>\n'
          '  </defs>\n')

    # ---- Title ----
    s += text(550, 38, matter_title, size=26, color=NAVY, weight="bold")
    sub = cfg.get("subtitle")
    if sub:
        s += text(550, 62, sub, size=12, color=BLACK, italic=True)

    # ================= PHASE 1 =================
    s += text(60, 105, "Phase 1 — During Both Lifetimes" if is_joint else "Phase 1 — During Lifetime",
              size=20, color=NAVY, weight="bold", anchor="start")
    s += hline(113)

    if is_joint:
        # Two mirrored trusts
        s += box(180, 130, 300, 92, BOX_BLUE_FILL, NAVY)
        s += text(330, 160, g1.get("trust_label", "Trust 1"), size=17, color=NAVY, weight="bold")
        s += text(330, 182, f"{g1.get('name','Grantor 1')} — Grantor & Trustee")
        s += text(330, 202, g1.get("phase1_note", "Fully revocable"))

        s += box(620, 130, 300, 92, BOX_BLUE_FILL, NAVY)
        s += text(770, 160, g2.get("trust_label", "Trust 2"), size=17, color=NAVY, weight="bold")
        s += text(770, 182, f"{g2.get('name','Grantor 2')} — Grantor & Trustee")
        s += text(770, 202, g2.get("phase1_note", "Fully revocable"))

        s += text(550, 172, "mirror", size=12, color=BLACK, italic=True)
        s += (f'  <line x1="480" y1="176" x2="620" y2="176" stroke="{GREY}" '
              f'stroke-width="1.5" stroke-dasharray="5,4"/>\n')

        s += text(550, 245, cfg.get("phase1_caption",
                                    "Each spouse keeps full control over their own trust while both are living."),
                  size=12, italic=True)
        s += arrow(330, 258, 330, 300)
        s += arrow(770, 258, 770, 300)
        s += text(345, 288, "first death", size=13, color=TEAL, weight="bold", anchor="start")
    else:
        # Single trust
        s += box(400, 130, 300, 92, BOX_BLUE_FILL, NAVY)
        s += text(550, 160, g1.get("trust_label", "Trust"), size=17, color=NAVY, weight="bold")
        s += text(550, 182, f"{g1.get('name','Grantor')} — Grantor & Trustee")
        s += text(550, 202, g1.get("phase1_note", "Fully revocable"))
        s += text(550, 245, cfg.get("phase1_caption",
                                    "Grantor keeps full control during lifetime."),
                  size=12, italic=True)
        s += arrow(550, 258, 550, 300)
        s += text(565, 288, "death", size=13, color=TEAL, weight="bold", anchor="start")

    # ================= PHASE 2 =================
    if is_joint:
        s += text(60, 320, "Phase 2 — After First Spouse's Death", size=20, color=NAVY, weight="bold", anchor="start")
        s += hline(328)

        s += box(300, 345, 500, 70, BOX_GREEN_FILL, TEAL)
        s += text(550, 375, "Surviving Spouse = Sole Trustee", size=17, color=TEAL, weight="bold")
        s += text(550, 397, "Deceased spouse's trust divides into two shares")

        s += arrow(470, 415, 400, 442)
        s += arrow(630, 415, 700, 442)

        # Family share
        s += box(120, 450, 360, 135, BOX_BLUE_FILL, NAVY)
        s += text(300, 478, "Family Trust Share", size=17, color=NAVY, weight="bold")
        s += text(300, 500, "(Credit Shelter / Bypass)")
        s += text(300, 524, "EXCLUDED from survivor's estate")
        s += text(300, 544, "Shelters assets from estate tax")
        s += text(300, 566, "Survivor may disclaim assets into here", italic=True)

        # Marital share
        s += box(620, 450, 360, 135, BOX_BLUE_FILL, NAVY)
        s += text(800, 478, "Marital Trust Share", size=17, color=NAVY, weight="bold")
        s += text(800, 500, "(QTIP — qualifies for marital deduction)")
        s += text(800, 524, "INCLUDED in survivor's estate")
        s += text(800, 544, "Defers tax to second death")
        s += text(800, 566, "Survivor benefits during lifetime", italic=True)

        s += lines_block(550, 610, [
            "Survivor decides asset allocation between shares for tax efficiency.",
            "Surviving spouse's own trust continues unchanged."
        ])
        s += arrow(300, 585, 300, 672)
        s += arrow(800, 585, 800, 672)
        s += text(550, 658, "second death", size=13, color=TEAL, weight="bold")

        phase3_title = "Phase 3 — After Both Spouses Pass"
        phase3_y = 700
    else:
        # Individual: no marital/family split; assets continue for beneficiaries
        phase3_title = "Phase 2 — Distribution to Beneficiaries"
        phase3_y = 360

    # ================= PHASE 3 (or 2 for individual) =================
    s += text(60, phase3_y, phase3_title, size=20, color=NAVY, weight="bold", anchor="start")
    s += hline(phase3_y + 8)

    combine_y = phase3_y + 25
    if is_joint:
        s += box(280, combine_y, 540, 64, BOX_GREEN_FILL, TEAL)
        s += text(550, combine_y + 28, "All shares combine for the children's benefit", size=17, color=TEAL, weight="bold")
        if merge_option:
            s += text(550, combine_y + 50, "Option 3A: kept as separate trusts  ·  Option 3B: merged into one trust")
        else:
            s += text(550, combine_y + 50, "Held for the children's benefit")
        pot_y = combine_y + 110
        s += arrow(550, combine_y + 64, 550, pot_y - 8)
    else:
        pot_y = combine_y

    # Common / pot trust
    s += box(300, pot_y, 500, 86, BOX_BLUE_FILL, NAVY)
    s += text(550, pot_y + 28, "Common Trust (Pot Trust)", size=17, color=NAVY, weight="bold")
    s += text(550, pot_y + 50, f"Used while any child is under {common_age}")
    s += text(550, pot_y + 70, "Trustee has discretion to meet each child's varying needs")

    # Split caption + arrows to children
    split_y = pot_y + 124
    s += text(550, split_y, f"Splits into equal separate shares once youngest reaches {common_age}", size=12, italic=True)
    child_box_y = pot_y + 137

    kids = children if children else [{"name": "Child 1"}]
    n = len(kids)

    # ---- Children display mode ----
    # "individual" (default) -> one box per child (responsive grid below)
    # "summary"              -> single box covering all children
    # "auto"                 -> individual up to summary_threshold, else summary
    display = cfg.get("children_display", "individual")
    threshold = cfg.get("summary_threshold", 5)
    if display == "auto":
        display = "summary" if n >= threshold else "individual"

    if display == "summary":
        # Single consolidated box for all children's shares
        BW, BH = 560, 130
        bx = 550 - BW / 2
        s += arrow(550, split_y + 7, 550, child_box_y - 6)
        s += box(bx, child_box_y, BW, BH, BOX_BLUE_FILL, NAVY)
        s += text(550, child_box_y + 30, f"Equal Separate Shares for the {n} Children",
                  size=17, color=NAVY, weight="bold")
        names = ", ".join(k.get("name", "Child") for k in kids)
        # Wrap the names line if long (~70 chars per line)
        name_lines = _wrap(names, 70)
        ny = child_box_y + 52
        for ln in name_lines[:2]:
            s += text(550, ny, ln, size=13)
            ny += 18
        s += text(550, child_box_y + 96, "Each share held in trust · asset-protected", size=13)
        s += text(550, child_box_y + 116, f"Withdrawal right at age {withdrawal_age}* · may remain in trust for protection",
                  size=12, italic=True)
        last_row_bottom = child_box_y + BH
    else:
        # ---- Responsive children grid ----
        # 1 child  -> centered
        # 2 children -> side by side (cols=2)
        # 3 children -> row of three (cols=3)
        # 4+ children -> 2-column grid
        if n == 1:
            cols = 1
        elif n == 2:
            cols = 2
        elif n == 3:
            cols = 3
        else:
            cols = 2

        BW = 360 if cols <= 2 else 300          # box width (narrower when 3 across)
        BH = 120
        ROW_GAP = 26
        canvas_w = 1100
        margin = 70
        usable = canvas_w - 2 * margin
        col_centers = [margin + usable * (c + 0.5) / cols for c in range(cols)]

        def child_box(cx, top, child):
            nm = child.get("name", "Child")
            out = box(cx - BW / 2, top, BW, BH, BOX_BLUE_FILL, NAVY)
            tsize = 17 if cols <= 2 else 15
            out += text(cx, top + 28, f"{nm} — Separate Share", size=tsize, color=NAVY, weight="bold")
            out += text(cx, top + 52, "Held in trust · asset-protected", size=13 if cols <= 2 else 12)
            out += text(cx, top + 74, f"Withdrawal right at age {withdrawal_age}*", size=13 if cols <= 2 else 12)
            out += text(cx, top + 98, "May leave in trust for divorce/creditor protection",
                        size=12 if cols <= 2 else 11, italic=True)
            return out

        # Connector arrows from the pot trust down to the first row of children
        first_row = kids[:cols]
        for idx, child in enumerate(first_row):
            cx = col_centers[idx]
            start_x = 550 + (cx - 550) * 0.25
            s += arrow(start_x, split_y + 7, cx, child_box_y - 6)

        last_row_bottom = child_box_y
        for r in range((n + cols - 1) // cols):
            row_top = child_box_y + r * (BH + ROW_GAP)
            last_row_bottom = row_top + BH
            for c in range(cols):
                i = r * cols + c
                if i >= n:
                    break
                s += child_box(col_centers[c], row_top, kids[i])

    # ---- Footnotes ----
    foot_y = last_row_bottom + 30
    s += text(550, foot_y, "*Withdrawal age can be raised (e.g., 50 or 60) for greater protection.", size=12, italic=True)
    nexty = foot_y + 20
    if succession:
        chain = " → ".join(succession)
        s += text(550, nexty, f"Trustee succession: {chain} (each serving solo).", size=12, italic=True)
        nexty += 20
    s += text(550, nexty + 10, firm, size=12, color=GREY, italic=True)

    total_h = nexty + 40
    s += '</svg>\n'
    # Patch dynamic height into the opening <svg> tag (viewBox + background rect)
    s = s.replace('viewBox="0 0 1100 1200"', f'viewBox="0 0 1100 {total_h}"', 1)
    s = s.replace('<rect x="0" y="0" width="1100" height="1200"',
                  f'<rect x="0" y="0" width="1100" height="{total_h}"', 1)
    return s


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_flowchart.py config.json [output_basename]")
        sys.exit(1)

    cfg_path = sys.argv[1]
    with open(cfg_path) as f:
        cfg = json.load(f)

    last = cfg.get("matter_last", "Matter")
    base = sys.argv[2] if len(sys.argv) > 2 else f"{last}_Trust_Structure_Flowchart"

    svg = build_svg(cfg)
    svg_path = f"{base}.svg"
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Wrote {svg_path}")

    # PDF (preferred for client delivery)
    try:
        import cairosvg
        pdf_path = f"{base}.pdf"
        cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
        print(f"Wrote {pdf_path}")
    except ImportError:
        print("cairosvg not installed — run: pip install cairosvg --break-system-packages")
        print("SVG written; convert separately if PDF is needed.")


if __name__ == "__main__":
    main()
