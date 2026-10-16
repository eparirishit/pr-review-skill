# Severity, confidence and attribution

| Severity | Impact |
| --- | --- |
| P0 | Catastrophic urgent harm, such as unconditional destruction of populated production data |
| P1 | Serious security/correctness/data-integrity impact, such as removed owner authorization |
| P2 | Meaningful bounded defect or incomplete required behavior, such as excluding a supported discount boundary |
| P3 | Limited correctness/robustness defect |

Severity is not finding confidence, reviewer urgency, code size or the mere existence of an unmet criterion. Explain impact and preconditions. Do not promote ordinary gaps to P1 because the PR says "complete". No INFO findings.

Confidence: `high` = direct source/reproduction strongly establishes the issue; `medium` = strong reasoning with an important condition unverified; `low` = substantial assumptions. Ordinarily keep low-confidence concerns in explicitly unverified residual risks/questions. Investigate high-impact hypotheses before calling them defects.

Compare before/after: `introduced_by_change=yes|no|unknown`. A requirement newly supplied by a reviewer does not make an unchanged defect introduced. Material pre-existing findings may be included with `no`; they do not become PR blockers solely by discovery. Unknown attribution stays unknown.

Deduplicate root cause and scenario. Keep three categories: actionable findings, non-blocking improvements, limitations/questions/residual risks. A concrete unvalidated concern is not automatically an actionable defect. Missing tests, style preferences and speculative redesign are not confirmed bugs.

Example finding: `F1 — Accept the inclusive discount boundary | P2 | high | correctness | checkout.py:2 | Static tracing shows 100 fails the <100 guard | checkout(10,100) raises instead of returning zero | valid fully discounted orders fail | change to <=100 and test the boundary | R1 | introduced=yes | validation=passed (static tracing only; runtime not run).`

Material blockers normally are introduced/unknown P0/P1; a P2 may block if it demonstrably prevents required behavior, with rationale. Do not use unrelated pre-existing defects or uncertainty as automatic blockers. Risk derivation and count rules live in report-schema.md.
