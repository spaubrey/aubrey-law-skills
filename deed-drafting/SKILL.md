---
name: deed-drafting
description: >
  Drafts the Massachusetts deed-transfer recording package — a Quitclaim Deed AND its companion
  Trustee's Certificate (M.G.L. c. 184 § 35) — transferring real property to a trust, using an
  uploaded deed (PDF or Word) as the source. Use this skill whenever Scott uploads a deed and
  wants to produce a draft transfer deed or trustee's certificate — including phrases like
  "draft a deed from the uploaded deed", "create a deed to transfer property to the trust",
  "populate the deed template", "draft a quitclaim deed", "draft the trustee's certificate", or
  any request involving an uploaded deed file and a transfer to a trust. Always use this skill
  when a deed document is uploaded and Scott wants a new deed or recording package produced from
  it, even if the request is casual like "make a deed from this" or "fill out the deed template
  using this deed."
---

# Deed Drafting Skill — Aubrey Law

## Purpose

This skill extracts property and party information from a client's current deed and uses it to
populate two Aubrey Law templates that are recorded together at the registry:

1. **Quitclaim Deed** transferring the property to the trust
2. **Trustee's Certificate** pursuant to M.G.L. c. 184 § 35, evidencing the trustees' authority

Both documents are produced as a package — the deed references the certificate ("as evidenced by
a Certificate of Trustees pursuant to M.G.L. c. 184, §35, recorded herewith"), and the registry
will not record the deed without the certificate.

The bundled template files are:
- `assets/Cowork Deed Template_v01.docx` — the Quitclaim Deed
- `assets/Trustees Certificate Template.docx` — the Trustee's Certificate

Use these bundled files as the base for every matter. Open and edit them directly — do not build
either document from scratch. Each template's exact font, spacing, page layout, and signature-page
structure must be preserved.

---

## Step 0 — Confirm Trust Details Before Starting

Before extracting anything from the deed, ask Scott two questions (use AskUserQuestion tool):

1. **What is the full name of the trust?** (This will be inserted in ALL CAPS — e.g., "TREACY REALTY TRUST")
2. **Who are the trustees?** Confirm whether the grantors on the uploaded deed are themselves
   the trustees of the new trust, or whether different people will serve as trustees.

In most cases the grantors and trustees will be the same people — the clients are transferring
their property into their own trust. Confirm this assumption explicitly rather than guessing.

Do not proceed to extraction or population until Scott has confirmed both answers.

---

## Template Structure (What's in the File)

The template is a US Letter document (1-inch top/bottom, 0.75-inch left/right margins) in
Garamond font. It has exactly this layout:

**Page 1:**
- Large top spacing, then centered bold: `QUITCLAIM DEED`
- Grantor/grantee block (see Step 1 for how to populate)
- A floating text box (anchored to the page) with: `PROPERTY ADDRESS: [ADDRESS]` — this is a
  Relaw.ai auto-fill field, leave it **completely untouched**
- `with Quitclaim Covenants,`
- Then: `[Property Description]`
- Metes-and-bounds rows (each indented, with tab stops): `[Directional Call 1]  [Bound Description 1]` through Call 6
- `[DESCRIPTION 2]`
- `Meaning and intending to convey the same premises of Grantors' deed recorded on [Recording Date of Current Deed], and filed in the [Registry of Deeds] in Book [Current Deed Book Number], Page [Current Deed Page].`
- **Property Address paragraph** (added just before the page break):
  `Property Address: [street address of the property]`
- Centered: `[SIGNATURES ON NEXT PAGE]` with a page break

**Page 2 (Signature page):**
- `Witness our hands and seals this _____ day of ________________.`
- Signature table: two signature lines side by side — `[GRANTOR]` on the left, `[GRANTOR 2]` on the right (borderless table)
- `COMMONWEALTH OF MASSACHUSETTS`
- `COUNTY OF __________________________`
- Notary acknowledgment paragraph referencing `[GRANTOR] and [GRANTOR 2]`
- Notary signature line, `Notary Public`, `My Commission Expires:`

> **Important:** The recording reference placeholder in the actual template XML reads
> `[Recording Date of Current Deed]` — not "Deed". Use that exact text when doing find-replace.

---

## Step 1 — Extract Information from the Uploaded Deed

Read the uploaded deed carefully and extract the following values:

| Placeholder in Template | What to Extract |
|---|---|
| `[GRANTOR]` | First grantor's full legal name (ALL CAPS) |
| `[GRANTOR 2]` | Second grantor's full legal name (ALL CAPS). If only one grantor, delete this placeholder **everywhere it appears** — in the body paragraph, in the signature table, and in the notary acknowledgment — and remove any orphaned "and" or punctuation. |
| Trustees | Use the names confirmed in Step 0. In most cases these are the same as the grantors. Both trustees are named in the grantee clause (see Step 2). |
| `[TRUST NAME]` | Use the name confirmed in Step 0, formatted in **ALL CAPS** everywhere it appears. |
| Trust date | Replace `[DocDate]` with a blank fill-in line: `________________________` |
| `[Property Description]` | Opening property description paragraph (e.g., "A certain parcel of land situated in…") |
| `[Directional Call 1]`–`[Directional Call 6]` | Each metes-and-bounds directional call. Add rows in the same indented tab-stop format if more than 6. Delete unused rows. |
| `[Bound Description 1]`–`[Bound Description 6]` | Corresponding bound for each directional call. |
| `[DESCRIPTION 2]` | Second description paragraph (easements, appurtenances, etc.). Delete entire paragraph if none. |
| `[Recording Date of Current Deed]` | Date the current deed was recorded at the registry *(this is the exact placeholder text in the template XML)* |
| `[Registry of Deeds]` | Full registry name (e.g., "Norfolk County Registry of Deeds") |
| `[Current Deed Book Number]` | Book number from the current deed's recording reference |
| `[Current Deed Page]` | Page number from the current deed's recording reference |
| `ADDRESS` in grantor block | Street address of the grantor(s) |
| `ADDRESS` in grantee block | Mailing address of the trustee/grantee (usually same as property address) |
| Property Address paragraph | Street address of the property (added as a plain paragraph just before `[SIGNATURES ON NEXT PAGE]`) |

**Lot/plan deeds:** If the property uses a lot/plan description rather than metes and bounds,
place the full description in `[Property Description]` and delete all `[Directional Call]` and
`[Bound Description]` paragraphs entirely.

**Registered land (Land Court):** The "Meaning and intending" paragraph uses Document No. and
Certificate of Title instead of Book/Page. Adapt the sentence accordingly.

**CRITICAL — Description format must mirror the source deed exactly:**
- Each boundary call goes in its own paragraph (not concatenated into one paragraph)
- "PARCEL 1" / "PARCEL 2" labels appear as **bold** paragraph headers before each description
- Lead-in sentence ("A certain parcel of land...bounded and described as follows:") is its own paragraph
- Each directional call is its own paragraph: `NORTHEASTERLY: by [description], [measurement];`
- Supporting paragraphs ("Said parcel is shown as...", "The above described land is subject to...", "For title, see...") each get their own paragraph
- If original deed has a "Said premises are conveyed subject to..." paragraph, include it after the last parcel
- [DocDate] in the grantee clause: replace with a blank line (`________________________`), NOT the literal text "[DocDate]"

**Orphaned punctuation:** After any deletion, remove surrounding words (like "and") and
punctuation (commas, semicolons) that would otherwise be left stranded.

---

## Step 2 — Populate the Template

Use the `docx` skill to:
1. Copy the bundled template (`assets/Cowork Deed Template_v01.docx`) to a working location
2. Unpack it, apply all find-replace substitutions to the XML, and repack

### Grantor/Grantee clause

The populated clause should read:

> **[GRANTOR] and [GRANTOR 2]**, of [grantor address] ("Grantors"), for full consideration of
> ONE DOLLAR ($1.00), grant to **[TRUSTEE] and [CO-TRUSTEE]**, Trustees of the
> **[TRUST NAME ALL CAPS]** u/a dated ________________________, as evidenced by a Certificate
> of Trustees pursuant to M.G.L. c. 184, §35, recorded herewith, having a mailing address at
> [grantee address] ("Grantee"),

- Trust name is always ALL CAPS (e.g., `TREACY REALTY TRUST`)
- `[DocDate]` is replaced with a blank fill-in line: `________________________`
- If the grantors are the trustees (most common case), the trustee names are the same as the
  grantor names — just inserted into the trustee slots

### Property Address paragraph

Add a new paragraph **after** the "Meaning and intending..." sentence and **before** the
`[SIGNATURES ON NEXT PAGE]` centered line. Format it as plain body text:

> Property Address: [street address of the property]

(Use the actual street address extracted from the deed.)

Do **not** alter: the floating property-address text box, page margins, paragraph spacing, font
(Garamond), or the signature-page layout. These must remain exactly as in the template.

After substitution, verify that no `[BRACKETS]` remain anywhere in the document except for
intentional blanks like the trust date fill-in line.

---

## Step 2b — Populate the Trustee's Certificate

Open `assets/Trustees Certificate Template.docx` and apply the substitutions below. The
certificate reuses the trust and trustee information already gathered in Step 0 and Step 1, so no
new client data is required — only the values you've already confirmed.

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

After substitution, verify that no `[BRACKETS]` remain anywhere in the document except for the
intentional blank fill-in lines (trust date, signing date, county if unknown, notary commission).

---

## Step 3 — Display a Confirmation Summary

Before saving, show Scott **two** two-column tables — one for the **Quitclaim Deed** and one for
the **Trustee's Certificate** — listing every placeholder and the value used (or "— blank fill-in
line —"). Then ask:

> "Does everything look correct on both documents? Should I make any changes before saving?"

**Always include these flags:**
- ⚠️ **Trust date is a blank fill-in line** on both documents — Scott will add the trust agreement date before execution.
- ⚠️ **Notary commission and signing date** on the Trustee's Certificate are blank fill-in lines — completed at signing.
- ⚠️ If the signing county was unknown, flag that it is a blank fill-in line on the certificate.

**Do not save either file until Scott explicitly confirms.**

---

## Step 4 — Save the Completed Recording Package

After Scott confirms, save **both** populated documents to the local outputs folder for Scott to
download:

**Deed filename:** `DRAFT - [Grantor Last Name] Deed [YYYY-MM-DD].docx`
**Certificate filename:** `DRAFT - [Grantor Last Name] Trustees Certificate [YYYY-MM-DD].docx`

- Use today's date for `[YYYY-MM-DD]`
- If two grantors have different last names, use the first grantor's last name (use the same last
  name on both files so they sort together)
- The `DRAFT` prefix signals these require attorney review before use
- Provide Scott with `computer://` links to **both** files in the final response, since they are
  recorded together as a single package
