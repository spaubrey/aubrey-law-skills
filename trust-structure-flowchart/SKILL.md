---
name: trust-structure-flowchart
description: >
  Generates a branded, client-ready trust-structure flowchart (.pdf/.svg) for an
  Aubrey Law matter — a phased diagram of how a revocable trust works during
  lifetime(s), after the first spouse's death (marital/family split for joint
  plans), and after both grantors pass (pot trust then protected children's shares).
  Triggers on "create the trust flowchart for [client]", "trust structure diagram",
  "draw the trust flow", "flowchart for the [client] trust", or
  "/trust-structure-flowchart". Does NOT draft the trust documents (trust-drafting),
  funding/closing packages, or summaries — only the explanatory graphic.
---

# trust-structure-flowchart — Client-Ready Trust Diagram

You are generating a single branded flowchart that explains a client's revocable
trust structure in three phases. It is a teaching aid Scott sends to clients to
visualize how their plan works — not a legal instrument.

## Legal Compliance Guardrails

- **Draft for discussion only.** The footer must always state the chart is a draft
  for discussion. It is an explanatory aid, not legal advice.
- **Carry client-stated facts verbatim.** Trustee names, succession order, children's
  names, withdrawal ages, and trust labels come from the matter — never invent them.
- **Flag uncertainty.** If a name, age, or succession step is unclear from the source,
  insert a `[VERIFY: ...]` placeholder in the config value and call it out in your
  summary rather than guessing. Do NOT silently use plausible defaults for
  client-specific facts (names, ages, succession).
- **Generic structure is fine to default.** The boilerplate explanatory text
  (credit shelter / QTIP descriptions, asset-protection language) is the firm's
  standard and may be used as-is.

## Inputs You Need

Gather these before generating. Ask Scott for anything missing; do not fabricate
client-specific facts.

| Field | Required | Notes |
|-------|----------|-------|
| `matter_type` | yes | `"joint"` (married couple, two trusts) or `"individual"` |
| `matter_last` | yes | Used for the output filename |
| `title` | yes | e.g. "Olson Family Trust Structure" |
| `subtitle` | optional | Trust labels / plan type line under the title |
| `grantors.grantor1` (and `.grantor2` if joint) | yes | `name`, `trust_label`, `phase1_note` |
| `children` | yes | List of `{ "name": "..." }`; rendered as a responsive grid or summary box |
| `children_display` | optional (default `individual`) | `individual` = one box per child; `summary` = single box listing all; `auto` = summary once count ≥ `summary_threshold` |
| `summary_threshold` | optional (default 5) | Used only when `children_display` is `auto` |
| `common_trust_age` | optional (default 23) | Age below which the pot trust holds |
| `withdrawal_age` | optional (default 30) | Beneficiary withdrawal right age |
| `trustee_succession` | optional | Ordered list, e.g. `["survivor","Sarah","Charles"]` |
| `show_merge_option` | optional (default true) | Joint only: show "separate vs. merged" option |
| `firm_footer` | optional | Defaults to the standard Aubrey Law footer |

See `config.example.json` (joint) and `config.individual.example.json` (individual).

## Workflow

1. **Collect matter data.** Pull from the meeting note, design sheet, or `claude.md`
   in the matter folder. If drafting from a review meeting, the trustee succession
   and children's names usually appear there. Confirm anything ambiguous with Scott.
2. **Build the config JSON.** Write a `config.json` in the working directory using
   the schema above. Use real client names — replace any "Son 1 / Son 2" style
   placeholders with the actual children's names once confirmed.
3. **Generate.** From the skill folder:
   ```bash
   pip install cairosvg --break-system-packages -q   # first run only
   python3 generate_flowchart.py config.json
   ```
   This writes `<MatterLast>_Trust_Structure_Flowchart.svg` and `.pdf`.
4. **Verify the render.** Rasterize to PNG and visually inspect — confirm no arrows
   overlap text, the phase-transition labels are centered between arrows, and all
   names are correct:
   ```bash
   python3 -c "import cairosvg; cairosvg.svg2png(url='X.svg', write_to='_check.png', output_width=900)"
   ```
   Then delete the `_check.png` scratch file before presenting.
5. **Deliver.** Present the PDF (primary) and SVG (editable source). Note any
   `[VERIFY: ...]` placeholders that still need Scott's confirmation.

## Layout Logic (do not regress)

- **Joint matters** render the full three-phase chart: mirrored trusts → survivor
  as sole trustee with Family (credit shelter, excluded) and Marital (QTIP, included)
  shares → combine for children → pot trust → separate protected shares.
- **Individual matters** collapse to two phases (lifetime → distribution): there is
  no marital/family split because there is no surviving spouse, so the chart skips
  straight to the pot trust and children's shares.
- **Children display is configurable** via `children_display`:
  - `individual` (default): responsive grid — 1 centered, 2 side by side, 3 in a row
    of three, 4+ in a 2-column grid. Canvas height grows to fit extra rows.
  - `summary`: a single box ("Equal Separate Shares for the N Children") listing all
    names — cleaner for large sibling sets where per-child boxes add length without
    adding information.
  - `auto`: individual until the child count reaches `summary_threshold` (default 5),
    then summary.

## Integration with trust-drafting

`matter_to_config.py` bridges this skill to `trust-drafting`. After the trust
documents are generated, trust-drafting can build a `matter` dict from data it
already collected and call:

```bash
python3 matter_to_config.py matter.json
```

This derives trust labels, title, subtitle, and phase-1 notes automatically (e.g.
"Raj" + "Patel" → "RP Trust"), writes the chart to `/mnt/user-data/outputs/`, and
prints the derived config for review. See `INTEGRATION_trust-drafting.md` for the
drop-in Step 6 to paste into `trust-drafting/SKILL.md`. The flowchart's ages,
succession, and structure must match the executed trust terms.

## Critical Rendering Rules (learned the hard way)

These are enforced in `generate_flowchart.py`. If you edit the script, preserve them:

1. **No CSS `<style>` block — all styles inline.** cairosvg ignores `<style>`, which
   makes the PDF diverge from the SVG. Every color/size is an inline attribute.
2. **Pre-split caption lines.** Long single-line captions WRAP in real PDF viewers
   (PDFelement), shoving labels into arrows. Captions are written as explicit
   stacked `<text>` lines, never one long string.
3. **Arrows leave a clear gap** before the next box/heading; phase-transition labels
   ("first death", "second death") are centered between the two arrows.
4. **Description text is black** (`#000000`), headings navy, accent labels teal.

See `learnings.md` for the full history of these fixes.
