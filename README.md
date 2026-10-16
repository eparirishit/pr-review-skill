# PR Review Skill

A portable, requirements-first code-review skill for coding agents. Skill name: `pr-review`.

**Status:** design and implementation planning; the skill is not implemented or installed yet.

- [Design specification](docs/superpowers/specs/2026-10-15-pr-review-design.md)
- [Implementation plan](docs/superpowers/plans/2026-10-15-pr-review.md)

The reviewer will work with local repository context, optionally enriched through authorized Git hosting and ticket integrations. It will report evidence-backed findings without editing code, posting comments, or changing Git state.

Development happens here. After evaluation, install only the `pr-review/` skill directory into `~/.agents/skills/pr-review/`.
