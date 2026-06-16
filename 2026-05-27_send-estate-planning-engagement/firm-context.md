# Firm Context — Aubrey Law

This file is read by the send-estate-planning-engagement skill (and other
Aubrey Law skills). Keep it in the Cowork working directory.

## Firm

- Name: Aubrey Law, LLC
- Attorney: Scott Aubrey
- Practice: Estate Planning (Massachusetts only)
- Address: 1329 Highland Ave, Suite 1, Needham, MA 02492
- Phone: (781) 474-3450
- Website: aubreylegal.com
- Portal: portal.aubreylegal.com

## Document standards

- Body font: Garamond 12pt
- Headings: Navy `#1B3A6B`
- Accents: Teal `#0F6E56`
- Body text: `#2C2C2A`
- Style prefix: `TR-` on all custom Word styles
- Section numbering: decimal
- Placeholder convention: `[BRACKET]` in static templates
- Firm footer text:
  `1329 Highland Ave, Suite 1, Needham, MA 02492 · (781) 474-3450 · aubreylegal.com`

## Storage paths

- OneDrive root for clients:
  `/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients`
- Estate Planning leads/clients parent:
  `/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning`

## DocuSeal API token

The send-estate-planning-engagement skill posts the rendered .docx directly
to DocuSeal's REST API via `scripts/docuseal_upload.py`. Get a token from
https://docuseal.com/settings/api → "API token" and paste it here:

```
docuseal_api_token: sabwmP9XKRjq4bstRK64752LB4DpY1UqPXvuLth3qa2
```

**Security:**
- Treat this token like a password. Do not commit `firm-context.md` to any
  public repo or share the skill folder publicly.
- Rotate the token at the DocuSeal settings page anytime it may have been
  exposed (e.g., after a test in a sandbox that you didn't fully control).
- If the token is missing or still the placeholder, the skill falls back
  to manual editor upload rather than failing silently.

The legacy Make.com SharePoint share-link webhook is no longer used by this
skill. The setup notes are preserved in `references/make-webhook-setup.md`
for reference only.

## Engagement defaults (optional)

- `flat_fee_default`: 5500   # Starting point Scott can override per matter

## Quality check preference

- For court filings and client-facing documents: always run quality review.
- For internal automation outputs: skip unless flagged.

## Practice area / jurisdiction

- Practice area: Estate Planning
- Jurisdiction: Commonwealth of Massachusetts
- Court rules: MGL c. 190B (MUPC), MGL c. 201D (trust), RUFADAA
- Tax structure: MA estate tax, no portability — Credit Shelter Trust
  planning where applicable
