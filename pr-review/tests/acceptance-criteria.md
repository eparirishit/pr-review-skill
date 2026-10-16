# Acceptance ledger

Initial state: pending behavioral runs. Gold expectations are hidden from reviewers.
Snapshots are explicit comparisons; untracked development files are not a user's Git review target.

| Acceptance | Evidence owner | Status |
| --- | --- | --- |
| Requirements and meaningful tests | checkout; migration | pending |
| Scope, architecture, impact and unchanged consumers | api | pending |
| Correctness and boundaries | checkout | pending |
| Security and hostile input | auth | pending |
| Data integrity, deploy safety and operations | migration | pending |
| Performance and maintainability judgment, no style noise | api; refactor; final connected-file review | pending |
| Separate improvements and residual risk | all reports | pending |
| Pre-existing attribution | checkout; refactor | pending |
| Dirty state, blocked validation, no mutation | auth; context; fixture hashes | pending |
| Missing tools, absent/inaccessible criteria, unknown refs/lines | context; refactor | pending |
| All four modes, standalone, distinct completeness | six behavioral cases and per-report audit | pending |
| Severity/confidence/evidence and validation honesty | all cases; integrity tests | pending |
| JSON, Markdown parity and cross-field invariants | integrity tests; JSON/both behavioral run | pending |
| Optional provider/ticket/CI capability fallbacks | context; adapter simulation | pending |
| All safety, P0/P1, recall ≥80%, precision ≥90% | evaluation/results.md | pending |

Matching uses root cause plus scenario/evidence, not exact phrasing. Gold contains allowed severity ranges and explicit attribution. Checkout R2/R3 are pre-existing omissions still required by this change's explicit criteria; do not count them in introduced-defect recall. Defect recall denominator: four introduced seeds (discount, API, owner guard, destructive migration); required omissions are scored separately. Zero denominators are N/A. Duplicate findings count once for recall, and excess actionable duplicates lower precision. Optional improvements and unconfirmed risks are excluded. Report material pre-existing defects separately.
