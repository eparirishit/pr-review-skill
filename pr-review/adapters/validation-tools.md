# Validation capabilities (optional)

Use the safety reference before selecting any check. `validation=none` allows manual reading/search/tracing and scope discovery, not tests/builds/linters/type checkers. `auto` is assessment, not consent to arbitrary execution.

Discover the existing toolchain from project evidence. Read candidate scripts, imports, hooks and configuration; account for writes, caches/bytecode, subprocesses, network, credentials and databases. Prefer a focused meaningful check through the real changed path. Mock-only assertions and stale CI do not validate production behavior.

Run only checks with known effects inside host authorization and read-only target boundaries. Writes need an authorized isolated output/sandbox; changing the target repository or external services is not an acceptable workaround. Missing tools/dependencies/isolation or unsafe hooks mean blocked checks, not silent installation, downloads or elevated access. Continue static review and explain the uncovered behavior.

For performed and relevant planned checks preserve name, static/runtime kind, actual outcome, evidence, revision when known and blocked/not-run reason. Manual static confirmation is not runtime execution. A reproduced failing test stays failed. Keep optional suggestions/generic disabled execution out of the checks ledger and in limitations; derive summary using the shared report contract. No remote comment, fix, deployment or data mutation is part of validation.
