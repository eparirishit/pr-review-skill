# Review: Customer migration snapshots

## 1. Summary
- **Mode:** deep; **output:** Markdown; **validation:** none.
- **Scope:** `pr-review/tests/fixtures/migration/before/` versus `pr-review/tests/fixtures/migration/after/`. These supplied snapshots define the comparison; Git base/head revisions are unknown, not inferred. Reviewed **2/2 changed files**: modified `schema.sql` and added `upgrade.sql`; also read the original schema.
- **Intent and provenance:** explicit requirements from `pr-review/tests/fixtures/migration/invocation.md`: preserve existing customers and emails (R1), and require email on new writes (R2). The invocation states that production is populated and no backfill or compatibility deployment is included. No ticket or remote context was supplied or queried.
- **Overall risk: critical.** Findings: **P0=1, P1=0, P2=0, P3=0**.
- **Validation: incomplete.** Manual static inspection establishes the destructive upgrade and the declared nullability constraint. No SQL, tests, builds, or other executable fixture validation ran. Database credentials are unavailable; actual database behavior and deployment execution remain unverified.
- Initial read-only Git discovery showed untracked skill/reference/template paths. These were neither modified nor used as a substitute for the snapshot comparison.

## 2. Requirement Coverage
| ID | Requirement / provenance | Status | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | Existing customer records and emails must survive upgrade. Explicit: invocation, line 2. | missing | `before/schema.sql:1` defines the existing customer table; `after/upgrade.sql:1-2` drops it and creates an empty replacement. The supplied upgrade has no data copy or restoration step. | Applying the upgrade to the stated populated production table destroys the records it must preserve; F1. |
| R2 | New writes must require email. Explicit: invocation, line 2. | verified | Both `after/schema.sql:1` and `after/upgrade.sql:2` declare `email TEXT NOT NULL`, directly establishing the database-level prohibition on missing/NULL email after successful schema application. | Static verification only; no database insert was run. This does not establish email format validation or rejection of empty strings, neither of which was requested. |

## 3. Findings

### F1 — Preserve populated customer data instead of dropping the table
- **Severity:** P0. **Confidence:** high. **Category:** data integrity / migration correctness.
- **Location:** `pr-review/tests/fixtures/migration/after/upgrade.sql:1-2` (after-snapshot relative evidence).
- **Evidence:** Line 1 is `DROP TABLE customers;`; line 2 recreates only the table structure with `email TEXT NOT NULL`. The original schema stores customer IDs and email values. There is no intervening preservation, copy, or restoration operation in the complete supplied upgrade. The invocation explicitly establishes that the production table is populated.
- **Triggering scenario:** Run the supplied upgrade successfully against the existing populated customer database. If the drop succeeds, the existing table and its contents are removed; a successful create produces a new empty table, not the old records with a strengthened constraint.
- **Impact:** Loss of all existing customer records and email values, directly violating the preservation criterion. P0 reflects destruction of the explicitly populated production data, not merely migration inconvenience. External dependency guards could instead reject the drop, but are not a data-preservation mechanism and are not evidenced here.
- **Recommendation:** Replace drop/recreate with an in-place migration that retains rows and email values. Establish a safe policy for existing NULL emails before enforcing `NOT NULL`; the old schema permits NULL and the supplied change includes no backfill. Reject or pause migration pending remediation rather than delete records. Validate on an isolated representative populated database, including rows with NULL email, before production execution.
- **Requirement IDs:** R1.
- **introduced_by_change:** yes. The destructive upgrade is newly added; the before snapshot only defines the original table.
- **Finding validation:** passed — manual static tracing and the snapshot diff confirm the new destructive statement and absence of preservation steps. This confirms the defect, not migration safety. No runtime reproduction or SQL execution was performed.

## 4. Architecture and Impact
- The complete supplied surface is SQL: a baseline table definition, its replacement definition, and a new upgrade script. No application layer, migration runner, callers, deployment configuration, or tests are present in these snapshots.
- `schema.sql` and the upgrade's recreated table agree on `id BIGINT PRIMARY KEY` and `email TEXT NOT NULL`. Fresh schema creation enforces R2, but that agreement does not validate the upgrade path or preserve existing rows.
- The changed contract is nullable-to-non-null email. Existing writers that omit email or send NULL will be rejected after upgrade. No compatible writer deployment is supplied; whether any such writer exists is unknown, not a separate established finding.
- The baseline allows NULL emails, so an in-place replacement migration must account for that possibility. Actual NULL counts, indexes, referencing tables, grants, triggers, and database-specific transactional DDL behavior are unavailable. None is needed to establish F1; none was invented as an additional defect.
- All twelve review dimensions were considered: requirements, scope, correctness, architecture, impact, testing, security, data integrity, performance, maintainability, operations, and improvements. Investigation concentrated on populated-data preservation, constraint semantics, writer compatibility, and migration failure/recovery. No supplied evidence supports a separate security, performance, or maintainability finding.

## 5. Validation Results
| Check / kind | Outcome | Evidence | Reason / limits |
| --- | --- | --- | --- |
| Read-only workspace discovery / static | passed | `git --no-optional-locks status --short` reported untracked `pr-review/SKILL.md`, `pr-review/references/`, and `pr-review/templates/`. | Git state was not changed; snapshot contents, not working-tree changes, define review scope. |
| Snapshot inventory and comparison / static | passed | Glob enumerated all three SQL snapshot files; `diff -ru .../before .../after` showed the one-line schema modification and the new upgrade script. | Diff exit code 1 denotes differences, not a failed validation. Two changed files, both reviewed. |
| Existing-data upgrade trace / static, manual | passed | Read baseline schema and both upgrade statements; traced drop followed by empty table creation. | Confirms F1 statically; not an executed database test. |
| New-write constraint trace / static, manual | passed | Both after definitions explicitly use `email TEXT NOT NULL`. | Establishes the declared constraint, not application integration or runtime deployment success. |
| Distinct completeness audit / static, manual | passed | Re-read both after files after initial investigation; reconciled their definitions against the original schema, both requirements, the complete diff inventory, and absent support files. | Actual production data and consumers remain unavailable; see sections 7–8. |
| Populated upgrade, preservation, NULL/omitted-email insert, and rollback checks / runtime | not_run | No SQL or fixture code executed. | Explicit `validation=none`; no database credentials. These are follow-up checks, not passing tests. |

Summary remains **incomplete**, not `issues_found`: all performed checks were static and completed successfully; they established a defect, but no executed check failed. Relevant runtime evidence remains absent.

## 6. Improvements
None separate from the required data-preservation fix and its validation. No speculative redesign recommended.

## 7. Limitations and Residual Risks
- Review is confined to the invocation and before/after SQL snapshots. No design, plan, evaluation, or expected-findings material was read. No external CI, ticket, or repository application code was consulted.
- No database credentials, engine/version, migration runner, production row samples, backup/restore guarantees, or referencing-object definitions were supplied. Runtime and integration behavior were not tested, and no rollback safety is claimed.
- Existing NULL email values are permitted by the baseline but not demonstrated in actual data. Their remediation is a prerequisite to safely enforcing the constraint, not proof of another current failure.
- Old-writer incompatibility is an unverified residual risk because no compatibility deployment is included and callers are unavailable. Confirm actual writer behavior before rollout; do not assume all writers are compatible.
- Destructive SQL was inspected only. No fixture execution, input edits, or service mutation occurred. The only authorized output is this report.

## 8. Conclusion
- **Material blocker: F1.** The introduced P0 upgrade discards the populated production customer table and cannot satisfy R1. Do not deploy this upgrade as supplied.
- Next actions: replace the destructive upgrade with a preserving migration; determine how to handle existing NULL emails and incompatible writers; then, with separate authorization and an isolated database, verify row/email preservation, required-email writes, failure behavior, and recovery.
- A **distinct completeness pass was performed**, not assumed: after the initial finding, both after files were re-read and reconciled with the original schema and diff. It checked R1/R2, additions and omissions, fresh-install versus existing-data transitions, negative NULL writes, absent migration/backfill/deployment/test support, unavailable consumers, before/after attribution, exact line anchors, severity counts, blocker IDs, risk, and actual execution claims. It found no second independently established defect. Production NULL prevalence, writer behavior, and database execution remain unresolved.
- This is evidence for a human review decision, not automatic approval. Runtime validation was deliberately skipped; production data loss is the established risk.
