# Review: checkout before/after snapshots

## 1. Summary
- **Mode:** standard; **output:** Markdown; **validation:** none. Repository: `/Users/rishit.epari/Documents/repos/pr-review-skill`. Scope is exclusively the immutable `pr-review/tests/fixtures/checkout/before/` and `after/` snapshots, compared by matching path. Base/head Git revisions: unknown and unnecessary for this snapshot comparison. Locations below are snapshot-relative, not Git revision anchors.
- **Changed files reviewed: 2/2:** modified `checkout.py`; added `checks.txt`. No deleted files or other snapshot files were found. Git working-tree state was not inspected because it is outside this explicit snapshot scope; no checkout or revision substitution was used.
- **Intent/provenance:** explicit user criteria R1–R3 from `pr-review/tests/fixtures/checkout/invocation.md`: accept inclusive discounts, reject negative totals, and return currency. The supplied PR description claims completion and green tests; that claim has no execution evidence in these inputs. No remote tools are configured.
- **Overall risk: medium. Counts: P0=0, P1=0, P2=3, P3=0.** F1 is introduced; F2 and F3 are pre-existing unmet criteria, included in counts but excluded from change-risk derivation and blockers.
- **Validation: incomplete.** Manual static inspection was performed; executable checks were not run as requested. Proposed mock-only checks cannot establish production behavior.

## 2. Requirement Coverage
| ID | Requirement / provenance | Status | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | Accept discounts 0 through 100 inclusive; explicit user criterion, invocation.md:4 | partial | `after/checkout.py:2–4` accepts 0 and values below 100 but raises for 100. Manual static boundary trace. | Inclusive upper boundary fails (F1). No production-path boundary tests supplied. |
| R2 | Reject negative totals; explicit user criterion, invocation.md:4 | missing | `after/checkout.py:1–4` has only a discount guard; `checkout(-10, 0)` reaches the return and yields a negative total. `before/checkout.py:1–2` also lacks rejection. | Negative-total validation is absent, pre-existing (F2). |
| R3 | Return currency with the total; explicit user criterion, invocation.md:4 | missing | The sole return in `after/checkout.py:4` contains only `total`, as did `before/checkout.py:2`. | Currency is absent, pre-existing (F3). Required currency value and its source are unspecified. |

## 3. Findings

### F1 — Accept the fully discounted boundary
- **Severity:** P2. **Confidence:** high. **Category:** correctness / requirements. **Location:** `after/checkout.py:2–3`. **Requirement:** R1.
- **Evidence/scenario:** For `checkout(10, 100)`, `0 <= 100 < 100` is false, so the new guard raises `ValueError("discount")` instead of accepting the explicitly supported 100% discount and returning a zero total. The before snapshot had no rejecting guard.
- **Impact:** Fully discounted orders fail. This is a bounded but direct violation of required behavior, not a P1 incident.
- **Recommendation:** Make the upper bound inclusive and add production-function checks for 0, 100, and out-of-range discounts.
- **introduced_by_change:** yes.
- **Validation:** passed — manual static tracing confirms the branch and before/after attribution; no runtime reproduction was performed. This status confirms the finding's evidence, not a fix.

### F2 — Reject negative totals before returning a checkout result
- **Severity:** P2. **Confidence:** high. **Category:** correctness / input validation. **Location:** `after/checkout.py:1–4`. **Requirement:** R2.
- **Evidence/scenario:** `checkout(-10, 0)` passes the sole guard and returns `{"total": -10.0}`. No total-validation path exists anywhere in the supplied implementation. The before snapshot also accepted negative totals.
- **Impact:** The function returns an invalid negative checkout total contrary to the user contract. No downstream charge or persistence impact is established by these snapshots.
- **Recommendation:** Reject negative totals explicitly; test a negative input with a valid discount and retain zero-total acceptance.
- **introduced_by_change:** no — pre-existing omission; not a PR blocker solely because it was discovered here.
- **Validation:** passed — manual static tracing of the entire function and comparison with `before/checkout.py:1–2`; runtime checks not run.

### F3 — Include currency in the checkout result
- **Severity:** P2. **Confidence:** high. **Category:** response contract / requirements. **Location:** `after/checkout.py:4`. **Requirement:** R3.
- **Evidence/scenario:** A successful call such as `checkout(10, 0)` returns a dictionary with only `total`; no currency field or currency source exists in the supplied function. `before/checkout.py:2` had the same omission.
- **Impact:** Successful responses cannot fulfill the required total-with-currency contract. No actual downstream consumer failure is demonstrated.
- **Recommendation:** Establish the intended currency source/value, include currency in the response, and assert it through the real function. Do not invent a default currency from these inputs.
- **introduced_by_change:** no — pre-existing omission, not made introduced by the newly supplied criterion.
- **Validation:** passed — manual static inspection of both complete return paths; runtime checks not run.

## 4. Architecture and Impact
- The supplied production surface is one standalone Python function, `checkout(total, discount)`. The signature is unchanged; the implementation adds discount validation and calculation while retaining the single-key response shape.
- The new guard introduces a `ValueError` path; the calculation changes the returned amount for nonzero discounts. No callers, exports, service entrypoints, persistence, currency configuration, or deployment configuration are present in either snapshot. Compatibility beyond this surface is unknown rather than assumed safe.
- The only supplied apparent consumer is `after/checks.txt:2–4`, which creates its own `Mock` named `checkout`; it neither imports nor exercises the production function. Its assertion cannot validate the guard, calculation, negative-total handling, or currency contract.
- All twelve review dimensions were considered: requirements, scope, correctness, impact, and testing yielded the evidence above; architecture is limited to this function. Input validation is the concrete security-relevant concern, without evidence of an exploit. No persistence/concurrency, external I/O, dependency/build, or operational changes are present to justify deeper data-integrity, performance, supply-chain, or rollout investigation. No material maintainability issue was established; practical test improvements are separated below.

## 5. Validation Results
| Check / kind | Outcome | Evidence | Reason / limits |
| --- | --- | --- | --- |
| Snapshot inventory and matching-path comparison / static, manual inspection | passed | Enumerated both snapshot trees; read the before function, after function, and added checks file in full. Two changed files accounted for. | Snapshot comparison only; no Git refs or working-tree review. |
| Criteria and boundary tracing / static, manual inspection | passed | Traced `discount=0`, `discount=100`, `total=-10, discount=0`, and the successful response keys in `after/checkout.py:1–4`. | Establishes direct source properties and findings; not executed Python or integration validation. |
| Caller, guard, and test-evidence search / static, read/search | passed | Scoped search for checkout, currency, total, and discount in snapshot Python/text files found only the two implementations and the mock-only proposed check. | No production callers supplied; absence outside the snapshots is not claimed. |
| Distinct completeness reconciliation / static, manual inspection | passed | After initial investigation, rechecked all scoped references against R1–R3, both changed files, before/after attribution, response shape, negative path, and test substitution. Reconciled F1–F3, counts, risk, locations, and blocker selection. | Cannot resolve currency source or consumers absent from the inputs. |
| Production runtime, boundary, and regression tests / runtime | not_run | No test or fixture code executed. | Explicit `validation=none` and no-fixture-execution instruction. |
| PR claim: tests all green / runtime | not_run | Claim appears only in invocation.md:4; checks.txt:1 explicitly labels its contents proposed tests, not execution evidence. | No revision-matched external result, runtime output, or real-function test result supplied. |

Static checks marked passed mean the inspection was performed and supports its stated evidence; they do not mean requirements pass. Overall validation remains **incomplete** because production/runtime evidence is absent and the supplied mock check is insufficient. No test failures or runtime passes are claimed.

## 6. Improvements
- Replace or supplement the proposed `Mock` assertion with tests importing the real `checkout`. Assert inclusive discount boundaries, rejection of out-of-range discounts and negative totals, zero total, and currency presence/value. This closes the concrete evidence gap without counting missing tests as a separate defect.

## 7. Limitations and Residual Risks
- No code execution, tests, builds, linters, type checkers, remote requests, dependency installation, or input mutation was performed. Review conclusions are based on static evidence only.
- Scope contains no surrounding application, authoritative currency source, callers, or meaningful production tests. Broader API compatibility and end-to-end monetary behavior remain unverified.
- Supported numeric types, rounding, and non-finite input policy are unspecified; no additional defect is asserted from those unknowns. The correct currency cannot be chosen from the supplied criteria alone.
- The PR completion/green-tests assertion is not independently verified. Pre-existing F2/F3 remain unmet acceptance criteria even though they are not introduced regressions.

## 8. Conclusion
- **Material blocker: F1.** This introduced P2 demonstrably rejects an explicitly supported input, so it blocks satisfaction of R1 despite its bounded severity. Correct the inclusive boundary and obtain real-function validation.
- **Remaining required work:** address pre-existing F2 and F3 for the stated checkout-complete objective; agree the currency source/value. These are not retroactively attributed to this diff or used as introduced blockers.
- **Actual separate completeness audit:** after the initial finding investigation, the scoped search/reinspection reconciled all three criteria, both changed files, missing negative-total and currency paths, omitted supporting tests, mock realism, absent consumers/config/exports, before/after attribution, and every execution claim. Final reconciliation confirmed three P2 findings, medium introduced-change risk, incomplete validation, and only F1 as a material blocker. Currency sourcing and external compatibility remain unresolved because no relevant evidence was supplied.
- This report is review evidence, not automatic merge approval. Runtime checks and external consumers were not checked; no inputs were changed.
