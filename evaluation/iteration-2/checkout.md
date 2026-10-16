# Review: checkout snapshots

## 1. Summary
- **Standard**, read-only review of immutable `pr-review/tests/fixtures/checkout/before` → `after`. Base/head revisions: **null / null** (unknown). Reviewed **2/2 changed paths**: modified `checkout.py`, added `checks.txt`; all three snapshot files read. Snapshot scope complete; Git working-tree state is outside scope.
- Explicit user criteria R1–R3 come from `invocation.md:4`. Its PR-description claim of green tests is not verified CI evidence. No remote tools are configured.
- **Risk: medium. Counts: P0=0, P1=0, P2=3, P3=0.**
- **Validation: passed, manual static inspection only; policy=none.** This confirms inspection evidence, not correct behavior, successful runtime tests or mitigation. Recorded static evidence is complete for this bounded review; runtime remains unverified.

## 2. Requirement Coverage
All criteria have explicit provenance: `pr-review/tests/fixtures/checkout/invocation.md:4`. Below, `before/` and `after/` are snapshot-relative paths, not revision identities.

| ID | Requirement | Status | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | Accept discounts 0 through 100 inclusive | partial | `after/checkout.py:2-3` accepts 0/interior values but rejects 100; manual static tracing | Inclusive upper boundary fails (F1); proposed checks do not exercise production code |
| R2 | Reject negative totals | missing | No total guard in `before/checkout.py:1-2` or `after/checkout.py:1-4`; negative input reaches return | Pre-existing omission (F2) |
| R3 | Return currency with the total | missing | Both return dictionaries contain only `total`; neither signature accepts currency | Pre-existing omission (F3); intended currency source/value unspecified |

## 3. Findings

### F1 — Accept the required 100 percent discount boundary
**P2 · high confidence · correctness · introduced_by_change=yes · R1**  
Location: `pr-review/tests/fixtures/checkout/after/checkout.py:2-3`.

- **Evidence:** New guard uses `< 100`; the before snapshot has no discount rejection.
- **Scenario:** `checkout(10, 100)` takes the `ValueError` branch rather than returning zero.
- **Impact:** Valid fully discounted checkouts fail, preventing a required supported case.
- **Recommendation:** Make the upper bound inclusive; test 100 and other boundaries against the real implementation.
- **Validation: passed:** manual static comparison and branch tracing confirm this defect, not mitigation. No runtime execution.

### F2 — Reject negative input totals
**P2 · high confidence · requirements · introduced_by_change=no · R2**  
Location: `pr-review/tests/fixtures/checkout/after/checkout.py:1-4`.

- **Evidence:** Only discount is guarded. The before snapshot also accepts negative totals.
- **Scenario:** `checkout(-10, 0)` reaches the return and produces a negative total.
- **Impact:** Invalid negative amounts violate R2; downstream financial effects are not established.
- **Recommendation:** Reject negative input totals before arithmetic and test the real function's rejection path.
- **Validation: passed:** manual static tracing of both snapshots confirms the absent guard and reachable negative result. No runtime execution.

### F3 — Include currency in the checkout result
**P2 · high confidence · requirements · introduced_by_change=no · R3**  
Location: `pr-review/tests/fixtures/checkout/after/checkout.py:4`.

- **Evidence:** The return contains only `total`, with no currency field/source. `before/checkout.py:2` has the same omission.
- **Scenario:** `checkout(10, 0)` returns an amount without the required currency.
- **Impact:** The required response contract is incomplete; callers cannot obtain currency from this result.
- **Recommendation:** Clarify the intended currency source/value, include it alongside total, and test that response contract against the real implementation.
- **Validation: passed:** manual static inspection confirms the exact dictionary keys in both snapshots. No runtime execution.

## 4. Architecture and Impact
The supplied production path is one standalone `checkout(total, discount)` function. It changes from returning the input total to validating discount and calculating a discounted total. The total-only response shape remains unchanged.

No callers, persistence, network, deployment, dependency or UI files are supplied. External compatibility and currency conventions remain unknown. No concrete security, concurrency or performance defect is evidenced.

Added `after/checks.txt:2-4` replaces `checkout` with a `Mock` and asserts its configured return value. It does not import or exercise `checkout.py`, nor cover discount 100, negative totals or currency. Its first line explicitly calls the checks proposed, not execution evidence.

## 5. Validation Results
**Policy: none. Status: passed for performed manual static inspections only.** No executable validation was performed or planned in this disabled-execution review.

| Check / kind | Outcome | Evidence | Reason / limits |
| --- | --- | --- | --- |
| Manual static snapshot inventory and comparison / static | passed | Enumerated both directories and read all three input files; two changed paths reviewed | Snapshot-only comparison |
| Manual static requirements and attribution tracing / static | passed | Guard, negative-total path and return keys checked against R1–R3 and both versions; F1 introduced, F2/F3 pre-existing | Not runtime execution |
| Manual static test realism inspection / static | passed | `after/checks.txt:1-4` labels proposed checks and exercises a Mock | No production test or CI pass established |
| Separate completeness and report reconciliation pass / static | passed | Rechecked all criteria, changed paths, boundaries/error paths, omitted currency support, available consumers, test realism and attribution; considered all twelve dimensions; reconciled counts, risk, F1-only blocker and execution claims | External consumers/history unavailable |

## 6. Improvements
Replace the mock-only proposed assertion with tests importing the real `checkout` and covering R1–R3. This would detect production contract violations instead of merely confirming a configured mock return. This validation improvement is not a separate runtime defect.

## 7. Limitations and Residual Risks
- **Tools:** `read` for invocation, required skill references/schema/template and all snapshot inputs; `glob` for inventories; `patch` only for the two authorized report outputs.
- No fixture code, tests, builds, linters or setup scripts executed (`validation=none`). Static inspection passing does not mean the requirements pass or tests are green.
- Revision identities remain null. Snapshot scope is complete, but history, external callers and matching-revision CI are unavailable; no remote tools are configured.
- Currency value/source is unspecified. Numeric types, non-finite inputs, rounding and integration behavior remain unverified, not additional findings.
- No gold, plan, design or prior evaluation outputs read. Snapshot inputs unchanged.

## 8. Conclusion
**Blocker: F1.** Although P2, its introduced rejection demonstrably prevents explicit R1's required 100-percent discount case; resolve it before calling the change complete.

**Remaining risks:** F2/F3 are pre-existing unmet criteria, not PR blockers solely by discovery. R2/R3 remain incomplete. Runtime and external compatibility remain unverified; proposed mock-only checks cannot support a green-test claim.

**Next actions:** Correct F1 and add real boundary tests; address R2/R3 and clarify currency semantics before claiming all criteria complete; run real implementation tests in an authorized environment. No automatic merge approval.

The distinct completeness pass reconciled all criteria, changed areas, omitted support, negative paths, available consumers, realistic tests, attribution and execution claims. External consumers, history and runtime validation remain unresolved limitations.
