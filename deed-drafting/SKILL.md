---
name: deed-drafting
description: >
  Drafts a Massachusetts Quitclaim Deed transferring real property to a trust, using an uploaded
  deed (PDF or Word) as the source. Use this skill whenever Scott uploads a deed and wants to
  produce a draft transfer deed — including phrases like "draft a deed from the uploaded deed",
  "create a deed to transfer property to the trust", "populate the deed template", "draft a
  quitclaim deed", "draft a realty trust deed", "transfer to a realty trust", or any request
  involving an uploaded deed file and a transfer to a trust. Always use this skill when a deed
  document is uploaded and Scott wants a new deed produced from it, even if the request is casual
  like "make a deed from this" or "fill out the deed template using this deed." Also triggers when
  Scott asks to draft a Realty Trust alongside or instead of a deed transfer.
---

# Deed Drafting Skill — Aubrey Law

## Purpose

This skill extracts property and party information from a client's current deed and uses it to
populate the Aubrey Law Quitclaim Deed template, producing a ready-to-review draft deed that
transfers the property to a trust.

This skill also optionally generates a **Massachusetts Realty Trust** (Declaration of Trust +
Schedule of Beneficial Interests) as a companion to the deed. When a Realty Trust is created,
the **Realty Trust is the Grantee on the deed** — not the underlying revocable living trust(s).

Bundled templates:
- `assets/Cowork Deed Template_v01.docx` — Quitclaim Deed
- `assets/Realty_Trust_Template.docx` — Realty Trust Declaration + Schedule
- `assets/Trustees Certificate Template.docx` — Trustee's Certificate (M.G.L. c. 184 § 35)

Use these bundled files as the base for every document. Do not build from scratch.

A complete Realty Trust transfer bundle therefore has **three** documents:
1. Quitclaim Deed (Step 2)
2. Trustee's Certificate (Step 2b) — required for recording alongside the deed under M.G.L. c. 184 § 35
3. Realty Trust Declaration + Schedule (Step 3)

When a transfer is made directly to a living trust (no Realty Trust), the bundle is the deed
and the Trustee's Certificate; the Realty Trust step is skipped.

---

## Step 0 — Confirm Details Before Starting

Before extracting anything from the deed, ask Scott the following (use AskUserQuestion tool):

1. **What is the full name of the trust?** (e.g., "TREACY REALTY TRUST" — used in ALL CAPS)
2. **Who are the trustees?** Confirm whether the grantors on the uploaded deed are themselves
   the trustees, or whether different people will serve. In most cases they are the same people.
3. **Should a Realty Trust be drafted in addition to the deed?** (Yes / No)
   - If **Yes**: **Is this a joint trust or separate trusts (one per spouse)?**
     - *Joint trust*: One joint revocable living trust holds **100%** of beneficial interest.
     - *Separate trusts*: Client's trust holds **50%**, spouse's trust holds **50%**.
   - If **Yes**: Confirm the **full names of both living trusts** (needed for the Schedule).

Do not proceed until Scott has confirmed all answers.

---

## Template Structure — Deed

See the deed template at `assets/Cowork Deed Template_v01.docx`.

The template is US Letter (1-inch top/bottom, 0.75-inch left/right margins), Garamond font:

**Page 1:**
- Centered bold: `QUITCLAIM DEED`
- Grantor/grantee block
- Floating text box: `PROPERTY ADDRESS: [ADDRESS]` — **leave completely untouched** (Relaw.ai field)
- `with Quitclaim Covenants,`
- `[Property Description]`
- Metes-and-bounds rows: `[Directional Call 1]  [Bound Description 1]` through Call 6
- `[DESCRIPTION 2]`
- `Meaning and intending to convey the same premises of Grantors' deed recorded on [Recording Date of Current Deed], and filed in the [Registry of Deeds] in Book [Current Deed Book Number], Page [Current Deed Page].`
- `Property Address: [street address]` (added just before the page break)
- Centered: `[SIGNATURES ON NEXT PAGE]` + page break

**Page 2 (Signature page):**
- `Witness our hands and seals this _____ day of ________________.`
- Signature table: `[GRANTOR]` (left) | `[GRANTOR 2]` (right) — borderless table
- Notary block referencing both grantors

> **Important:** The recording reference placeholder in the template XML reads
> `[Recording Date of Current Deed]` — use that exact text in find-replace.

---

## Template Structure — Realty Trust

See the Realty Trust template at `assets/Realty_Trust_Template.docx`.

The template has **two sections** in one file:

### Section 1: Declaration of Trust

Key placeholders:

| Placeholder | What to Insert |
|---|---|
| `[REALTY TRUST]` | Realty Trust name in ALL CAPS (e.g., `TREACY REALTY TRUST`) |
| `[CLIENT]` | First trustee's full legal name |
| `[SPOUSE]` | Second trustee's full legal name |
| `[Ordinal Execution Date]` | Blank fill-in line: `________________________` |
| `[DocDate]` (in notary block) | Blank fill-in line: `________________________` |
| `[RETRUSTEE]` | First trustee's full name (notary acknowledgment) |
| `[COTRUSTEE]` | Second trustee's full name (notary acknowledgment) |
| `[SIGNING COUNTY]` | Blank fill-in line: `________________________` |
| Notary Commission | Blank fill-in line: `________________________` |

### Section 2: Schedule of Beneficial Interests and Agreement

Key placeholders:

| Placeholder | What to Insert |
|---|---|
| `[REALTY TRUST]` | Realty Trust name in ALL CAPS |
| `[DocDate]` (Schedule date) | Blank fill-in line: `________________________` |
| `[DocDate]` (Declaration date reference) | Blank fill-in line: `________________________` |
| Beneficiary row(s) | See ownership rules below |
| `[CLIENT]` | First trustee's full name |
| `[SPOUSE]` | Second trustee's full name |
| `[Joint Trust/Client Trust]` | Living trust name(s) per ownership structure |
| `[Spouse Trust]` | Spouse's living trust name (separate trusts only) |
| `[Ordinal Execution Date]` | Blank fill-in line: `________________________` |
| `[SINGING COUNTY]` (sic) | Blank fill-in line: `________________________` |
| `DOCDATE` (notary block) | Blank fill-in line: `________________________` |
| Notary Commission | Blank fill-in line: `________________________` |

---

## Step 1 — Extract Information from the Uploaded Deed

Read the uploaded deed and extract:

| Template Placeholder | What to Extract |
|---|---|
| `[GRANTOR]` | First grantor's full legal name (ALL CAPS) |
| `[GRANTOR 2]` | Second grantor's full legal name (ALL CAPS). If only one grantor, delete everywhere — body, signature table, notary block — and remove orphaned "and"/punctuation. |
| Trustees | Confirmed in Step 0; usually same as grantors |
| `[TRUST NAME]` | Confirmed in Step 0, ALL CAPS |
| `[DocDate]` | Replace with blank fill-in line: `________________________` |
| `[Property Description]` | Opening description paragraph |
| `[Directional Call 1–6]` / `[Bound Description 1–6]` | Metes-and-bounds calls. Add rows if >6; delete unused rows. |
| `[DESCRIPTION 2]` | Second description paragraph (easements, etc.). Delete if none. |
| `[Recording Date of Current Deed]` | Date deed was recorded at registry |
| `[Registry of Deeds]` | Full registry name |
| `[Current Deed Book Number]` | Book number |
| `[Current Deed Page]` | Page number |
| `ADDRESS` (grantee block) | Grantee mailing address (usually same as property) |
| Property Address paragraph | Street address (plain paragraph before `[SIGNATURES ON NEXT PAGE]`) |

**Lot/plan deeds:** Place full description in `[Property Description]`; delete all directional
call and bound description rows.

**Registered land:** Adapt "Meaning and intending" to reference Document No. and Certificate
of Title instead of Book/Page.

---

## Step 2 — Populate the Deed Template

Use the `docx` skill to unpack, find-replace, and repack `assets/Cowork Deed Template_v01.docx`.

### Grantee Clause — No Realty Trust

> **[GRANTOR] and [GRANTOR 2]**, ("Grantors"), for full consideration of
> ONE DOLLAR ($1.00), grant to **[TRUSTEE] and [CO-TRUSTEE]**, Trustees of the
> **[TRUST NAME ALL CAPS]** u/a dated ________________________, as evidenced by a Certificate
> of Trustees pursuant to M.G.L. c. 184, §35, recorded herewith, having a mailing address at
> [grantee address] ("Grantee"),

### Grantee Clause — With Realty Trust

When a Realty Trust is drafted, **the Realty Trust is the Grantee**. The living trust(s) do
not appear on the deed — they appear only in the Schedule of Beneficial Interests.

> **[GRANTOR] and [GRANTOR 2]**, ("Grantors"), for full consideration of
> ONE DOLLAR ($1.00), grant to **[TRUSTEE] and [CO-TRUSTEE]**, Trustees of the
> **[REALTY TRUST NAME ALL CAPS]** u/a dated ________________________, as evidenced by a
> Certificate of Trustees pursuant to M.G.L. c. 184, §35, recorded herewith, having a mailing
> address at [grantee address] ("Grantee"),

After substitution, verify no `[BRACKETS]` remain except intentional blank fill-in lines.

---

## Step 2b — Populate the Trustee's Certificate

Open `assets/Trustees Certificate Template.docx` and apply the substitutions below. The
certificate reuses the trust and trustee information already gathered in Step 0 and Step 1, so no
new client data is required — only the values you've already confirmed.

Use the `docx` skill to unpack, find-replace, and repack. The certificate has no placeholders
in its footers, so only `word/document.xml` needs substitution.

> **Which trust name to use:** If a Realty Trust is being created, the Trustee's Certificate is
> for the **Realty Trust** (the grantee on the deed). If no Realty Trust is involved, the
> certificate is for the underlying revocable living trust named as grantee.

### Header block

| Placeholder | Value |
|---|---|
| `[DEED GRANTEE]` (Name of Trust row) | Trust name in ALL CAPS (e.g., `TREACY REALTY TRUST`) |
| `[DATE]` (Dated row) | Blank fill-in line: `________________________` (Scott will write in the trust agreement date at signing) |
| `[ADDRESS]` (Address row) | Mailing address of the trustees — same address used in the deed's grantee clause |

### Body paragraphs

| Placeholder | Value |
|---|---|
| `[I][We]` | Use `We` if there are two trustees; `I` if a single trustee. Delete the bracketed alternative entirely. |
| `[is][are]` | Use `are` for two trustees; `is` for one. |
| `[GRANTEE TRUSTEE]` | First trustee's full legal name (mixed case — match how it appears in the trust, e.g., "John P. Treacy"). |
| `[GRANTEE COTRUSTEE]` | Second trustee's full legal name. If only one trustee, delete this placeholder **everywhere it appears** along with the preceding " and ", and adjust `[I]/[We]`, `[is]/[are]`, and `Trustee[s]` to singular. |
| `[GRANTEE TRUST]` | Trust name in ALL CAPS (same as header). |
| `[DocDate]` (in body) | Blank fill-in line: `________________________` |
| `Trustee[s]` | Use `Trustees` for two; `Trustee` for one. Remove the brackets either way. |
| `[ADDRESS]` (Paragraph (e), property reliance sentence) | Street address of the property being transferred (same as the deed's Property Address paragraph). |

### Signature block (page 2)

| Placeholder | Value |
|---|---|
| `[Ordinal DocDate]` ("Executed as a sealed instrument…") | Blank fill-in line: `this _____ day of ________________, 20___` |
| `[GRANTEE TRUSTEE]` (left signature cell) | First trustee's name |
| `[GRANTEE COTRUSTEE]` (right signature cell) | Second trustee's name. If only one trustee, delete the right cell's contents and the entire right column row. |
| `[SIGNING COUNTY]` | Massachusetts county where the certificate will be notarized — usually the same county as the property. If unknown, leave a blank fill-in line: `__________________________`. |
| `[DocDate]` (notary acknowledgment) | Blank fill-in line: `________________________` |
| `[RETRUSTEE]` and `[COTRUSTEE]` (notary acknowledgment) | First and second trustee names. For a single trustee, delete `and [COTRUSTEE]` and change "persons whose names are signed" / "they signed it voluntarily" to singular ("person whose name is signed" / "he/she signed it voluntarily" — leave he/she as a blank fill-in if gender is not confirmed). |
| `[Notary Commission]` | Blank fill-in line: `_______________` (Scott's notary commission expiration is filled in at signing). |

### Single-trustee adaptation summary

When there is only one trustee, every plural construct collapses to singular and the second
trustee is removed everywhere. Check each of these locations after substitution:

- Header "Name of Trust" stays the same
- Body paragraph 1: "I," "am," single trustee name, "Trustee" (singular)
- Paragraphs (a)–(g): "Trustee" not "Trustees"
- Signature table: drop the right-hand signature cell
- Notary acknowledgment: singular "person" / "name is signed" / "he or she"

### What to leave alone

- Page margins, fonts (Garamond), spacing, and the borderless signature table layout
- Paragraph numbering and the parenthetical letters (a)–(g)
- The `[SIGNATURE PAGE TO FOLLOW]` centered marker and the page break that follows it
- The footers (no substitutions needed there)

After substitution, verify that no `[BRACKETS]` remain anywhere in the document except for the
intentional blank fill-in lines (trust date, signing date, county if unknown, notary commission).

---

## Step 3 — Populate the Realty Trust Template (if requested)

Use the `docx` skill to unpack, find-replace, and repack `assets/Realty_Trust_Template.docx`.

> **Critical — replace `[REALTY TRUST]` in the footers too.** The Realty Trust template has
> `[REALTY TRUST]` in two footer files in addition to the body:
> - `word/footer1.xml` — `[REALTY TRUST] DECLARATION OF TRUST`
> - `word/footer3.xml` — `[REALTY TRUST] SCHEDULE OF BENEFICIAL INTEREST AND AGREEMENT`
>
> When you run find-replace on `[REALTY TRUST]`, apply it to **`word/document.xml`,
> `word/footer1.xml`, and `word/footer3.xml`** (every `.xml` file under `word/` that contains
> the placeholder). After packing, unzip the resulting `.docx` and grep both footer files to
> confirm the realty trust name appears there and no `[REALTY TRUST]` remains.
> `word/footer2.xml` contains only the boilerplate "Practitioner's Action Steps…" page footer
> and has no placeholders — leave it alone.

### Declaration of Trust — Substitutions

Replace all placeholders per the table in the Template Structure section above. All dates
become blank fill-in lines. County lines become blank fill-in lines.

The opening clause should read (after substitution):

> **[CLIENT FULL NAME] and [SPOUSE FULL NAME]**, (the "Trustee"), hereby declare that they
> and their successors in trust will hold any and all property... [rest of boilerplate unchanged]

### Schedule of Beneficial Interests — Ownership Table

The template includes **two pre-built beneficiary table variants**. Delete the one that does
not apply and populate the one that does:

**Joint trust (100%)** — one row:

| Beneficiary | | Interest |
|---|---|---|
| Trustees of the **[JOINT TRUST NAME ALL CAPS]** u/d/t dated ________________________, or any successor Trustees thereof | | 100% of any and all property held from time to time by the trustees of the [REALTY TRUST] |

Delete the two-row (50%/50%) table variant entirely.

**Separate trusts (50%/50%)** — two rows:

| Beneficiary | | Interest |
|---|---|---|
| Trustees of the **[CLIENT TRUST NAME ALL CAPS]** u/d/t dated ________________________, or any successor Trustees thereof | | 50% of any and all property held from time to time by the trustees of the [REALTY TRUST] |
| Trustees of the **[SPOUSE TRUST NAME ALL CAPS]** u/d/t dated ________________________, or any successor Trustees thereof | | 50% of any and all property held from time to time by the trustees of the [REALTY TRUST] |

Delete the single-row (100%) table variant entirely.

Living trust dates in the table are always blank fill-in lines (`________________________`).

### Schedule — Signature Blocks

The template has three signature table sections in the Schedule:

1. **Beneficiaries** (first block) — `[CLIENT]` as Trustee of the joint/client trust | `[SPOUSE]` as Trustee of the joint/client trust
2. **Beneficiaries** (second block) — `[CLIENT]` as Trustee of the spouse trust | `[SPOUSE]` as Trustee of the spouse trust
3. **Trustees** — `[CLIENT]`, Trustee of `[REALTY TRUST]` | `[SPOUSE]`, Trustee of `[REALTY TRUST]`

**Joint trust:** Populate blocks 1 and 3. Block 1 reads: `[CLIENT], Trustee of the [JOINT TRUST NAME]` | `[SPOUSE], Trustee of the [JOINT TRUST NAME]`. Delete block 2 (the separate spouse trust block) entirely.

**Separate trusts:** Populate all three blocks. Block 1 uses the client trust name, block 2 uses the spouse trust name, block 3 uses the Realty Trust name.

All signature lines are blank underscores. The "Not to be recorded" note stays as-is.

---

## Step 4 — Display a Confirmation Summary

Before saving any files, show Scott a two-column summary table of every placeholder and value
used (or "— blank fill-in line —"). Show a separate table for each document produced:

- Deed (always)
- Trustee's Certificate (always)
- Realty Trust Declaration (if drafted)
- Realty Trust Schedule (if drafted)

Then ask:

> "Does everything look correct? Should I make any changes before saving?"

**Always flag:**
- ⚠️ **All trust/execution dates are blank fill-in lines** — to be completed before signing.
- ⚠️ **County lines are blank fill-in lines** — confirm signing county before execution.
- ⚠️ **Notary commission expiration is a blank fill-in line** — Scott completes at signing.
- ⚠️ **"Not to be recorded" note on the Schedule** — confirm client understands the Schedule is kept private.
- ⚠️ **Recording order at the registry:** Trustee's Certificate is recorded **alongside** the deed;
  the Realty Trust Schedule is **not** recorded.

Do not save any files until Scott explicitly confirms.

---

## Step 5 — Save the Completed Documents

After confirmation, save to outputs using the format `YYYY-MM-DD_[Grantee]_[Document Title].docx`:

| Document | Filename |
|---|---|
| Deed | `YYYY-MM-DD_[Grantee Last Name]_Quitclaim Deed.docx` |
| Trustee's Certificate | `YYYY-MM-DD_[Grantee Last Name]_Trustees Certificate.docx` |
| Realty Trust | `YYYY-MM-DD_[Grantee Last Name]_Realty Trust.docx` |

- Use today's date for `YYYY-MM-DD` (e.g., `2025-06-17`)
- **[Grantee]** is the trust or realty trust receiving the property (e.g., `TREACY REALTY TRUST` → `Treacy Realty Trust`; or the living trust name in title case)
- For a direct-to-living-trust transfer, use the trust's short name (e.g., `Smith Family Trust`)
- No `DRAFT` prefix — the `YYYY-MM-DD_Grantee_Title` format is self-identifying
