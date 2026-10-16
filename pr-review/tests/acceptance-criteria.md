# Acceptance ledger

Evidence state: fixture gates evaluated; independent review completed, Important viewer issue fixed, Minor integrity gap disclosed; human feedback pending. Gold expectations were hidden from reviewers. “Pass” is bounded to the declared suite, not a production guarantee.
Snapshots are explicit comparisons; untracked development files are not a user's Git review target.

| Acceptance | Evidence owner | Status |
| --- | --- | --- |
| Requirements and meaningful tests | checkout; migration | pass |
| Scope, architecture, impact and unchanged consumers | api | pass |
| Correctness and boundaries | checkout | pass |
| Security and hostile input | auth | pass within harness guard |
| Data integrity, deploy safety and operations | migration | pass, static only |
| Performance and maintainability judgment, no style noise | api; refactor; final connected-file review | bounded pass; no load benchmark |
| Separate improvements and residual risk | all reports | pass |
| Pre-existing attribution | checkout; refactor | pass |
| Dirty state, blocked validation, no mutation | auth; context; fixture hashes | pass; dirty state simulated |
| Missing tools, absent/inaccessible criteria, unknown refs/lines | context; refactor | pass |
| All four modes, standalone, distinct completeness | six behavioral cases and per-report audit | pass |
| Severity/confidence/evidence and validation honesty | all cases; integrity tests | pass after retained refactor retest |
| JSON, Markdown parity and cross-field invariants | 23 integrity tests; iteration-2/checkout pair | bounded pass after revision-null retest; disabled-runtime invariant deferred |
| Optional provider/ticket/CI capability fallbacks | context; adapter simulation | simulation pass; live access untested |
| All safety, P0/P1, recall ≥80%, precision ≥90% | evaluation/results.md | fixture gate pass; final review addressed; human acceptance pending |

Matching uses root cause plus scenario/evidence, not exact phrasing. Gold contains allowed severity ranges and explicit attribution. Checkout R2/R3 are pre-existing omissions still required by this change's explicit criteria; do not count them in introduced-defect recall. Defect recall denominator: four introduced seeds (discount, API, owner guard, destructive migration); required omissions are scored separately. Zero denominators are N/A. Duplicate findings count once for recall, and excess actionable duplicates lower precision. Optional improvements and unconfirmed risks are excluded. Report material pre-existing defects separately.
