# Firm Context

This file is generated once during first-time setup and loaded by every skill created
by the Legal Skill Creator. Update it if firm details change.

## Practice Area(s)
Estate Planning (Aubrey Law) — Massachusetts wills, revocable living trusts (individual,
joint, simplified joint), pour-over wills, and incapacity documents (durable power of
attorney, health care proxy, living will / advance directive, HIPAA authorization).

## Primary Jurisdiction
Massachusetts (the al-generator is configured for MA only: states/MA/rules.json).

## Firm Size
Solo / small firm. <!-- Update if this changes. -->

## Document Formatting Standards
- Body text: Garamond 12 pt; footer text: Garamond 10 pt (enforced automatically by
  al-generator.py after rendering — do not override).
- Personal and trust names render in UPPERCASE via the `| name` Jinja filter.
- Output documents are editable Word (.docx) drafts, numbered per package
  (e.g., 01-..., 02-...).
- Firm tooling: MS365 (email, calendar, OneDrive file storage); QuickBooks Online
  (accounting). Generated drafts are typically saved to the matter's OneDrive folder.

## Quality Check Preference
Only for court filings and client-facing
<!-- Options: Always | Only for court filings and client-facing | Let me decide per skill | Never -->
<!-- Estate plan documents are client-facing final deliverables, so the quality review
     step runs by default for this skill. -->

---

## How Skills Should Use This File

Every skill created by the Legal Skill Creator should:
1. Read this file at activation to understand the firm's context
2. Apply jurisdiction-specific rules based on the jurisdiction listed above
3. Follow document formatting standards when producing output (if applicable)
4. Include or exclude the quality review step based on the preference above
5. Reference the practice area when selecting templates or examples
