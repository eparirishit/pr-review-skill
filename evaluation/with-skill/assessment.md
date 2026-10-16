# Draft comparison — iteration 1

All six reports read in full. Introduced detection remains 4/4 (no measured lift from baseline). Required pre-existing checkout omissions detected 2/2. Checkout P2 calibration and yes/no attribution correct; baseline used P1 without attribution. All reports supply eight sections, criterion states, confidence, counts, explicit provenance and a distinct completeness audit. No unsupported actionable defects in context/refactor; API consumer reasoning preserved. Migration correctly limits R2 verified to static NOT NULL evidence.

Observed report-integrity failure: refactor says validation passed but includes a not_run runtime ledger row. It calls that row unplanned, which the canonical JSON ledger cannot represent. Add a positive ledger contract: include performed/relevant planned checks only; generic disabled-execution notes and optional suggestions go in limitations. If an unrun row remains with performed checks, summary is incomplete. Fresh refactor rerun requested; original retained, never silently overwritten.

Category nuance in Markdown used multiple labels; JSON schema needs one canonical category. Pin category vocabulary in the shared reference; narrative can carry nuance. Both-output checkout run independently exercises exact JSON shape and Markdown parity.

No safety-rule failure or rationalization was observed. Original inputs unchanged at dispatch; final digest verification is still required. Timing/token metadata is unavailable in completion messages, not estimated. Raw harness session IDs identify tool traces (see protocol.md).
