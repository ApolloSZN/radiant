# Radiant standing run protocol

This protocol applies to every substantive Radiant work session.

## 1. Fix what is broken or weakest first

Before adding new capability, inspect the latest repository, tests, eval artifacts, run ledger, release gates, stale documentation, and scientific claims. Select the highest-leverage defect or weakest subsystem. A "fix" includes correcting code, data leakage, weak baselines, stale documentation, unsupported claims, incomplete provenance, or a release/reproducibility failure.

Do not protect prior headlines. If a stronger baseline, falsification test, or new evidence weakens a result, preserve the negative result and update the claim everywhere it appears.

## 2. Write a plain-English finding inside the repository

Every run must create or update `docs/FINDINGS.md` with a short section that answers:

- What did we test or fix?
- What did we actually find?
- What changed from the previous belief?
- What can we now claim?
- What can we still not claim?
- Why does it matter?

This explanation should be understandable without reading the source code.

## 3. Update the interview explanation

Every run must update `docs/interview_walkthrough.md`. Keep three layers available:

- **30-second version:** problem, what was built, strongest honest result.
- **2-minute version:** architecture, evaluation, failure/negative result, next step.
- **Likely follow-ups:** baseline choice, leakage, provenance, why the result matters, what failed, and what the user personally built/decided.

If a run changes a headline result, the interview guide must change in the same run.

## 4. External-AI input is evidence to inspect, not authority

Artifacts or analysis produced by another AI may be useful for code, hypotheses, audits, or candidate evidence. Before adoption:

1. diff it against the current repository;
2. run its tests locally;
3. independently inspect the changed logic;
4. verify factual claims against primary sources when they affect empirical conclusions;
5. tag the input in `docs/EXTERNAL_INPUTS.md`;
6. adopt only the parts that survive those checks.

External-AI output never silently becomes a primary source.

## 5. End-of-run minimum checklist

A run is not complete until all applicable items below are done:

- [ ] latest state inspected
- [ ] weakest/broken item selected
- [ ] implementation or correction completed
- [ ] tests/evals rerun
- [ ] failures and rejected approaches recorded
- [ ] `docs/FINDINGS.md` updated in plain English
- [ ] `docs/interview_walkthrough.md` updated
- [ ] external AI provenance logged if used
- [ ] README/PROGRESS corrected if headline state changed
- [ ] exact next executable action recorded
- [ ] release/CI state recorded

## 6. Owner priorities and guardrails (set by Logan, Run 028 — binding on scheduled runs)

These override any "next action" written in an earlier run log.

1. **New facts before new guardrails.** Every run must add at least one new, sourced number about the real world (with evidence ID, vintage and scope) or explain specifically why that was impossible. A run that only adds infrastructure, gates, tests or documentation may not follow another such run.
2. **Primary objective: GOES adequacy.** Tighten `radiant/data/goes_import_floor.py`. In order:
   - annual U.S. GOES trade: run `python scripts/fetch_goes_trade.py` or read `data/goes/goes_trade_annual.csv` if the `goes-data` GitHub workflow already committed it. If neither works, record why and ask the owner to run the `goes-data` workflow. Once present, interpret the trend (did imports rise after 2019? from where?) in FINDINGS;
   - Cleveland-Cliffs electrical-steel shipments and capacity from 10-K filings (vintage-tagged);
   - (done Run 029) Defense stockpile contract recorded as an upper adjustment; upgrade to the DoD/SAM.gov primary notice if reachable;
   - GOES embodied in imported cores/laminations (HTS 8504.90) and finished transformers (8504.23), since steel-form trade understates dependence;
   - DOE distribution-transformer efficiency rule status (shifts demand between GOES and amorphous cores).
   Replace conditions with data; do not add new conditions without new data.
3. **Forecasting is closed.** No further selector or forecasting work unless a policy is frozen *before* evaluation on a genuinely new held-out or strict-vintage series.
4. **Release rule (ADR 006) is settled.** Failed results are withdrawn and published as negative results. Do not reintroduce any gate that makes release depend on winning a claim the evidence has already failed. Do not re-assert a withdrawn result without passing its original fair gate.
5. **Keep it shippable.** `python -m radiant.eval --strict` must exit 0 at the end of every run. If new work would break it, withdraw the failing claim instead.
6. **Stop condition for polishing.** Do not rewrite README or FINDINGS for style. Update them only when a result changes.
7. **Release infrastructure is frozen until a real hosted run exists (added Run 039).** Runs 031–038 spent eight consecutive runs hardening release gates for a CI run that has never happened. Until `artifacts/completed_ci_run.json` from a real GitHub run exists, do not add or harden release gates, receipts, fingerprints or workflows. The only allowed release change is fixing a failure observed in a real hosted run log.
8. **"Network unavailable" is not an exemption from rule 1.** If the Census API is unreachable, find a different sourced fact by web research instead. Candidates: GOES embodied in imported cores/laminations (HTS 8504.90) and transformers (8504.21–8504.23) from published DOE/Commerce/USITC reports; Cleveland-Cliffs statements on GOES-specific volumes; foreign GOES capacity additions (Japan, Korea, Germany, Mexico, Canada) that could supply U.S. imports; Section 232 tariff status for GOES and cores. One sourced fact with evidence ID, vintage and scope.
