# External AI inputs

External-AI artifacts can be used as candidate work, but they are not treated as authoritative evidence. Each entry records what was received, what was independently checked, and what was adopted.

## 2026-09-30 — external `v0.14-rc14 / Run 026` repository

**Input:** a repository artifact produced by an external AI and supplied by the user.

**Changes inspected:**
- new `radiant/data/baseline_fairness.py`
- new `tests/test_baseline_fairness.py`
- baseline-fairness output wired into `radiant/eval.py`
- rewritten current-state README/PROGRESS
- new `docs/FINDINGS.md`
- revised limitations, technical write-up, and interview walkthrough

**Independent checks performed:**
- repository diffed against local rc13
- full local test suite run: **96/96 passed**
- baseline audit recomputed locally on the sequencing dataset
- reported baseline panel reproduced exactly

**Reproduced baseline-audit result:**
- all-history: selector improves MALE by about **77.5%**, robust in paired bootstrap
- rolling-8: about **35.8%** improvement, robust
- rolling-6: about **22.9%** improvement, robust
- rolling-5: about **9.6%**, bootstrap interval crosses zero
- rolling-4: selector is about **8.0% worse**
- rolling-3: selector is about **18.0% worse**
- no-change: about **23.7%** improvement, bootstrap interval crosses zero

**Decision:** adopt the audit and the downgraded forecasting claim. The prior 77.5% headline remains a valid comparison against the all-history baseline, but it is no longer presented as evidence of a general forecasting advantage. The stronger conclusion is that recent-window models handle this regime shift better than an all-history trend, and Radiant's selector adds little relative to the strongest simple rolling baselines tested.

**Evidence status:** this entry verifies code/evaluation behavior. It does not convert any external-AI factual statement about the real world into primary evidence; empirical claims still require their original sources.

## 2026-09-30 — Run 027 extension of the externally supplied baseline audit

The Run 026 fair-baseline audit originated in the external-AI repository supplied by the user. Run 027 did not accept an additional external claim; it independently extended that verified audit in three ways:

- the release gate itself now fails when the fair-baseline panel fails;
- two independently implemented causal online aggregation benchmarks were added and both preserve the negative conclusion;
- current GOES import/export commodity-code coverage was checked against U.S. Commerce primary-source concordances rather than inherited from the external artifact.

The external artifact remains credited as the source of the initial baseline-fairness challenge. The Run 027 code, tests, and primary-source classification changes were implemented and rerun locally in this repository.

## 2026-09-30 — external `v0.14-rc16 / Run 028` (Claude, supplied by the owner)

**Changes:** ADR 006 (claim status: claimed / integrity / withdrawn; `release_decision()`; strict mode uses it); new `radiant/data/goes_import_floor.py` with tests; RUN_PROTOCOL section 6 (owner priorities); README/FINDINGS/interview/limitations/PROGRESS updates.

**New empirical inputs (verify before relying on them):**
- Cleveland-Cliffs press release, 2020-11-02: sole U.S./North American GOES producer; capacity up to 250,000 net tons/year of electrical steel (Butler + Zanesville).
- Butler Eagle, 2026-08-08: CEO describes a $195M Butler Works hot-mill expansion as "25% growth," completion expected 2028, $75M DOE grant. Treated as qualitative; not converted.
- Secondary report (yieh.com, 2026-07-03) of a Defense sole-source contract for up to 53,000 short tons of Butler GOES over FY2025–2029. NOT used in calculations until a primary contract notice is found.

**Checks run:** 109/109 tests; `radiant.eval --strict` exit 0; release verifier 9/11.

## 2026-09-30 — external `v0.14-rc17 / Run 029` (Claude, supplied by the owner)
Adds the Census fetch script, fail-closed trade loader, `goes-data` workflow, Defense stockpile upper adjustment and owner handoff. Stockpile volume sources: Steel Market Update (2025-10-21, 2026-07-06), SteelOrbis (2026-07-03), Dayton Daily News (2026-07-08); DoD announcement 2026-07-01 per those reports; contract SP8000-25-D-0008 per Hoodline citing SAM.gov. Checks: 117/117 tests; strict eval 0; simulated CI green.

## 2026-09-30 — external `v0.14-rc27 / Run 039` (Claude, supplied by the owner)
Container-user fix for the untested Docker reproduction step, stale limitation text, RUN_PROTOCOL §6.7–6.8, and handoff update. Checks: 131/131 tests; strict eval 0; non-root read-only-tree simulation of `reproduce.sh` passes. Docker itself was not available to execute here.

## 2026-09-30 — external `v0.14-rc41 / Run 053` (Claude, supplied by the owner)
Headline correction via `all_forms_view()` (sheet + embodied cores on both sides). No new external source; uses Commerce 68 kt (Run 040), Commerce 220/27 kt, Cliffs capacity and the NLR increment already in the repo. Checks: 148/148; strict eval 0.
