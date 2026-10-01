# Limitations and negative results

## GOES import floor (Run 028)
- Mixed vintages: capacity is a 2020 company statement, baseline use is 2019, and the grid increment is a 2026 planning model. The floor is conditional on non-grid use staying near 2019 levels; the break-even decline (40–49%) is reported.
- Capacity is company-stated, not independently measured. It covers all electrical steel, so it can only overstate GOES capacity. This makes the floor conservative.
- The 2026 hot-mill "25% growth" statement is not converted into GOES capacity.
- Annual 2020–2025 trade quantities are not yet ingested. The Census API could not be queried from this environment because the fetch tool drops query parameters.
- No shortage, price or tariff effect is claimed.
- The Defense stockpile contract volume (up to 53,000 short tons) is a ceiling stated by the producer's CEO and reported by trade press; the DoD announcement (2026-07-01) confirms the award. It is used only as an upper adjustment, not in the identified floor.
- Trade quantities cover GOES in steel form only. GOES embodied in imported cores, laminations and finished transformers is not counted, so steel-form imports understate total dependence.


## Baseline fairness (Run 026) — most important forecasting limitation
The 77.5% sequencing improvement is measured against an all-history log-linear fit, which is known to fail after the next-generation-sequencing regime shift. Against a predeclared panel of simple baselines, the selector robustly beats only all-history, rolling-8 and rolling-6. It is not robustly better than rolling-5 (+9.6%, 95% CI −6.3% to +26.8%) or no-change (+23.7%, CI −7.5% to +49.1%), and it loses to rolling-4 (−8.0%) and rolling-3 (−18.0%). The robustness and sensitivity results below remain correct but only describe the all-history comparison.


- Dense sequencing, battery, and GPU series are retrospective. They are valid for retrospective model comparison but **not** strict historical-vintage forecasts.
- Five contemporaneous NHGRI sequencing anchors are too sparse and mix approximate values with upper bounds. Radiant refuses to manufacture a dense Gate-1 backtest from them.
- The sequencing adaptive rule did not generalize to batteries; forced adaptation was worse than all-history. This negative result motivated causal prequential model selection.
- Public transformer evidence establishes dependencies and macro capacity bounds but does not identify a unique marginal manufacturing bottleneck. Wide admissible parameter ranges destroy the crisp ranking.
- Transformer expansion announcements often report dollars, jobs, facility area, or relative capacity rather than comparable units/year. Radiant does not convert those quantities into LPT output without evidence.
- Synthetic event-study tests validate implementation and falsification behavior, not a real transformer causal effect.
- Illustrative RAF/cross-scale networks demonstrate common software grammar only; they are not empirical evidence for a universal scientific ontology.

## Sampling robustness of headline retrospective results (Run 016)
The sequencing headline improvement is not merely a single aggregate point estimate: a deterministic paired bootstrap over its 39 one-step forecast errors gives a 95% interval of 65.8% to 85.7% relative MALE improvement, and leave-one-out improvement never falls below 76.1%. This strengthens sampling robustness but **does not** change the evidence class; the series was assembled retrospectively.

The battery result is much weaker. With only six paired forecast errors, its paired-bootstrap 95% interval for relative improvement is -8.6% to +23.8%, and leave-one-out sensitivity can become negative (-2.6%). Therefore the reported 11.4% battery improvement should not be treated as established generalization. It remains a small-sample compatibility result / no-regression check, not a robust cross-domain win.

## Run 017 — specification sensitivity
The retrospective selector result is now audited across a predeclared grid of plausible window sets and warm-up lengths. This is deliberately reported as a distribution over specifications rather than selecting the best configuration after seeing outcomes. It does not upgrade retrospective data to historical-vintage evidence. Battery remains too small to support a broad generalization claim even if several nearby selector specifications improve on its baseline.

### Real LPT path parameterization remains partially identified
DOE's 2022 grid supply-chain assessment and July 2024 LPT resilience report identify a real production path (GOES/CTC copper/insulation → core/winding/components → assembly → testing) and report selected facts including roughly one-week LPT testing, facilities with 1–2 test beds in stakeholder evidence, GOES/CTC each at roughly one quarter of production cost, majority foreign GOES sourcing, and current lead times up to/exceeding 36 months. They do **not** provide a mutually compatible public set of physical input coefficients and per-stage annual capacities. Radiant therefore stores this as an evidence-backed topology with explicit unknown numeric parameters. It does not convert cost shares, lead times, import dependence, or test-bed counts into unit-throughput coefficients. The normalized `lpt_scenario()` remains a scenario test of the engine, not a calibrated U.S. factory model.

### Run 021 — partial identification of LPT throughput
Additional primary/public evidence gives useful bounded facts but still does not close the physical coefficient gap. USITC reports illustrative finished LPT weights of roughly 110–410 tons across selected designs; this is **not** a bound on GOES or copper content. Siemens Energy states its Charlotte expansion is planned to reach 57 new LPTs/year at full capacity; this is an announced future site-level output target, not measured current national capacity or a per-stage capacity. Hitachi Energy says its Varennes expansion will "nearly triple" annual production capacity, but without a compatible absolute baseline Radiant does not translate that phrase into a numeric throughput interval. The empirical Charlotte path therefore remains only partially identified: unknown upstream compatible capacities imply a conservative throughput interval of [0, 57] new LPTs/year under the simple serial abstraction. The upper endpoint inherits the announced-target evidence class; it is not an observed output rate.

### NLR 2026 material model is a planning assumption, not a factory BOM
Run 023 incorporates the January 2026 DOE-funded NLR transmission supply-chain model because it supplies explicit, reproducible material assumptions: approximately 600 kg/MVA total transformer weight and assumed mass shares of 48% GOES, 30% copper, 12% non-GOES steel, and 10% other. Radiant types these as `published_model_assumption`. They are useful for scenario demand calculations but are not treated as measurements of Siemens Charlotte's future product mix, bill of materials, procurement, or achieved throughput. Charlotte calculations therefore remain sensitivity scenarios indexed by explicit MVA assumptions.

## Run 027 — fair-baseline gate and online aggregation

The executable release harness now treats the predeclared baseline-fairness panel as a gate. The sequencing selector therefore fails the current scientific ship gate: MALE 0.1762 versus 0.1493 for the strongest fixed panel member (rolling-3), or about 18.0% worse. The old 77.5% improvement versus all-history remains a historical diagnostic only.

Two standard causal online aggregation formulations do not overturn this conclusion. Follow-the-leader reaches MALE 0.1561 and exponential weights reaches 0.1641, but neither robustly beats rolling-3 under the paired-bootstrap diagnostic. These algorithms were added as a falsification benchmark, not as a post-hoc replacement selected for deployment.

Current GOES import-code coverage is also period- and direction-dependent. The 2026 Commerce/SIMA import list uses four relevant ten-digit HTSUSA codes, while the current export concordance uses two Schedule B codes. Historical series must use the concordance valid for each period; the current code list must not be projected backward without checking classification changes.
