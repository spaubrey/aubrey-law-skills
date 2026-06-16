# Script Setup and Run Guide

## Script Locations

The two templates live directly in the skill folder:

```
skills/pmps-proposal/
├── pmps-proposal.js            ← Estate Plan Proposal template
├── pmps-one-page-summary.js    ← One-Page Plan Summary template
├── assets/
│   └── aubrey-law-logo.png     ← Header logo
└── node_modules/               ← docx library (pre-installed)
```

In the VM/bash environment, the workspace maps to:
`/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/`

So the scripts are at:
`/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/skills/pmps-proposal/`

---

## Step A: Ensure _shared.js Is Present

Both templates require `_shared.js` in the same directory. Check first:

```bash
ls "/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/skills/pmps-proposal/_shared.js"
```

**If missing**, copy from the pmps-prep-skill folder and patch the logo path:

```bash
SKILL_DIR="/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/skills/pmps-proposal"
SRC="/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/skills/pmps-prep-skill/pmps-prep/Templates/_shared.js"

cp "$SRC" "$SKILL_DIR/_shared.js"

# Patch LOGO_PATH: the pmps-proposal assets/ is at the same level as _shared.js
# Original: path.join(__dirname, '..', 'assets', 'aubrey-law-logo.png')
# Correct:  path.join(__dirname, 'assets', 'aubrey-law-logo.png')
sed -i "s|path.join(__dirname, '..', 'assets', 'aubrey-law-logo.png')|path.join(__dirname, 'assets', 'aubrey-law-logo.png')|g" "$SKILL_DIR/_shared.js"

echo "✓ _shared.js ready"
```

**If already present**, skip this step — no need to re-copy.

---

## Step B: Create Output Directory

```bash
CLIENT="Smith"  # Use the client's last name or filePrefix
OUT_DIR="/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/OUTPUTS/${CLIENT}_Proposal"
mkdir -p "$OUT_DIR"
echo "Output directory: $OUT_DIR"
```

Note: `data.matter.outputDir` must use the **workspace path** (as seen by file tools):
`/Users/scottaubrey/Desktop/Aubrey Law Cowork/OUTPUTS/${CLIENT}_Proposal/`

---

## Step C: Write and Run the Runner Script

Create a runner.js in the outputs folder, then execute it:

```javascript
// runner.js — place in /tmp/ or outputs folder, then run with node
'use strict';
const path = require('path');
const SKILL = "/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/skills/pmps-proposal";
const OUT   = "/sessions/busy-awesome-babbage/mnt/Aubrey Law Cowork/OUTPUTS/Smith_Proposal";

const data = {
  matter: {
    date: "May 12, 2026",
    filePrefix: "Smith",
    outputDir: OUT
  },
  // ... full data object here
};

Promise.all([
  require(path.join(SKILL, "pmps-proposal.js"))(data),
  require(path.join(SKILL, "pmps-one-page-summary.js"))(data)
]).then(() => {
  console.log("✓ Both documents generated");
}).catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
```

Run it:
```bash
node /tmp/runner.js
```

---

## Step D: Verify Output

```bash
ls -la "$OUT_DIR"
# Should show:
# Smith_Proposal.docx
# Smith_OnePager.docx
```

If only one file appears, check for errors in the node output. Common issues:
- `_shared.js` not found → run Step A
- Logo path error → verify assets/ folder exists in skill directory
- `Cannot find module 'docx'` → verify node_modules/ is present in skill folder

---

## Output File Names

The templates name files using `data.matter.filePrefix`:
- Proposal: `{filePrefix}_Proposal.docx`
- One-Pager: `{filePrefix}_OnePager.docx`

Set `filePrefix` to the client's last name or the standard matter identifier used
for the client's folder (e.g., `"Smith"`, `"Miller-Chen"`, `"OBrien"`).
