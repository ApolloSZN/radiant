# Radiant

**Version:** v0.14-rc42 (release candidate) · **Tests:** 149 passing · **Strict eval:** green. Release infrastructure is frozen under `docs/RUN_PROTOCOL.md` §6.7 until a real hosted run exists; the last local release check was 8/11 in Run 039 and was not rerun in this evidence-focused session.

## In plain English

Radiant is a system for checking claims about how technologies and production systems change. It is built to tell the difference between four things that normally get blurred together:

1. what has actually been **measured**,
2. what the evidence **bounds** without pinning down,
3. what would need a **probability model** that the evidence may not justify, and
4. what is only an **assumption** or scenario.

It also keeps track of **when** each piece of evidence became available. That lets it replay the past without cheating: a forecast "made in 2010" can only use what was knowable in 2010.

When the evidence can't support an answer, Radiant says so instead of producing a confident-looking number. For example, the announced capacity of a new transformer factory is recorded as "somewhere between 0 and 57 units a year" until the upstream stages are evidenced.

## What it has found so far

- **Transformer imports (identified result).** In 2019 the U.S. produced about 137 large power transformers, imported about 617, exported about 4, and reported roughly 40% factory utilization. That implies about 342 units/year of domestic capacity. Even at 100% utilization, the U.S. would still have needed about 410 imports a year. Using idle factories could not have ended import dependence. Radiant does not claim to know *why* utilization was low.
- **Grid expansion pushes U.S. reliance on foreign transformer steel from about a third to at least 41–44% (identified conditional bound, Runs 028/040/053).** Cleveland-Cliffs, the only U.S. maker of grain-oriented electrical steel (GOES), states capacity of up to ~227 kt a year for *all* electrical steel, an upper limit on GOES. In 2019 the U.S. used ~220 kt of GOES as sheet (27 kt imported) plus an estimated 68 kt that arrived already built into imported cores (Commerce). That is ~288 kt in all forms, ~95 kt (33%) of it foreign. A 2026 DOE-funded national-lab model adds 94–114 kt/yr for transmission expansion. Even if the domestic producer made nothing but GOES at full capacity, foreign GOES in all forms must reach at least **155–175 kt/yr, 1.6–1.8× the 2019 level and 41–44% of U.S. use**. Equivalently, if core imports stay flat, sheet imports must be at least 87–107 kt/yr. The earlier "3–4× 2019 imports" headline divided by sheet imports only and is withdrawn as a headline (Run 053). The floor only vanishes if non-grid use falls 40–49% below 2019. The 2026 hot-mill "25% growth" statement is not converted into GOES capacity. The Defense stockpile contract (up to 53,000 short tons, multi-year) is a ceiling sensitivity only. No shortage is claimed: whether foreign supply can meet the floor is not identified.
- **Forecasting: claim withdrawn.** Against a straight line fitted to all history, the original selector cuts error by 77.5%, but a rolling-3 trend beats it (MALE 0.1493 vs 0.1762). Follow-the-leader (0.1561) and exponential weights (0.1641) also fail to beat rolling-3 robustly. Radiant therefore asserts no forecasting result; the comparison is published as a negative result. See `docs/FINDINGS.md`.
- **Negative results kept on purpose.** The battery-price improvement (11.4%, six forecasts) is not robust. On archived BLS productivity releases, the revision-correction model is 31.6% worse than doing nothing. That experiment exists to prove the historical-replay machinery doesn't leak future information, and it does that job.

## What it is not

- Not a proven forecasting advantage.
- Not a breakthrough-discovery engine.
- Not an established model of civilization or a universal theory of adaptive systems. The cross-scale examples (protocell, lab, industrial region) are illustrative and tagged as such.

## Technical overview

| Layer | Module | What it does |
| --- | --- | --- |
| Kernel | `radiant/kernel.py` | Bounded adaptive system (state, resources, observation, memory, control, action, viability, update). Persistence, regulation, self-production and autonomy are statistical tests, not labels. |
| Topological closure | `engines/raf.py` | RAF / maxRAF closure (Hordijk–Steel), exact knockouts, recursive causal DAGs of collapse. |
| Material viability | `engines/viability.py` | LP stock-flow viability: steady state, finite horizon, non-depleting self-maintenance, and period-resolved paths that cannot borrow future supply backward. |
| Dynamics | `engines/dynamics.py` | Wright/Moore curves, composition drift, Amdahl ceilings, reflexivity, thresholds, regime detection. |
| Counterfactuals | `engines/counterfactual.py` | Reproducible interventions with common random numbers and deterministic result hashes. |
| Constraint resolution | `engines/constraint_resolution.py`, `uncertain_constraints.py`, `partial_identification.py` | Production LPs, knockouts, relaxations, bottleneck migration, epistemic ensembles, distribution-free bounds that return "not identified" when evidence is insufficient. |
| Evidence & forecasts | `data/backtest.py`, `vintage_eval.py`, `forecast_ledger.py` | Bitemporal replay, prequential model selection, immutable hashed forecast ledger, Brier/log scoring. |
| Audits | `data/robustness.py`, `eval_sensitivity.py`, `baseline_fairness.py`, `online_aggregation.py` | Paired bootstrap, leave-one-out, predeclared specification grid, fair-baseline panel, causal online aggregation benchmarks. |
| Transformer / GOES case | `data/transformer_*.py`, `lpt_evidence_network.py`, `goes_supply_panel.py`, `goes_import_floor.py` | Evidence-typed U.S. large-power-transformer production network and GOES supply work. |

Design decisions are recorded in `docs/adr/`. Negative and unidentified results are in `docs/limitations.md`. A longer write-up is in `docs/technical_writeup.md`. The standing work-session requirements are in `docs/RUN_PROTOCOL.md`, and externally supplied AI work is tracked in `docs/EXTERNAL_INPUTS.md`.

## Run

```bash
pip install -r requirements.txt
./scripts/reproduce.sh          # tests + eval harness + demo
python -m radiant.eval          # report-only: writes artifacts/eval_report.json
python -m radiant.eval --strict # CI mode: non-zero while the scientific gate is red
python -m radiant.release --run # fail-closed release verifier
# clean-container release reproduction (the v1.0 gate): bash scripts/reproduce_container.sh
```

## Release status

Release rule (ADR 006): a result may be asserted only if its gate passes. A result that fails is withdrawn and published as a negative result. It does not block release, and it cannot be re-asserted without passing the same fair gate. Under that rule the eval gate is green (`python -m radiant.eval --strict` exits 0), and the raw sequencing fair-baseline test still reports `passed: false`.

Remaining gates: the exact candidate commit must execute on hosted GitHub Actions, and that run must be observed as completed and successful. To clear them, push the repository to GitHub, let `.github/workflows/ci.yml` run, and save the completed run record as `artifacts/completed_ci_run.json` (see ADR 004).

## Next scientific step

Annual trade data: `scripts/fetch_goes_trade.py` pulls 2019+ GOES imports and exports from the Census API, and `.github/workflows/goes-data.yml` runs it on GitHub monthly or on demand. When `data/goes/goes_trade_annual.csv` exists, the import floor is automatically compared with the latest full-year imports. The 2025 Cleveland-Cliffs aggregate stainless/electrical shipment figure and DOE transformer-rule status are now recorded, but neither is GOES-specific tonnage. Remaining: annual GOES trade, GOES-specific domestic output, and GOES embodied in imported cores and transformers. Forecasting is closed unless a frozen policy is tested on a new held-out series.

## References

- Hordijk, Smith, Steel (2015). Algorithms for detecting and analysing autocatalytic sets. *Algorithms for Molecular Biology* 10:15.
- Nagy, Farmer, Bui, Trancik (2013). Statistical basis for predicting technological progress. *PLOS ONE*.
- U.S. DOE (2022, 2024). Grid supply-chain and large power transformer resilience reports.
- U.S. Department of Commerce (2020). Section 232 investigation, grain-oriented electrical steel.
- NHGRI DNA Sequencing Costs data; NREL/BNEF battery pack prices; BLS Productivity and Costs archived releases.
