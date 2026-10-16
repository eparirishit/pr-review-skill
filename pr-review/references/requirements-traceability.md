# Requirements traceability

Use explicit requirements when available. Otherwise label inferred intent and its confidence/source; no title-derived acceptance criteria masquerade as a ticket. Empty criteria remain empty. Unknown criteria are a limitation, not an invented requirement with invented acceptance. If sources contradict, state the conflict and do not pretend it is resolved.

Split independently observable behaviors; retain stable report-local IDs and source/provenance. For each record implementation anchors, relevant tests/static evidence, edge/failure coverage, gap/assumptions and exactly one state:

| State | Evidence rule |
| --- | --- |
| verified | Implementation plus relevant validation supports behavior; explicit static tracing can establish direct properties, not unexecuted runtime/integration behavior |
| implemented_unverified | Implementation appears present but relevant validation is insufficient |
| partial | Demonstrably only part of the criterion is implemented |
| missing | Behavior demonstrably absent within sufficient relevant scope, not merely unlocated |
| unknown | Available evidence cannot establish satisfaction |
| not_applicable | Outside applicability; include justification |

Example: `R1 | Accept discounts 0..100 inclusive | partial | checkout.py:2 excludes 100; static trace | Include upper bound; runtime not run.`

Tests are evidence only for what they exercise. Follow real production entrypoints and assertions. A mock replacing the function under review can pass while validating none of its behavior. Check negative/boundary/regression paths rather than counting tests. Missing tests alone imply neither missing implementation nor a confirmed defect; state the actual validation gap. An unchanged omission may still violate explicit criteria, but its finding attribution remains `no`.
