---
name: pr-review
description: Use when reviewing a pull request, merge request, branch, commit, working-tree change or supplied diff, including reviews against ticket acceptance criteria, API/database changes, regression risk, architecture fit or test meaningfulness.
---

# PR Review

Determine whether a change safely fulfills its intent in the surrounding system. Produce evidence for a human decision, not a volume of findings or an automatic approval.

## Start here

1. Read [safety and validation](references/safety-and-validation.md) **before commands**. Read-only is invariant; `read_only=false` is unsupported, not permission to fix anything.
2. Normalize the request using the table below. Preserve repository root, scope, revisions, changed-file inventory, story provenance, applicable project instructions and available tools. Keep unavailable context unknown.
3. Read [workflow](references/workflow.md), [requirements](references/requirements-traceability.md) and [severity](references/severity-and-confidence.md). Execute phases 0–8, including the separate completeness pass.
4. Consider all twelve [dimensions](references/review-dimensions.md); read that reference and deepen applicable risks rather than performing twelve exhaustive audits.
5. Read [report contract](references/report-schema.md); fill [Markdown report](templates/review-report.md), or use [JSON schema](templates/review-report.schema.json) for JSON/both. Report in conversation unless an output destination is authorized.

## Invocation defaults

| Setting | Default | Meaning |
| --- | --- | --- |
| mode | standard | `quick`, `standard`, `deep`, `requirements` |
| output | markdown | `markdown`, `json`, `both` |
| validation | auto | `auto` assesses safe checks; `none` disables executable validation, not reading/search |
| base_ref / head_ref | unknown | Resolve supplied revisions; never guess the intended comparison |
| story | optional | User criteria first; optional ticket/PR context; then commits/docs/code with provenance |

Quick covers requirements, immediate consumers and highest-risk paths with omissions disclosed. Standard traces relevant changed areas and affected contracts. Deep follows concrete cross-system, failure and operational risks. Requirements prioritizes every criterion's implementation/test evidence while retaining material defects and disclosing other omissions. All modes use the same safety and evidence standards.

Use only configured, authorized tools. No tool, Git host or ticket system is required: explicit snapshots/diffs support standalone review. For remote context, read the applicable optional guide: [Git providers](adapters/git-providers.md), [tickets](adapters/ticket-systems.md), [validation tools](adapters/validation-tools.md). Missing integrations become limitations, not a setup project.

## Completion contract

Every criterion has one evidence-backed state. Every actionable finding has severity, independent confidence, evidence, scenario, impact, recommendation, attribution and truthful validation. Keep improvements and unverified residual risks separate. Reconcile counts, revision/line anchors, blockers and risk using the report reference. Stop after scoped investigation and the distinct completeness pass; disclose what remains unknown.

## Common mistakes

- Passing mock-only assertions do not validate production behavior; inspect the path exercised.
- Missing tests do not prove missing implementation. Inaccessible criteria are not absent criteria.
- A pre-existing omission can violate today's criteria without being introduced by this diff.
- Severity describes impact, not urgency of the review request. Ordinary bounded gaps are not automatically P1.
- Empty findings mean no actionable defect established in inspected scope, not merge approval or full coverage.
