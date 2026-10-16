# Report contract

Use the eight sections in templates/review-report.md. JSON uses schema version `1.0` and templates/review-report.schema.json. The schema pins exact nested shapes; Markdown renders the same information. Unknown revisions/story source/total file count may be null. Omit an unlocatable finding location (or use null where allowed); never invent line numbers. Label snapshot-relative paths/revision evidence clearly.

Required finding slots: unique ID, title, P0–P3 severity, independent confidence, category, evidence, triggering scenario, concrete impact, practical recommendation, introduced_by_change yes/no/unknown, validation status/evidence, and optional requirement IDs/location. Location contains file and known start/end lines. Findings are distinct from improvements and residual risks.

Choose one canonical category: `requirements|scope|correctness|architecture|impact|testing|security|data_integrity|performance|maintainability|operations`. Add nuance in evidence, not extra category values. JSON includes `review.read_only=true`; scope includes type, nullable base/head, reviewed_files, nullable total_changed_files and incomplete; validation includes policy, evidence_incomplete, status and checks. The schema and tests/reports/valid.json illustrate exact nesting.

Requirement slots: unique ID, text, explicit/inferred provenance/source, one canonical status, evidence and gap. Empty sections say none/unknown briefly, not filler. Empty criteria do not imply acceptance approval. In both output mode derive both representations from one result ledger.

## Derived values

- Count each actionable finding exactly once in its P0/P1/P2/P3 count, including separately labeled pre-existing findings. Overall risk uses only introduced/unknown findings: highest P0→critical, P1→high, P2→medium, P3→low. With no such finding and material scope limitations use `incomplete`; otherwise `low`. If findings establish risk, retain it and disclose scope gaps separately.
- Validation checks have name, kind static/runtime, outcome passed/failed/not_run/blocked, evidence and nullable reason. Record manual tracing explicitly as static. No performed checks means no passed/failed checks.
- The checks ledger contains performed checks and relevant planned checks. Optional future suggestions or generic disabled execution belong in limitations, not extra ledger rows. If a `not_run`/`blocked` row is in the ledger and any check was performed, summary cannot be `passed`. This keeps Markdown and JSON derivation identical, including quick static-only reviews.
- Summary validation: any failed check → `issues_found`; else disabled with zero performed → `not_run`; else blocked/not_run relevant planned checks or incomplete evidence → `incomplete`; else at least one performed and all planned passed → `passed`; else → `not_run`. Review summary and validation status agree. A disabled review may still record performed manual static inspection; it cannot perform executable checks.
- Finding validation allows passed/failed/not_run/blocked/incomplete and describes its evidence, not mitigation. A check failure confirming a defect is still a failed check. Preserve separate static/runtime limitations.
- Unique IDs; finding requirement links exist; reviewed files ≤ known total; known start/end lines are positive integers with end ≥ start. Blocker IDs reference findings, exclude pre-existing defects, and include rationale for P2/P3 blocking decisions.
- Conclusion lists material blockers, remaining risks and next actions. With no established findings say so within inspected scope, not "approved". Material unknowns remain visible even if no blocker is proven.

Before rendering, perform a separate reconciliation: every requirement, every finding/evidence/attribution, every count, check outcome, risk, blocker and location. Canonical formatting is not evidence of review quality.
