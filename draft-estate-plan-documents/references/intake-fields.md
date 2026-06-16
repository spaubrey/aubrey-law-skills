# Intake Fields by Package

Build the client JSON to match the corresponding `assets/generator/examples/*.json`
file exactly — same nesting, same key names. The generator validates required
fields and will report anything missing. Below: which example to mirror, the
required fields, and the inputs to collect each run.

Names render in UPPERCASE automatically (the `| name` filter) — enter them in
normal case. Dates are free text formatted "Month Day, Year" (e.g. "May 21, 2026").

---

## Shared building blocks

- **client**: `full_name`, `city`, `state` ("MA"), `county`; plus, depending on
  package: `street_address`, `signing_county`, `date_of_birth`,
  `pronoun_subject` (she/he/they), `pronoun_object`, `pronoun_possessive`.
- **spouse**: `exists` (bool), `full_name`, optionally `pronoun_possessive`.
- **children**: array of `{ "full_name", "minor": true|false }`. A child with
  `minor: true` triggers guardian provisions.
- **execution**: `signing_scheduled` (bool). If true, also `doc_date`,
  `ordinal_doc_date` ("the 21st day of May, 2026"), `signing_county`,
  `notary_commission`. If false, those render as blank lines.
- **planning**: `uses_revocable_trust` (bool).

---

## core-estate  →  mirror `examples/client.json`
Required: client.full_name, client.state, client.county, client.city,
client.street_address, client.date_of_birth, client.pronoun_subject,
client.pronoun_possessive, fiduciaries.executor.primary.full_name,
fiduciaries.trustee.primary.full_name, fiduciaries.agent.primary.full_name,
healthcare.agent.primary.full_name + .relationship + .address + .phone,
healthcare.agent.alternate.full_name.
Also collect: guardians.primary.full_name (if minor children),
specific_gifts (array of `{item, recipient}`), charitable_gifts.

## incapacity-documents  →  mirror `examples/client-ma-incapacity.json`
Required: client.full_name, client.city, client.state,
fiduciaries.agent.primary.full_name, healthcare.agent.primary.full_name.
Collect: client.street_address, date_of_birth, signing_county, pronouns;
agent.primary (+ optional agent.co_primary.full_name and
agent.co_agents_action "joint"|"separate"; primary_has_spouse bool);
healthcare primary + alternate (full_name, relationship, address, phone);
execution signing details. For unscheduled signing use
`examples/client-ma-incapacity-unscheduled.json` (signing_scheduled:false).

## pourover-will  →  mirror `examples/client-ma-pourover.json`
Required: client.full_name, client.city, client.county, client.state,
trust.name, trust.date, fiduciaries.executor.primary.full_name.
Collect: spouse; children (+minor); executor primary/co_primary/successor/
co_successor; guardians primary/successor/second_successor and optional
guardians.excluded (array of `{full_name, reason}`). If no minor children,
mirror `examples/client-ma-pourover-no-minors.json` (guardian article suppressed).

## joint-trust-simplified  →  mirror `examples/client-ma-joint-trust-simplified.json`
Required: client.full_name, client.state, client.county, spouse.full_name,
trust.name, fiduciaries.trustee.primary.full_name,
fiduciaries.trustee.successor.full_name.
Collect: children (+minor); trust.date; trust.disinherited (array of
`{full_name}`); trust.blended_family.client_children and .spouse_children
(arrays of `{full_name}`) for prior-relationship children; execution details.
Also supports specific_gifts and charitable_gifts
(arrays of `{item, recipient}`) and the blended_family children arrays.

## trust-individual-single  →  mirror `examples/client-ma-trust-individual-single.json`
Required: client.full_name, client.state, client.county, client.pronoun_subject,
client.pronoun_possessive, trust.name, trust.contingent_beneficiary.full_name,
trust.tangible_personal_property.distribution_method ("equal_shares"|"priority_order"),
trust.descendants_distribution.method ("outright"|"staged"),
trust.remote_beneficiaries.individuals (array), trustee primary/successor/
second_successor full_name, fiduciaries.trustee.co_trustees_action
("joint"|"independent"), execution.signing_county, execution.notary_commission,
execution.id_type (e.g. "Massachusetts driver's license").
Conditional detail:
- TPP equal_shares → trust.tangible_personal_property.beneficiaries (array)
- TPP priority_order → trust.tangible_personal_property.priority_beneficiaries (array)
- descendants outright → trust.descendants_distribution.distribution_age
- descendants staged → stage_1_age, stage_2_age, stage_3_age
- remote_beneficiaries.individuals items take `{full_name, share}`; optional
  remote_beneficiaries.charity.name.
- trust.disinherited (array of `{full_name}`) optional.

---

## Field reference
For exact types and descriptions of every field, read
`assets/generator/schemas/data-dictionary.json`.
