# Lead OneDrive Folder — Naming & Creation

## Parent path (fixed)

```
/Users/aubreylawmacmini/Library/CloudStorage/OneDrive-AubreyLaw/Aubrey Law Clients/Estate Planning
```

This is the local OneDrive sync path. Files written here are uploaded to
SharePoint by the OneDrive client. The skill writes locally; OneDrive
handles the sync transparently.

## Folder hierarchy

Lead folders live **directly** under the Estate Planning root. There is no
intermediate year folder — the year is the first segment of the lead
folder name itself.

```
Estate Planning/
├── 2026-EP-Doe, John & Jane/                  ← flat-fee couple
│   └── Engagement Agreement - Doe - 2026-05-19.docx
├── 2026-EP-Jones, Bob/                        ← flat-fee single
├── 2026-EP-LP-Smith, Sean & Sara/             ← legal-plan couple
│   └── Engagement Agreement - Smith - 2026-05-19.docx
├── 2026-EP-LP-Brown, Sarah/                   ← legal-plan single
├── 2025-EP-Wilson, Mary & Tom/                ← previous year
└── ...
```

## Lead folder format

```
YYYY-<prefix>-LastName, FirstName [& SpouseFirst | & SpouseFirst-SpouseLast]
```

| Practice area | legal_plan | Prefix | Example |
| --- | --- | --- | --- |
| Estate Planning (flat fee) | `false` | `EP` | `2026-EP-Doe, John & Jane` |
| Estate Planning - Legal Plan (ARAG, MetLife, Hyatt, LegalShield, LegalEASE) | `true` | `EP-LP` | `2026-EP-LP-Smith, Sean & Sara` |

Both variants use the same `-` (dash) separator between every segment.
The only difference is whether the practice-area prefix is `EP` or `EP-LP`.

After the last name and comma + first name:

- ` & SpouseFirst` — appended when couple AND spouse shares the primary
  client's surname (no need to repeat the surname)
- ` & SpouseFirst-SpouseLast` — when the spouse has a different surname,
  attach the spouse's surname with a hyphen (so the folder still uniquely
  identifies both people)

### Full examples

| Inputs | Lead folder name |
| --- | --- |
| EP, single: Bob Jones | `2026-EP-Jones, Bob` |
| EP, same surname: John & Jane Doe | `2026-EP-Doe, John & Jane` |
| EP, different surnames: John Smith & Jane Doe | `2026-EP-Smith, John & Jane-Doe` |
| EP-LP, single: Sarah Brown | `2026-EP-LP-Brown, Sarah` |
| EP-LP, same surname: Sean & Sara Smith | `2026-EP-LP-Smith, Sean & Sara` |
| EP-LP, different surnames: Alice Johnson & Mark Lee | `2026-EP-LP-Johnson, Alice & Mark-Lee` |

The year is `YYYY = current calendar year` at skill invocation — the year
the engagement agreement is generated, not the client's intake date.

The script `build_lead_folder_name()` in `scripts/send_engagement.py`
implements this rule. The prefix branch is keyed off the `legal_plan`
boolean from the same inputs JSON that drives the document render — so the
folder prefix is guaranteed to match the agreement type.

## File naming

```
Engagement Agreement - LastName - YYYY-MM-DD.docx
```

- `LastName` is the primary client's last name only (no spouse, no comma).
- `YYYY-MM-DD` is today's date at skill invocation.
- If a file with the exact same name already exists, append `-2`, `-3`, etc.
  before the `.docx` extension. Never overwrite — engagement agreements are
  legally significant artifacts.

## Transition from lead to retained matter

When the client signs and the matter is retained, Scott typically renames
the folder using the matter convention from the `new-matter-folder` skill
(`YYYY_LastName, FirstName`) and moves it into `Clients/Estate Planning/`.
That rename happens outside this skill — do not attempt it here.

## When the folder already exists

If the lead folder already exists (e.g., Scott previously generated a draft
agreement for the same client this same year), use it — do not create a
duplicate. Save the new .docx alongside the prior one; the filename's
date and collision-safe suffix keep them distinct.

If the same client previously had a flat-fee folder (`EP-`) but is now
being engaged under a legal plan (`EP-LP-`) — or vice versa — the new
folder will have a different prefix and be created fresh. Don't auto-
migrate; leave both folders in place and let Scott consolidate manually
if he wants.

## Implementation notes

The script uses `pathlib.Path` with `parents=True, exist_ok=True` for
`mkdir`. The path with spaces and the special characters `,` and `&` are
safe inside `pathlib`; pass the path as a `Path` object, not a shell string.

If the parent path `Aubrey Law Clients/Estate Planning` does not exist
(OneDrive not mounted, or unusual env), the script raises a clear error
instead of silently creating a stray local directory.
