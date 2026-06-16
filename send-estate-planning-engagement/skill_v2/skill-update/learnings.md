# Learnings — send-estate-planning-engagement

- 2026-06-04: SignWell API requires the base64 file entry key to be `name`,
  not `file_name` (422 "name can't be blank" otherwise). Fixed in
  send_engagement.py.
- 2026-06-04: Save location changed from OneDrive lead folders to a flat
  folder: `/Users/aubreylawmacmini/Desktop/Claude Cowork Mini/Signwell
  Engagement Agreements`. Base64 upload is the standard SignWell path; the
  Make.com share-link webhook is legacy.
- 2026-06-04: LP template updated — per-row optional-services checkboxes
  (`{{c:1:n}}`), required spouse signature (`{{signature:2:y}}`). Client
  signature tag normalized to `{{signature:1:y}}` (uploaded version had
  `{{signature1:y}}`, missing colon).
- 2026-06-04: Inputs simplified to: client name/email, spouse name/email if
  couple, will vs trust plan, legal plan name if applicable, flat fee if no
  legal plan. Trust type, deed, CST, and phone questions removed.
- 2026-06-04: Will Plan + legal plan supported via automatic Schedule A
  edits. Will-only flat-fee remains manual (no template bundled).
- 2026-06-04: Individual clients adapted from the couple template (spouse
  blocks and Joint Representation section removed) — flag for careful review.
- 2026-06-04: SignWell checkbox text tag must be `{{c:1:n}}` or
  `{{check:1:n}}` — `{{c1:n}}` (no colon) is NOT detected. Verified via
  test-mode sends; template normalized accordingly.
