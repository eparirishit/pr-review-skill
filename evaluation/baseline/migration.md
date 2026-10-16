# Customer migration review

**Verdict: Block deployment.** The upgrade destroys existing customer records and emails, violating R1. Reviewed in deep mode using static inspection only; validation=none.

## Findings

### [P0] Preserve the populated customer table instead of dropping it

**Location:** `pr-review/tests/fixtures/migration/after/upgrade.sql:1–2`

The upgrade unconditionally executes `DROP TABLE customers` and recreates an empty table. Since production is populated, a successful upgrade removes every existing customer ID and email. Recreating the same columns does not restore those rows. This directly violates R1 and is a deployment blocker regardless of whether existing emails contain NULLs.

Replace the destructive recreation with a data-preserving migration. The old schema permits NULL emails, so simply applying `NOT NULL` in place is not a complete migration strategy: any existing NULLs would prevent that change from succeeding. Establish a policy that preserves existing records and emails while rejecting missing emails on new writes, and provide any required staged enforcement or remediation before deploying. No backfill or compatibility deployment is included in the supplied inputs.

## Requirement assessment

- **R1 — existing customer records and emails survive upgrade:** Fails by inspection of the unconditional drop/recreate.
- **R2 — new writes require email:** The resulting schema declares `email TEXT NOT NULL`, which rejects NULL and omitted email values, but does not make the destructive upgrade acceptable. Empty-string rejection was not specified.
- **Existing NULL emails:** Possible under the before schema; their actual presence is unknown. No database access or data profile was available.

## Scope, tools, and checks

- Read `pr-review/tests/fixtures/migration/invocation.md` and listed only its fixture directory and the before/after directories to locate inputs.
- Read the complete supplied snapshots: `before/schema.sql`, `after/schema.sql`, and `after/upgrade.sql`.
- Compared the schemas and traced both upgrade statements statically against the stated populated-production condition and R1/R2.
- Tools used: `read`, `multi_tool_use.parallel` for independent reads, and `patch` solely to save this report. All succeeded.
- No fixture code executed, inputs mutated, database connections attempted, or tests run. No review skills, design files, other evaluation files, expected findings, or gold files were read.

Not checked: live data, SQL-engine-specific behavior, rollback, or application callers; validation was explicitly disabled and no database credentials were available.
Risk: deploying the supplied upgrade successfully loses all existing customer records and emails.
