# Review: shared user-response API snapshots

## 1. Summary
- **Mode:** deep; **output:** Markdown; **validation:** none; no integrations. Repository: `/Users/rishit.epari/Documents/repos/pr-review-skill`.
- **Comparison:** immutable `pr-review/tests/fixtures/api/before/` → `pr-review/tests/fixtures/api/after/`. Git base/head revisions are unknown and unnecessary for this snapshot comparison. All locations below are snapshot-relative, not branch line anchors.
- **Inventory:** 1/1 changed files reviewed (`services/users.py`); the sole unchanged consumer (`apps/web/profile.ts`) was also reviewed in both snapshots. No additions, deletions, renames, configuration, tests or generated files appear in the supplied snapshots.
- **Intent/provenance:** explicit PR intent from `pr-review/tests/fixtures/api/invocation.md:4`: simplify user lookup while preserving existing clients. No separate ticket or detailed simplification criteria were supplied. Client preservation is directly assessable; lookup simplification itself has no supplied lookup implementation or measurable acceptance criterion.
- **Overall risk:** **medium**. **Counts:** P0=0, P1=0, P2=1, P3=0.
- **Validation:** **incomplete** overall: static comparison and manual contract tracing completed; execution was disabled, and the actual HTTP/deserialization/integration path is not supplied. No runtime, build, lint, type-check or fixture code was executed.
- Initial read-only Git status showed untracked `pr-review/SKILL.md`, `pr-review/references/` and `pr-review/templates/`; these were not changed by the review. This is not a working-tree change review.

## 2. Requirement Coverage
| ID | Requirement / provenance | Status | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | Preserve existing clients; explicit PR intent, `invocation.md:4` | missing | Before `services/users.py:2` emits `display_name`; after line 2 replaces it with `name`. Unchanged `apps/web/profile.ts:1–2` requires and dereferences `display_name`. F1 documents the incompatible contract. | No compatibility alias, adapter or versioned response appears in the complete supplied scope. End-to-end wiring is unavailable. |

“Simplify user lookup” remains a stated objective, not an invented additional acceptance test: neither snapshot contains lookup logic, and its success cannot be established from a response-field rename.

## 3. Findings

### F1 — Preserve `display_name` for existing response consumers
- **Severity:** P2. **Confidence:** high. **Category:** API compatibility / correctness.
- **Location:** `after/services/users.py:2`; affected unchanged consumer: `after/apps/web/profile.ts:1–2`.
- **Evidence:** the producer previously returned `{"id": user.id, "display_name": user.name}` and now returns `{"id": user.id, "name": user.name}`. The consumer still executes `user.display_name.toUpperCase()`. Both consumer snapshots are identical. The supplied response has no `display_name` property and no supplied code restores it.
- **Triggering scenario:** an existing client passes the new response shape to its existing profile-label function, as it could with the old response. The required property is now absent; accessing it produces `undefined`, and calling `toUpperCase()` on that value throws. This is a static language-semantics trace, not an executed reproduction. A real boundary validator might reject the response earlier instead; either path is incompatible with the old contract.
- **Impact:** existing clients can no longer render the user label from the new response. This is a bounded client-breaking API regression, not evidence of a system-wide outage.
- **Recommendation:** retain `display_name` in the response for existing clients. If `name` is needed, add it without removing the old field and test the real serializer-to-client contract. Changing only this consumer would not preserve other existing clients.
- **Requirement:** R1. **introduced_by_change:** yes; the old response supplied the exact field still consumed, and the diff removes it.
- **Validation:** passed for manual static confirmation of the incompatible shapes and unchanged dereference. Runtime reproduction and actual endpoint wiring were not run/available; this status does not mean the defect is fixed.

## 4. Architecture and Impact
- The supplied architecture consists of a Python response-shaping function and a TypeScript label formatter. The shared boundary is a JSON-like object with `id` and a display-name string.
- This is a cross-language runtime contract: the local TypeScript parameter annotation does not rename Python response keys or validate external JSON. No generated contract, transport adapter or runtime guard is present in the supplied scope.
- The change leaves `id` and the source value `user.name` unchanged; the regression is the public key removal. The unchanged consumer, rather than just the changed Python file, establishes the impact.
- All twelve dimensions were considered: requirements, scope, correctness, architecture, downstream impact and test realism warranted the contract trace. No changed auth/input boundary, persistence/concurrency, resource/performance path, dependency/build configuration or deployment mechanism is shown. Maintainability does not justify an additional finding; rollout compatibility is covered by F1 rather than duplicated.

## 5. Validation Results
| Check / kind | Outcome | Evidence | Reason / limits |
| --- | --- | --- | --- |
| Scope discovery and dirty-state inspection / static | passed | `functions.glob` enumerated all four snapshot source files; `git --no-optional-locks status --short` recorded existing untracked skill material. No snapshot-local `AGENTS.md` was found. | Snapshot scope, not an inferred Git branch comparison; no files outside the permitted source snapshots were investigated for product behavior. |
| Snapshot diff inventory / static | passed | `git --no-optional-locks diff --no-index -- pr-review/tests/fixtures/api/before pr-review/tests/fixtures/api/after` showed only the response-key replacement in `services/users.py`. | Exit 1 denotes differences for this command, not a failed code check. |
| Producer/consumer manual tracing / static | passed | `functions.read` inspected both revisions of both files; `functions.grep` searched `user_response`, `display_name`, `.name` and `label` across snapshot Python/TypeScript sources. F1 follows directly from the incompatible shapes. | No additional callers, guards, adapters or tests exist in the supplied file inventory; actual integration wiring remains unknown. |
| Distinct completeness and report reconciliation pass / static | passed | After the initial investigation, re-read all four source snapshots; reconciled R1, the sole changed file, unchanged client, negative missing-property path, attribution, test/config omissions, F1 location/count and blocker rationale. | Did not turn unavailable lookup/transport evidence into an invented criterion or claim of runtime coverage. |
| Runtime reproduction, tests, type checking and build / runtime | not_run | None executed. | `validation=none` and explicit prohibition on fixture execution. These are limitations, not suggested commands represented as results. |

Tools used: `functions.read`, `functions.glob`, `functions.grep` and read-only Git discovery through `functions.shell`. `functions.patch` was used only to write this authorized report. No integrations, installs, network requests or fixture execution were used. The inspection checks passed; overall validation remains incomplete because production integration behavior is not validated.

## 6. Improvements
None separate from the compatibility repair and focused regression coverage recommended in F1. Missing tests alone are not a second defect.

## 7. Limitations and Residual Risks
- The snapshots contain only two source files each. No HTTP route, client fetch/deserialization code, API schema, integration tests, deployment policy or other external clients are available. F1 establishes a structural incompatibility; whether this exact formatter receives this exact endpoint response in production is not demonstrated.
- The amount and timing of production impact cannot be measured here. Additional clients may depend on `display_name`, but their existence is unverified and is not counted as another finding.
- No code was executed, so runtime error text, endpoint behavior and any external compatibility layer remain unverified. No CI evidence was supplied or queried.
- No design, plan, evaluation result, expected-findings material, JSON schema or adapter was read. The authorized output destination is not an evaluation input.

## 8. Conclusion
**Material blocker: F1.** Although P2, it directly prevents the explicit required behavior of preserving existing clients, so restoring the old response contract should precede treating this change as ready. Preserve `display_name`, then validate a real response against the unchanged client when execution is authorized.

The distinct completeness pass reconciled the sole criterion, every changed area, unchanged consumer, missing-property failure path, absence of snapshot tests/config/adapters, before/after attribution, all finding counts and execution claims. It left lookup simplification and actual production transport/rollout behavior unresolved because the required evidence is not supplied. This is not merge approval.
