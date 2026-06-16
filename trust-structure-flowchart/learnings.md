# learnings — trust-structure-flowchart

Accumulated fixes. Apply these on every run; do not regress them.

## Rendering / PDF fidelity

- **cairosvg ignores `<style>` CSS blocks.** Class-based styling rendered fine in the
  SVG preview but the exported PDF came out unstyled (wrong colors, default fills).
  Fix: every style is an inline attribute (`fill=`, `font-size=`, `font-weight=`,
  `font-style=`). No `<style>` block anywhere.

- **Long caption lines wrap in real viewers.** A single `<text>` line of
  "Survivor decides asset allocation… continues unchanged." rendered on one line in
  the quick preview but wrapped to TWO lines in PDFelement, which pushed the
  "second death" label down into the arrowheads. Fix: captions are pre-split into
  explicit stacked `<text>` lines via `lines_block()`. Never emit a long caption as
  one element.

- **Arrow lengths and label centering.** Arrows must stop with a visible gap before
  the next box or phase heading, or the arrowhead collides with text. Phase-transition
  labels ("first death", "second death") are centered at x=550 between the two
  vertical arrows (x=300 and x=800), not offset to one side.

- **Always rasterize to PNG and eyeball the result** before delivering. The PDF is
  the source of truth, not the inline SVG preview — they can differ (see above).

## Content

- **Replace placeholder child names.** First Olson draft used "Son 1 / Son 2". Always
  swap in real names once confirmed; flag with `[VERIFY: ...]` if unknown.
- **Trustee succession came from the meeting note** (survivor → Sarah → Charles →
  Jeffrey). Confirm with Scott — meeting-note OCR/auto-summary names are not reliable
  enough to ship unverified.
- **Black description text** was an explicit request — headings navy, body black,
  accent labels teal.

## Layout variants

- Joint = 3 phases with marital/family split. Individual = 2 phases, skips the split
  (no surviving spouse), goes lifetime → pot trust → children's shares.
- **Children grid is responsive** (added after initial build): 1 centered, 2 side by
  side, 3 in a row of three with narrower boxes, 4+ in a 2-column grid. The SVG
  `viewBox` height and background rect are patched dynamically at the end of
  `build_svg()` so the canvas grows to fit extra rows and footnotes stay anchored
  below the last child row. Do not hard-code height back to 1200.
- **`children_display` toggle** (added later): `individual` (per-child boxes, default),
  `summary` (one consolidated box listing all names — best for large sibling sets),
  or `auto` (summary once count ≥ `summary_threshold`, default 5). The summary box
  word-wraps the names line via `_wrap()`. Bridge passes the toggle through.
- `matter_to_config.py` derives the flowchart config from a trust-drafting matter
  object (trust labels from initials, title/subtitle/captions auto-built) so the two
  skills share one data entry. Keep ages/succession/structure in sync with the
  executed trust terms — regenerate the chart if terms change.
