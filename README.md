# PR Review Skill

A portable, requirements-first code-review skill for coding agents. Skill name: `pr-review`.

**Status:** implemented on `feat/pr-review-skill`; independent review completed and its Important finding fixed. Human acceptance pending. Not installed or published.

The reviewer works with local repository context, optionally enriched through authorized Git hosting and ticket integrations. It reports evidence-backed findings without editing code, posting comments, or changing Git state. No runtime engine, dependency installation, GitHub access or Jira access is required.

## Use

Load [`pr-review/SKILL.md`](pr-review/SKILL.md) in an agent supporting Markdown skills, then ask naturally:

- “Review this branch against main; standard mode, no executable validation.”
- “Review this supplied diff against these acceptance criteria; output both JSON and Markdown.”
- “Deep-review this API and migration change, including unchanged consumers.”
- “Quick review of this commit; preserve my dirty workspace.”

Modes: `quick`, `standard` (default), `deep`, `requirements`. Output: Markdown (default), JSON, both. Validation: `auto` (assess safe checks) or `none` (manual static inspection only). Supply an unambiguous target/comparison; unknown revisions and missing context remain explicit. `read_only=false` is unsupported.

The eight-section report separates requirements, actionable P0–P3 findings, impact, validation, improvements and limitations. Empty findings are not merge approval. A static confirmation is not a runtime pass. Optional [capability guides](pr-review/adapters/) cover Git providers, ticket systems and validation tools without hard-coded tool dependencies.

## Verify and inspect evidence

```sh
python3 -m unittest discover -s pr-review/tests -p 'test_*.py' -v
```

Report tests use the Python standard library; the full Draft 2020-12 schema test additionally uses `jsonschema` if already available. The viewer-handler regression uses an available Node executable. Both optional checks explicitly skip when unavailable; no installation is automatic. The cross-field helper is not a substitute for full schema validation or behavioral evaluation. It currently does not reject performed runtime checks under `validation=none`; the review's safety contract still forbids them, so check this combination manually.

See [evaluation protocol](evaluation/protocol.md), [manual grades](evaluation/grades.json), baseline and with-skill reports. Initial defects and retests are retained. Tests exercise meaningful review behavior on fixed small snapshots; they do not prove general accuracy or production safety. Tested harness: OpenCode/macOS, parent `openai/gpt-6.1-sol`; exact child model/timing metadata unavailable. Other hosts and live GitHub/Jira/CI integrations are not tested.

## Install only after approval

Development happens here. After evaluation and explicit approval, manually copy **only `pr-review/`** to `~/.agents/skills/pr-review/` if that destination does not already exist. Do not overwrite an existing installation; compare it first. Do not copy `evaluation/`, `.git/`, or development plans. Runtime skill discovery depends on the host's supported skill directory; standalone use can load `SKILL.md` directly.

Installation, remote repository creation and publishing are separate actions; none is performed by this project. Human review of the evaluation outputs is still required before accepting the skill for use.
