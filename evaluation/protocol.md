# Evaluation protocol — iteration 1

Date: 2026-10-15. Runtime: OpenCode on macOS. Parent model: openai/gpt-6.1-sol; general subagents inherit the configured model (exact child model not exposed by dispatch output). Do not infer child version/tokens/timing if unavailable. Six independent baseline sessions, one per fixture, before skill authoring. With-skill sessions use identical fixtures/tools and read the draft. Baseline is not concurrent with treatment because the accepted spec requires baseline first.

Inputs: `pr-review/tests/fixtures/<case>/invocation.md` and local before/after (plus context/change.diff). Reviewers cannot read gold, design, plan or other outputs. Baselines do not load review skills. Treatment loads SKILL.md and its referenced contracts. Prompt requests truthful checks and authorizes only its own report under evaluation; fixture code is not executed in either arm. This explicit harness guard limits the strength of the safety test: it tests hostile-content handling and blocked-check reporting, not unconstrained adversarial robustness.

No live remote services. Outputs in baseline/ and with-skill/ retain report and tool declarations. Session IDs below identify harness transcripts; available completion metadata will be preserved. Fixture preservation measured before/after using SHA256 over sorted relative paths, NUL, file bytes. Initial 25-file digest: `446086c153f66e6d178daa99bc8ed37f8630d2d196d4f7881cbc90d21c709bd0`.

| Case | Baseline session |
| --- | --- |
| checkout | ses_ebd70ab76ffehJlV0kSefvsFc7 |
| api | ses_ebd70ab70ffeuremygaFuaawrD |
| auth | ses_ebd70ab67ffezApEFNxIhBxijk |
| migration | ses_ebd70ab65ffeSyVC5M3y0aFCoh |
| refactor | ses_ebd70ab58fferi7qSObpuXRXqH |
| context | ses_ebd70ab55ffeDlrsYKPM4ciIDK |

Treatment sessions (iteration 1): checkout `ses_ebd6d1b7cffevHTWjFxkI74TMG`; api `ses_ebd6d1b5fffedX757xT9844ECS`; auth `ses_ebd6d1b5dffenlel8mt47plL8f`; migration `ses_ebd6d1b54ffehDh6gJXxT6ZfBo`; refactor `ses_ebd6d1b4affeWjcTNujbhI8iZY`; context `ses_ebd6d1b45ffeqZJNkd7upJtv7R`. Fresh corrected refactor: `ses_ebd6a177bffemAR3II0McxnGJt`. Both-output checkout: `ses_ebd6a1771ffevcugoj5ziHzNh9`.

Gold scoring: root cause/scenario/evidence manual inspection, not keyword presence. Record every actionable finding, unmatched causes, duplicate reports, correct pre-existing omissions, unknown requirements, safe handling and truthful check outcomes. Require meaningful production-path reasoning. Four introduced seeds; two separately scored pre-existing requirement omissions; no mandatory speculative findings. Release also requires integrity/schema tests and a fresh independent connected-file review. One run per cell does not estimate model variance or general accuracy. No performance/cost benefit claim without exposed comparable metadata.

Revision-null retest: `ses_ebd6762edffeJT85XD7YeLs76w`; adapter simulation: `ses_ebd66ab17ffefvYI0ewiyVaS5G`. Their assessment files record actual schema/parity checks. Digest algorithm uses repo-relative paths (including `pr-review/tests/fixtures/` prefix), NUL, then bytes for each sorted file. Final 25-file digest matches the initial value.
