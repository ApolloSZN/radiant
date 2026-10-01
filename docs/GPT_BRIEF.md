# Brief for the scheduled GPT run on Radiant (from the owner, Logan)

Use this as the full instruction for each scheduled run. It overrides any "next action" in older run logs.

## Context in three lines
- Radiant's main finding (Run 061, research plan Phase 5): counting sheet, cores and finished transformers, 51–65% of U.S. GOES use in 2019 (282–376 kt) was foreign; it stays at 46% or more through 2035 in every scenario. See `radiant/data/goes_balance.py`. The Run 053 "33% → 41–44%" headline is withdrawn (288 kt double counted cores). Follow `docs/RESEARCH_PLAN.md`; the GPT scheduled task stays paused until the owner resumes it.
- The owner has no computer access for now. The repo is not on GitHub yet; Claude is handling the push separately. **Do not work on GitHub, CI, release gates, receipts, fingerprints, Docker or workflows.** RUN_PROTOCOL §6.7 freezes all of that.
- Runs 031–038 added no new facts. That must not happen again.

## Cadence
One run per day is enough. Facts that don't move the headline are context. Prefer one fact that changes a number over several that don't.

## Every run must do exactly this
1. Read `docs/RUN_PROTOCOL.md` section 6 and `docs/FINDINGS.md`.
2. **Find at least one new, sourced fact about GOES supply or demand by web research.** "The Census API was unreachable" is not an acceptable outcome (§6.8). Work down this list and take the first one you can source from a primary or official document:
   0. **Recent GOES-in-cores tonnage (2020–2025)**: embodied cores are now the largest foreign channel, but the only tonnage estimates are 2019 (68 kt) and 2020 (96 kt). Look for later Commerce, USITC, DOE, Core Coalition or federal-record estimates. Any change here moves the headline.
   1. **Annual U.S. GOES imports in tonnes for any year 2020–2025** from a published table (USITC report or DataWeb export, Commerce/trade.gov steel import monitor, DOE supply-chain report, company filing). State which HTS codes it covers.
   2. **GOES embodied in imports:** how many cores/laminations (HTS 8504.90) or large/distribution transformers (8504.21–8504.23) the U.S. imports, from DOE, Commerce or USITC reports. Steel-form trade understates dependence.
   3. **Foreign GOES capacity that could supply the U.S.:** stated capacity additions by POSCO, Nippon Steel, JFE, thyssenkrupp, Baosteel or others, or any announced North American GOES plant.
   4. **Current tariff status of GOES, laminations and cores** under Section 232, as of 2026, from a Federal Register notice or official proclamation.
   5. **GOES-specific output or shipments** from Cleveland-Cliffs (filings, earnings calls), not combined stainless/electrical totals.
3. Record each fact as an `Evidence(...)` entry (evidence ID, value, unit, period, publication date, evidence class, source URL, scope note), following `radiant/data/goes_import_floor.py`. Add a test. Do not convert qualitative statements into quantities, and do not use market-research-site numbers.
4. Change the import-floor calculation **only** if the new fact replaces a condition with data. Never claim a shortage unless the evidence identifies one.
5. Update `docs/FINDINGS.md` (a short plain-English section), `docs/interview_walkthrough.md` if the headline changed, `PROGRESS.md`, and a new `logs/run_NNN.md`.
6. Finish with `pytest -q` passing and `python -m radiant.eval --strict` exiting 0. If you cannot execute code, say so and still deliver the sourced facts in `logs/run_NNN.md` with the exact code you would add.

## Output
1. The updated repository as a zip named `radiant-v0.14-rcNN-runNNN.zip`.
2. At most 8 plain-English lines for the owner: the new fact, its source, whether it changed the finding, and what's next. No jargon.
