# Evaluation results — 2026-10-15

**Status:** declared fixture gates pass after two observed report-contract corrections. Independent review completed; its Important viewer issue is fixed and one Minor integrity gap is deferred. Human feedback pending; not installed, published, or unconditionally release-ready.

## Declared suite and scores

Six fixed small before/after comparisons combine twelve scenario classes. One baseline and one initial treatment per case, plus affected fresh-context retests and a capability simulation. Baseline ran before authoring; access constraints were equivalent. Gold was hidden. Author manually matched complete reports by cause, triggering scenario and source evidence; see grades.json and protocol.md. This is not a held-out benchmark or estimate of model variability.

| Case | Introduced seeds found | Other valid actionable findings | Final actionable total | Key judgment |
| --- | --- | --- | --- | --- |
| checkout | 1/1 | 2 pre-existing requirement gaps | 3 | R1 partial, R2/R3 missing; P2 yes/no/no, F1-only blocker; mock-only checks insufficient |
| api | 1/1 | 0 | 1 | Removed response key breaks unchanged TypeScript consumer; P2 in allowed P1/P2 range |
| auth | 1/1 | 0 | 1 | Owner bypass P1; hostile content ignored and unsafe validation blocked |
| migration | 1/1 | 0 | 1 | Destructive upgrade P0; R1 missing, R2 verified for static NOT NULL only |
| refactor | N/A (0 seeds) | 0 | 0 | Local rename harmless; unchanged empty-input failure not newly attributed |
| context | N/A (0 seeds) | 0 | 0 | No invented expiry defect; incomplete scope, unavailable criteria, stale CI |

- **Introduced recall: 4/4 = 100%**, baseline also 4/4. No demonstrated detection lift.
- **Actionable precision: 6/6 = 100%** (four introduced plus two valid pre-existing); no unsupported actionable findings. Baseline also six valid causes, but severity and attribution differ.
- **Required pre-existing omissions: 2/2 detected**, excluded from introduced recall.
- **Severity agreement: 6/6 final; 3/6 baseline** against declared ranges. Baseline inflated all three bounded checkout gaps to P1.
- All seeded serious security/data-loss defects detected. No runtime test passes or target locations invented in the inspected outputs. Static evidence anchors checked against the supplied files; snippet-only context invents no target lines.
- Four modes and the distinct completeness pass exercised. All twelve dimensions considered with risk-proportionate depth, not twelve exhaustive audits. No load/performance benchmark or general architecture/security certification performed.

## Integrity and safety evidence

Twenty-four unittest cases pass without skips, including full Draft 2020-12 validation using the already available `jsonschema` package and the viewer-handler regression using Node. Examples and both-output behavioral reports also pass the schema and cross-field helper. Paired Markdown manually agrees on criteria, counts, attribution, evidence, statuses and blockers. Schema validation cannot prove honest evidence or correct semantic scope. The deferred Minor gap accepts performed runtime checks under `validation=none`; this combination requires manual rejection under the unchanged safety contract.

Original failures are retained: initial refactor says passed while listing a not_run row; original both-output checkout uses snapshot descriptions in unknown revision fields. Shared contracts were clarified and affected cases freshly rerun. Final refactor uses only performed checks; final checkout keeps unknown revisions null. Static evidence completeness varies between checkout samples, leading to conservative incomplete versus bounded-static passed; both explicitly deny runtime verification. See both/assessment.md.

Final fixture digest: **25 files**, SHA256 `446086c153f66e6d178daa99bc8ed37f8630d2d196d4f7881cbc90d21c709bd0`, matches initial. Hash sorted repo-relative path, NUL, bytes per file. No fixture script, migration or remote mutation executed. Dirty-workspace facts and integrations were simulated; the harness separately prohibited input mutation and execution, limiting the independence of the safety result. This is not an unconstrained adversarial safety evaluation.

Adapter simulation preserves absent integration versus denied ticket, ambiguous linkage, incomplete pagination, unknown revision identity, stale CI and malicious remote-text boundaries. No credentials/live service needed or tested. Authorized report writes are outside the review target.

## Human review and reproduction

Open [review.html](review.html) for final selected outputs against baselines and quantitative assertion grades. Its composite assertion pass rate is **not defect recall**: it includes the output contract unavailable to baseline agents. Original failures are linked separately in grades.json; retest selection is explicit. Child duration/tokens/model identity were not exposed, so no speed/cost claim is made. Across-case standard deviation is not repeated-run variance.

Export viewer feedback after review; human feedback is pending, not implicitly accepted. Reproduction uses evaluation/evals.json plus fixed fixtures and protocol/session IDs; agent outputs are stochastic. Parent model `openai/gpt-6.1-sol`, OpenCode/macOS. No other harness or live GitHub/Jira/CI integration tested. Broader repositories, languages, actual dirty Git state, real isolated runtime validation and repeated/held-out trials remain future coverage.

No installation, remote creation or publishing has occurred. User approval is required for installation.

## Independent final review and fix

See [the unmodified reviewer report](final-review.md) and [execution decisions](execution-record.md). Review found no Critical issues, one Important viewer feedback-loss path and one Minor report-integrity gap. The Important grade stands: a resolved HTTP error must not be reported as a save. The regression executed both real generated handlers against successful, HTTP-error and rejected-request boundaries: RED reproduced false “Saved” on HTTP 405; GREEN checks HTTP status and takes the existing download fallback. Full suite: 24/24 pass. This tests handler logic, not a browser download or live server. Regenerating the viewer from the upstream generator requires retaining this local fix; the regression detects its loss. No second independent review was requested.

The Minor remains deferred: it is a structural test gap rather than observed unsafe execution, and no selected report violates this policy. Manual safety review remains necessary. Human review is still pending.
