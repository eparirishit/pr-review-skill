# Final independent review — f502c7a..676a04c

## Strengths

- The small entrypoint and six connected references implement a coherent requirements-first review, including unchanged consumers, before/after attribution and a distinct completeness pass. Optional adapters preserve the same safety and uncertainty rules rather than requiring providers.
- Safety explicitly covers dirty work, ambiguous revisions, imports/hooks/caches/network effects, hostile repository text and authorized report destinations. The selected reports actually apply these distinctions; they do not merely repeat instructions.
- Independently checked the six fixture comparisons against baseline/treatment outputs, gold expectations and selected retests. The four introduced causes and two pre-existing checkout omissions support the declared 4/4 introduced recall and 6/6 actionable precision **on this small suite**. No detection lift over baseline is demonstrated or claimed. Retained failures and retest selection are transparent.
- The final JSON/Markdown checkout pair agrees on findings, requirement states, attribution, counts and blockers. The context reports preserve unavailable criteria, partial scope, unknown revisions and stale CI without inventing findings or locations. Human feedback, live-provider testing and installation remain explicitly pending; those disclosures are not fabricated success.

## Issues

### Critical

None established.

### Important

**F1 — HTTP errors silently discard viewer feedback while reporting success.**

- **Location:** `evaluation/review.html:1012-1021`, `evaluation/review.html:1044-1059`.
- **Evidence/scenario:** Both feedback POST handlers enter their success continuation on any resolved `fetch`, without checking `Response.ok`. A normal static HTTP server without `/api/feedback` returns an HTTP error (commonly 404/405/501); `fetch` resolves for those responses. Autosave therefore says “Saved,” and final submission shows the completion overlay instead of downloading `feedback.json`. The download fallback only handles rejected requests, not HTTP errors. Opening the file directly may reject the request and work, but serving the same artifact statically exposes this failure.
- **Impact:** A human can complete the requested evaluation believing feedback is retained when nothing was saved or exported, then lose it on closing/reloading. This breaks the human-review handoff rather than the review skill itself.
- **Recommendation:** Check `response.ok` before either success action; route unsuccessful responses through the existing download/error fallback. Add a small report-viewer check covering HTTP error responses as well as a successful save.
- **Confidence/attribution:** High; introduced by this branch. Established by source inspection and standard Fetch response semantics; no browser/server/network execution performed.

### Minor

**F2 — Integrity checks accept executed runtime validation under `policy=none`.**

- **Location:** `pr-review/tests/test_report_integrity.py:49-60`; connected schema: `pr-review/templates/review-report.schema.json:99-106`.
- **Evidence/scenario:** Starting with `tests/reports/valid.json`, changing its single passed check's `kind` from `static` to `runtime` leaves `policy=none`. Both the full Draft 2020-12 validator and `assert_report_integrity` accept it. This was independently reproduced using report data only. The derivation checks outcomes but never checks the policy/kind incompatibility.
- **Impact:** The advertised structural gate misses a directly machine-checkable violation of disabled executable validation. The core safety reference still prohibits it, and no inspected selected report committed this violation; consequently this is a bounded integrity-test gap, not evidence that unsafe checks ran.
- **Recommendation:** Reject performed runtime checks (`passed` or `failed`) under `policy=none`, with a regression case. Preserve allowed manual static checks and unrun/blocked records. This cannot by itself distinguish manual inspection from executable static tooling; retain that documented semantic-review limitation.
- **Confidence/attribution:** High; introduced by this branch. Safe report-only reproduction confirmed acceptance of the invalid combination.

## Review Focus

- Dirty workspace and ambiguous revisions: protected user work and no guessed base; Task 1/2 safety cases.
- Ticket unavailable versus absent: preserve uncertainty without invented criteria; Task 1/2 context cases.
- Tests with hidden writes/network effects: inspect/isolate or block, never assume safe; Task 1/2 safety cases.
- Missing line numbers and pre-existing bugs: no invented locations or new-defect attribution; Task 1/3 report cases.
- Partial coverage with no findings: disclose incompleteness rather than imply clean approval; Task 1/3/5 cases.

### Focus assessment

1. **Dirty work/revisions:** Core contracts prohibit checkout/reset/stash and guessed comparisons. Auth/context outputs preserve supplied dirty-state facts; snapshot scopes and null revision identities are explicit. Actual dirty Git preservation was simulated, not independently exercised by these behavioral fixtures.
2. **Ticket uncertainty:** Context and adapter outputs retain denied versus absent capability, ambiguous ticket links and unknown criteria. No invented expiry criteria or missing-implementation defect was counted.
3. **Validation effects:** Auth output reads and blocks the file-writing/outbound-POST script and rejects malicious notes. Core guidance also covers imports/hooks and less obvious side effects. This fixture advertises its unsafe contents and the evaluation harness independently prohibits execution, so it supports bounded handling, not unconstrained safety robustness.
4. **Locations/attribution:** Context avoids target line invention. Checkout distinguishes one introduced defect from two pre-existing omissions; refactor does not blame the rename for unchanged empty-input behavior. Original snapshot-label revision fields remain retained as an acknowledged failure; the selected pair corrects them to null.
5. **Incomplete/no findings:** Context and adapter reports explicitly use incomplete risk/validation, unknown total file count, no established blockers and no approval. The refactor's complete bounded static comparison is separately justified. Static-only “passed” labels in selected retests explicitly deny runtime success and follow the accepted contract.

## Verification and evidence

- Read the supplied reviewer guidance, design, actual plan at `docs/superpowers/plans/2026-10-15-pr-review.md`, review package and ledger Ruling lines. The abbreviated requested `plans/2026-10-15-pr-review.md` path does not exist; the ledger identifies the actual path.
- Connected inspection covered entrypoint, all references/adapters, both templates, helper/tests/examples, fixture source and invocations, baseline/treatment reports, selected retests, adapter simulation, evaluation protocol/grades/benchmark/evals, README and viewer logic/embedded data. The ledger's explicit rulings on sequential baseline, overlapping independent tasks and combined fixtures do not create an undisclosed implementation deviation.
- Ran `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s pr-review/tests -p 'test_*.py' -v`: **23 tests passed**, including the optional full-schema test; no skips.
- Separately ran full-schema plus cross-field checks on the valid example, selected checkout JSON, adapter JSON and retained original both-output JSON: all pass structurally. The original revision-label issue is semantic and correctly disclosed, not caught by those validators.
- Recomputed fixture digest: **25 files**, `446086c153f66e6d178daa99bc8ed37f8630d2d196d4f7881cbc90d21c709bd0`, matching the recorded digest. Read fixture contents only; did not import/execute fixture code, scripts or migrations.
- Parsed the viewer's embedded JSON as data: all **12** embedded report texts match the selected baseline/treatment files, and its embedded benchmark matches `evaluation/benchmark.json`. No claim of browser interaction testing follows from this check.
- Reconciled severity/precision/recall denominators against the actual reported causes. Composite viewer assertion rate is correctly disclosed as different from defect recall; no speed/cost or repeated-run variability claim is justified or made.

## Recommendations

Fix F1 before asking the user to rely on viewer submission. Close F2's small structural blind spot without introducing a review runtime. Keep original evaluation outputs immutable and rerun affected report/viewer checks after fixes. Preserve the existing approval/install boundary.

## Declined to judge

[] — No considered behavior was excluded merely because the specification was silent. Unperformed integration/browser/adversarial checks are limitations, not favorable judgments.

## Assessment

**Ready to merge? With fixes.** The portable core and declared bounded behavioral scores are well supported; no critical core-review defect was established. The human-feedback handoff has a real loss path that should be corrected before acceptance, and the integrity helper has one small enforceable policy gap. This is not installation approval or a claim of general reviewer accuracy.

## Limitations

No fixture execution, network access, browser loading, live providers, installation, source edits or Git-state changes were performed. Browser behavior for F1 was traced statically, not reproduced interactively; raw historical session tool traces were not independently replayed, so historical safety claims remain bounded by retained reports, session identifiers and fixture hashes. Only this authorized report was written.

Human feedback remains pending. Broad repositories, real dirty-worktree reviews, isolated runtime validation, hidden side-effect/adversarial trials and other harnesses remain untested rather than implicitly passed.
