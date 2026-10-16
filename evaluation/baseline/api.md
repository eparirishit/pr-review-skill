# API change review

**Recommendation: request changes.** One high-priority compatibility regression conflicts with the stated goal of preserving existing clients.

## Findings

### [P1] Preserve the `display_name` response field

**Location:** `pr-review/tests/fixtures/api/after/services/users.py:2`

`user_response` now returns `name` instead of `display_name`, removing a field required by the unchanged TypeScript consumer in `apps/web/profile.ts:1–2`. When that consumer receives the new response, `user.display_name` is undefined and `.toUpperCase()` throws instead of rendering the label. Existing clients depending on the old field also lose compatibility. The TypeScript parameter annotation does not validate or adapt the Python response at runtime.

Keep `display_name` in the response. If `name` is needed, add it without removing the existing field; a coordinated client migration alone would not preserve existing clients. Add a response-contract regression test asserting that `display_name` remains present with the expected value, and cover the web label consuming that response.

## Scope and checks

- Reviewed the immutable before/after snapshots directly, not the working-tree diff.
- Read both versions of `services/users.py` and `apps/web/profile.ts`, including the unchanged consumer.
- The only observed change is the response key rename from `display_name` to `name`.
- Tools used: `read` for the invocation, fixture directory, and all four snapshot files; `glob` to enumerate fixture inputs; `patch` to write this report.
- Static inspection only: validation=none. No fixture code, tests, builds, type checks, or integrations were executed. No tool failures occurred.
- No design, skill, expected-findings, gold, or evaluation files were read. Fixture inputs were not modified.

## Limitations

The snapshots do not show HTTP wiring or other clients, so the exact transport path and broader client population are unverified. The producer/consumer field mismatch is directly visible in the supplied files.
