# Twelve review dimensions

Consider each for relevance; deepen concrete risks, not every hypothetical audit.

| Dimension | Investigation prompts |
| --- | --- |
| Requirements | Criteria, constraints, incomplete paths; explicit versus inferred intent |
| Change scope | Full diff inventory, deletions/renames/generated/config, omitted work, scope drift |
| Correctness | Inputs/boundaries, state transitions, errors/retries, cleanup/resource lifecycle |
| Architecture | Existing boundaries and dependency direction evidenced by code; fit without speculative redesign |
| Impact | Unchanged callers/consumers, API/events/data contracts, compatibility and blast radius |
| Testing | Actual production paths, useful assertions, mock realism, negative/boundary/regression behavior |
| Security | Authn/authz, privacy, untrusted inputs, secrets, injection and dependency/supply-chain changes |
| Data integrity | Transactions, populated migrations/rollback, concurrency, idempotency, ordering and persistence |
| Performance | Complexity, query/I/O counts, bounded resources, representative workload and scale assumptions |
| Maintainability | Material unnecessary complexity or convention violations; not taste/style |
| Operations | Deploy/config compatibility, observability, recovery, reproducible builds and rollouts |
| Improvements | Practical non-blocking gains, separated from confirmed defects |

Auth changes merit tracing every trust boundary and bypass. Shared API changes merit unchanged consumer inspection across languages/packages. Migrations merit existing data and staged deployment reasoning without executing destructive statements. Concurrency merits interleavings and retry/idempotency failures. UI changes merit state, keyboard/accessibility and failure paths. Build/dependency changes merit lifecycle scripts and supply-chain effects. Prefer concrete evidence and scenarios over generic checklist findings.
