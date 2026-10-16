# Checkout PR review

**Decision: Request changes.** Static comparison of the matching before/after snapshots found three unmet acceptance criteria.

## Findings

1. **[P1] Accept a 100% discount (R1)** — `pr-review/tests/fixtures/checkout/after/checkout.py:2`
   The upper bound is exclusive, so `checkout(10, 100)` raises `ValueError` rather than accepting the required 100% discount and returning a zero total. Change the bound to include 100; preserve rejection outside 0–100.

2. **[P1] Reject negative totals (R2)** — `pr-review/tests/fixtures/checkout/after/checkout.py:4`
   No validation checks the input total. For example, `checkout(-10, 0)` returns a negative total rather than rejecting it. Validate the input total before calculating the discount, including when the discount would otherwise hide a negative input.

3. **[P1] Return currency alongside the total (R3)** — `pr-review/tests/fixtures/checkout/after/checkout.py:4`
   The returned dictionary contains only `total`, so every successful call omits the required currency. Establish the intended currency source (the supplied interface has no currency parameter or default) and include it in the response. The requirement does not specify a currency value, so this review does not assume one.

## Validation and evidence

- Mode: standard; output: Markdown; validation: none.
- Tools used: `functions.read` to inspect the invocation, list the input directories, and read both `checkout.py` snapshots and `after/checks.txt`; `multi_tool_use.parallel` to group independent reads; `functions.patch` to write this review.
- Executed checks: none. No fixture code, tests, shell commands, or remote tools were executed.
- `after/checks.txt:1–4` explicitly describes proposed tests, not execution evidence. It replaces `checkout` with a `Mock` and asserts that mock's configured response; it does not exercise the implementation or establish any acceptance criterion. The PR's “tests all green” claim is therefore unverified by the supplied material.
- Tool failures: none.

Skipped runtime validation as requested; no inputs were modified. Approval remains blocked by R1–R3, and the intended currency value/source needs clarification.
