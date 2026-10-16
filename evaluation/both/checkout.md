# Review: Checkout snapshots

## 1. Summary
- **Mode:** standard; read-only inputs; output overridden to both; validation policy `none`.
- **Scope:** `pr-review/tests/fixtures/checkout/before` → `pr-review/tests/fixtures/checkout/after`, immutable snapshots; Git revisions unknown. Reviewed **2/2 changed paths**: modified `checkout.py`, added `checks.txt`. Snapshot scope complete.
- **Context:** explicit user criteria from `pr-review/tests/fixtures/checkout/invocation.md:4`; all three available. Only supplied snapshots reviewed; external callers, Git revisions and remote CI unavailable.
- **Risk: medium.** Counts: P0=0, P1=0, P2=3, P3=0. Two findings are pre-existing; only F1 determines introduced-change risk.
- **Validation: incomplete.** Manual static inspection performed; no code checks or runtime execution. The PR's green-test claim is not substantiated.

All abbreviated `before/` and `after/` anchors below are relative to `pr-review/tests/fixtures/checkout/`.

## 2. Requirement Coverage
| ID | Requirement / provenance | Status | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | Accept discounts 0 through 100 inclusive; explicit user, `invocation.md:4` | partial | `after/checkout.py:2-4` accepts 0 ≤ discount < 100, but raises at 100. | Required upper boundary rejected; runtime unexecuted. |
| R2 | Reject negative totals; explicit user, `invocation.md:4` | missing | `after/checkout.py:1-4` lacks total validation; total=-10, discount=0 reaches a negative return expression. `before/checkout.py:1-2` also lacks rejection. | Pre-existing omission. |
| R3 | Return currency with the total; explicit user, `invocation.md:4` | missing | `after/checkout.py:4` and `before/checkout.py:2` return only the total key. | Pre-existing omission; currency value/source unspecified. |

## 3. Findings

### F1 — Accept the required 100-percent discount boundary
- **P2 · high confidence · correctness · introduced_by_change: yes · R1**
- **Location:** `pr-review/tests/fixtures/checkout/after/checkout.py:2-3`.
- **Evidence:** the new guard uses `discount < 100`; the before snapshot had no discount rejection.
- **Scenario:** `checkout(10, 100)` takes the `ValueError` branch instead of returning a zero total.
- **Impact:** valid fully discounted orders fail, violating R1's inclusive upper boundary.
- **Recommendation:** use an inclusive upper bound and add production-function checks for 0, 100 and out-of-range discounts.
- **Validation: passed (manual static confirmation only).** Traced `after/checkout.py:2-4` and compared `before/checkout.py:1-2`. No execution; this does not mean the defect is mitigated.

### F2 — Reject negative totals before calculating the result
- **P2 · high confidence · requirements · introduced_by_change: no · R2**
- **Location:** `pr-review/tests/fixtures/checkout/after/checkout.py:1-4`.
- **Evidence:** only discount is validated; total reaches the return expression unchecked. The before snapshot also accepts negative totals.
- **Scenario:** `checkout(-10, 0)` passes the guard and returns a negative total instead of rejecting input.
- **Impact:** the contract permits invalid negative totals despite R2; downstream charging behavior is not established.
- **Recommendation:** reject negative totals at the function boundary; test a negative value and zero using the actual function.
- **Validation: passed (manual static confirmation only).** Both snapshots confirm the missing guard and negative return path. No execution.

### F3 — Include currency in the checkout result
- **P2 · high confidence · requirements · introduced_by_change: no · R3**
- **Location:** `pr-review/tests/fixtures/checkout/after/checkout.py:4`.
- **Evidence:** the sole return dictionary has only a total key in both snapshots.
- **Scenario:** a successful `checkout(10, 0)` returns a total without currency.
- **Impact:** consumers cannot obtain the required currency from the result; R3 is unmet.
- **Recommendation:** confirm the intended currency value/source, include currency in successful results, and assert both fields using the real function.
- **Validation: passed (manual static confirmation only).** Inspected complete return dictionaries before and after. No execution.

## 4. Architecture and Impact
- The complete supplied implementation is one `checkout(total, discount)` function returning a dictionary. `checkout.py` is modified and `checks.txt` added; no other snapshot files exist.
- The change adds discount rejection and percentage arithmetic, affecting callers that previously received the unchanged total. Rejection at 100 is introduced; missing total validation and currency predate it.
- `after/checks.txt:2-4` replaces `checkout` with `Mock` and asserts its configured result. It neither imports nor calls production code and cannot substantiate the PR's green-test claim.
- All twelve dimensions were considered. Requirements, correctness, input validation, output compatibility and test realism have concrete evidence. No persistence, concurrency, UI, dependencies, deployment configuration or external consumers are present to assess further.

## 5. Validation Results
**Policy:** `none`. **Evidence incomplete:** true. **Summary:** `incomplete` because runtime/integration evidence is absent, despite performed manual static checks.

| Check / kind | Outcome | Evidence | Reason / limits |
| --- | --- | --- | --- |
| Manual static snapshot comparison and requirement tracing / static | passed | Read both `checkout.py` snapshots and `after/checks.txt`; traced R1–R3 and before/after attribution. | Manual confirmation of defects, not passing implementation tests; no executable tooling. |
| Manual inspection of proposed test realism / static | passed | `after/checks.txt:1` labels checks proposed, not execution evidence; lines 2–4 exercise only Mock. | No execution. |
| Separate manual completeness and report reconciliation pass / static | passed | Reconciled three criteria, both changed paths, success/rejection paths, absent support files/consumers, attribution, three P2 counts, F1 blocker and static-only claims. | Currency source and external/runtime behavior remain unresolved. |

No code checks were executed. Generic disabled execution is disclosed as a limitation, not represented as invented planned ledger checks. No remote CI pass is claimed.

## 6. Improvements
**Replace the mock-only proposed check with checks importing the production `checkout` function.** This would detect the discount boundary and unmet total/currency contracts instead of merely confirming mock configuration. Rationale: `after/checks.txt:2-4` shadows the function with Mock. This is a non-blocking testing improvement, not a separate confirmed production defect.

## 7. Limitations and Residual Risks
- No tests, builds, linters, type checkers, fixture code or other code checks were executed (`validation=none`). Only manual static reading and comparison were performed.
- Runtime/integration evidence is incomplete. The PR's green-test assertion has no matching execution record, revision or genuine production-function check in scope.
- Only the fixture invocation and before/after inputs were reviewed, alongside required skill references and report templates. No design, plan, gold, expected-findings or evaluation material was read.
- Git dirty state and revisions were not inspected: immutable snapshots define the entire requested comparison. The wider repository and external callers are outside scope.
- Currency value/source is unknown. No financial precision or downstream charging defect is established.
- Inputs were not mutated; only the two authorized report destinations were written.

## 8. Conclusion
- **Blocker: F1.** Although bounded P2 impact, the introduced rejection of 100 demonstrably prevents explicitly required R1 behavior.
- **Remaining risks:** pre-existing F2 and F3 leave R2 and R3 unmet, but are not change-introduced blockers. Runtime behavior, external consumer compatibility and currency source remain unverified.
- **Next actions:** fix the inclusive boundary and add actual production-function boundary checks; resolve negative-total/currency gaps against the criteria, confirming currency source; execute meaningful implementation tests only when separately authorized.
- The distinct completeness pass reconciled criteria, changed areas, omissions, tests, consumers, attribution, counts, risk, blockers, locations and execution claims. External/runtime context and currency source remain unresolved. This report supports a human decision; it is not merge approval.
