# Radiant progress

## Current status (Radiant v1.0 shipped; maintenance checkpoint Run 063)

| Subsystem | State |
|---|---|
| Kernel, RAF closure, viability, counterfactuals | tested |
| Constraint resolution / partial identification | tested; returns "not identified" when evidence is insufficient |
| Forecasting | **claim withdrawn** (loses to rolling-3; online learners also fail); published as negative result |
| Historical-vintage replay | strict BLS replay passes integrity; predictive model loses (kept) |
| Transformer case | identified macro import-dependence bound (2019) |
| GOES supply | **rebuilt (Run 061): 51–65% of 2019 U.S. GOES use was foreign in all forms (sheet + cores + finished transformers, 282–376 kt); ≥46% through 2035 in every scenario**; Run 053 "33% → 41–44%" withdrawn (288 kt double counted cores); no shortage claimed |
| Release rule | **v1.0 shipped** at exact release SHA `2044ca5f8a235889a27733f58b3c0cdf5c11a7c8`; hosted release evidence verified |
| Tests | **release gate green on exact shipped SHA**; historical Run 054 count below is retained as append-only evidence |
| Strict eval | **exit 0** |
| Hosted CI | **verified green** on exact shipped SHA; final release verifier's full-v1.0 ship-bar step passed |

**Weakest scientific link:** recent embodied-GOES mass is still missing. Run 054 adds 2024 and early-2025 USITC DataWeb counts for imported laminations, but those observations are in units rather than tonnes; the latest mass estimates remain 68 kt for 2019 and 96 kt for 2020 (estimate). Direct annual U.S. GOES steel tonnes for 2020–2025 are also still missing.

**Weakest shipping link:** none for Radiant v1.0. The remaining program gate is Phase-2 project selection; implementation must not begin until Logan explicitly approves a presented charter.

**Exact next executable action:** keep Radiant frozen and green. Do not reopen withdrawn forecasting claims or add speculative GOES conversions. Present/maintain the top-three Phase-2 charters and wait for Logan's explicit project approval before starting the single WIP.

# Run history (append-only; early entries describe earlier states)

## Run 004 evidence
- Historical-vintage ingestion: five contemporaneous NHGRI T0 anchors encoded with publication availability dates. Partial; insufficient for full strict replay.
- Regime/surprise engine: causal sequential detector implemented; adaptive forecast MALE 0.2084 vs rolling-8 0.2744 on retrospective sequencing series. Prototype evidence only.
- Tests: 29/29 passing.
- Gate 1: NOT PASSED; full historical information sets remain binding constraint.

## Run 005 / v0.6 evidence
- Second real domain added: lithium-ion pack prices, 2010–2020 (11 NREL/BNEF retrospective observations).
- Cross-domain falsification: sequencing-style adaptive forecaster fails to generalize; battery MALE 0.1765 vs 0.1344 for all-history. Negative result retained.
- Causal prequential model selector added; sequencing MALE 0.1762 and battery MALE 0.1461, without current-target leakage.
- 32/32 tests pass.
- Historical backtest gate remains NOT PASSED because dense real series are retrospective rather than complete contemporaneous vintages.

## Run 006 / v0.7 evidence
- Third measured domain added: leading AI GPU price-performance (P100/V100/A100/H100) from Epoch AI. Four real observations, explicitly retrospective; cannot pass historical-vintage replay.
- Immutable forecast registration/resolution ledger implemented with deterministic artifact hashes, evidence binding, Brier/log scores for binary forecasts and log/factor error for positive continuous forecasts.
- Recursive process-level knockout trace implemented; toy ore cut now yields a 22-edge causal DAG over 18 nodes for the 10-process collapse rather than only terminal root labels.
- 37/37 tests pass, including leakage/vintage rejection and forecast immutability tests.
- Historical backtest Gate 1 remains NOT PASSED. Binding constraint remains complete contemporaneous information vintages; secondarily, real production-network evidence.


## Run 007 / v0.8 evidence
- First real production-system case started: U.S. large power transformers. DOE primary evidence encoded for GOES, CTC copper/insulation dependencies, specialty factory-equipment lead times, import dependence, custom manufacture and long procurement lead times.
- New `constraint_resolution` LP maximizes declared system output and performs one-at-a-time marginal intervention scans with explicit evidence bindings.
- Critical epistemic guardrail: DOE qualitative dependencies are NOT silently converted to quantitative U.S. capacities. The first transformer network therefore separates evidence-backed topology from normalized scenario parameters. Its numerical intervention ranking is a software validation result, not a claim about the real U.S. bottleneck.
- In the normalized validation scenario, throughput=0.72; +20% test/qualification capacity raises it to 0.78 (+8.33%), after which assembly becomes binding. Increasing GOES availability alone has zero effect in that scenario. This demonstrates bottleneck migration and why single-factor narratives can fail, but is not empirical U.S. inference.
- 41/41 tests pass.
- Binding constraint: obtain measured transformer process capacities/material intensities/qualification throughput or procurement microdata sufficient to replace normalized scenario coefficients.

## Run 008 / v0.9 evidence
- Added uncertainty-aware constraint ensembles: capacity/import parameters can be represented as epistemic intervals and sampled reproducibly; intervention rankings are reported as probabilities rather than fake point certainty.
- Added measurement-priority diagnostics: rank correlation between uncertain parameters and system throughput identifies which missing measurement most controls the conclusion.
- Added DOE primary evidence anchors: ~750 U.S. new >60 MVA transformers in 2019, >80% imported, ~900 annual demand projected for 2027, and commonly quoted 36-month / up-to-60-month LPT acquisition lead times. Added 2026 DOE evidence for limited LPT interchangeability (~1.3 made per design). These are evidence records, not invented process capacities.
- Adversarial wide-uncertainty transformer scenario (all stage capacities 0.45-1.35 normalized; input limits 0.55-1.55; 300 deterministic draws) produces NO robust bottleneck: top-intervention probabilities are dispersed (assembly 19.0%, winding 18.3%, insulation prep 16.7%, core fabrication 15.3%, testing 12.0%, each input <=7%). This is a useful negative result: current public evidence does not identify a defensible single binding production constraint.
- Throughput in that epistemic stress test spans q05=0.461, median=0.569, q95=0.770 normalized units. These values are scenario diagnostics, not U.S. output estimates.
- 44/44 tests pass.
- Binding constraint is now parameter identification, specifically stage-level capacity/utilization/cycle-time and input availability measurements. Radiant can now state exactly when it does not know enough to rank interventions.

## Run 009 / v0.10 evidence
- Added partial-identification engine. When only parameter bounds are justified, Radiant enumerates admissible corner scenarios and certifies an intervention only if it remains best throughout the identified set; otherwise it returns no unique bottleneck. This avoids inventing probability distributions over epistemic uncertainty.
- Added 2019 U.S. LPT macro accounting from the Commerce Section 232 evidence: 137 domestic >100,000 kVA units, 617 imports, 4 exports -> 750 apparent consumption and 82.27% import share. Combining the reported ~40% utilization with output implies ~342.5 units/year nameplate capacity and ~205.5 units/year unused nameplate capacity as an accounting bound, not a feasible-output claim.
- Consequential inference: even the extreme counterfactual of full utilization of reported 2019 domestic nameplate capacity would leave ~411.5 imported units required to hold 2019 apparent consumption constant. Therefore utilization of the 2019 domestic plant base alone could not eliminate import dependence. This does NOT identify why utilization was low or which stage should be expanded.
- Added Commerce evidence for 2019 GOES/lamination/core imports and preserved a definition conflict: Commerce's broader accounting estimated ~44% GOES import penetration, while DOE reports much higher dependence for specific downstream GOES forms. Radiant now records both instead of collapsing them into one number.
- Added Wood Mackenzie 2024/2025 market evidence as T1: ~150-week ARO lead times and estimated 30% 2025 U.S. power-transformer supply deficit / ~80% import share. These constrain the macro state but remain insufficient for plant-stage causal identification.
- Tests: 47/47 passing.
- Binding constraint: acquire plant/order-level variation capable of explaining the utilization-to-throughput gap (labor, design mix/changeovers, winding/core/test utilization, material shortages, qualification/rework). Until then, no unique stage-level U.S. bottleneck is identified.

## Run 010 / v0.11 evidence
- Added an evidence-bounded capacity-expansion analyzer. It distinguishes disclosed unit/year additions from investments/jobs with no disclosed unit capacity and requires explicit product-definition compatibility before promoting arithmetic to an empirical bound.
- Added Siemens Charlotte as the first disclosed U.S. LPT unit-rate expansion: 24 new LPT/year initially and 57/year at full rate (APPA report of Siemens announcement). Hitachi South Boston is recorded as a major expansion but contributes **zero numeric units/year** until a source reports a unit rate; investment dollars/jobs are not converted into output.
- Combining the 2019 Commerce/DOE implied legacy nameplate (342.5 units/year) with Siemens full-rate +57 gives 399.5 units/year. Against a fixed 750-unit demand benchmark, even the optimistic 100%-utilization accounting bound leaves 350.5 units/year requiring external supply and caps domestic nameplate at 53.27% of that benchmark. This is a capacity-sufficiency bound, not a forecast.
- DOE's 2027 ~900-unit demand figure uses a >60 MVA category that is not identical to the Commerce >100,000 kVA accounting base. Radiant therefore computes the 500.5-unit residual only as a cross-definition scenario and explicitly refuses to call it an identified empirical gap.
- Added evidence records for shared build slots, 1-3 year factory construction, 1-2 year specialty-equipment procurement, workforce prevalence (89% hiring difficulty; 66% ongoing), and test-space directionality. These strengthen candidate causal mechanisms without assigning unsupported effect sizes.
- Added migration 006 to persist constraint hypotheses, typed evidence bindings, and capacity additions. `supports_presence`/`supports_direction` are structurally distinct from `quantifies_effect`.
- Tests: 50/50 passing.
- Adversarial direction check: improved empirical grounding, falsifiability, and claim discipline. A tempting stronger claim—"labor is the binding bottleneck"—was rejected: the workforce survey establishes prevalence, not marginal throughput or counterfactual relief.
- Current weakest link: effect identification. Public evidence now supports several simultaneous constraint hypotheses (workforce, test space, build slots/equipment, GOES) but still lacks plant/order-level variation sufficient to estimate which intervention yields the largest marginal throughput gain.
- Exact next executable action: acquire or construct dated plant/order panels (manufacturer/site, product class/design, quoted/actual delivery, expansion commissioning, workforce and test-space changes where observable) and implement event-study / difference-in-differences style falsification checks before using them to update intervention rankings.

## Run 011 / v0.12 evidence
- Ship eval harness added and CI-gated. Sequencing prequential selector: MALE 0.1762 vs all-history 0.7836, 77.5% lower. Battery selector: MALE 0.1461 vs rolling-5 0.1648, 11.4% lower. Both are explicitly `retrospective_real_data`, not historical-vintage evidence.
- Clean-machine reproduction infrastructure added: `requirements.txt`, Dockerfile, `scripts/reproduce.sh`, GitHub Actions workflow. Local reproduction passes.
- Initial ADRs added for evidence classes, RAF/material-viability separation, and prequential model selection.
- Causal effect-identification harness added for future transformer panels. It requires parallel-enough pretrends and a passing placebo; adversarial tests show either failure blocks `identified=True`.
- New primary evidence milestones logged: Prolec Goldsboro +200 medium-power transformers/year projected by 2030; Hitachi South Boston groundbreaking 2026-06-29 with no public units/year; Hitachi Mississippi 2026-09-15 states relative capacity doubling but no absolute units/year. Cross-product conversions remain prohibited.
- Tests: 54/54 passing locally; eval harness passes. Hosted CI execution is not verified because this artifact is not yet attached to a live GitHub repository in this run.
- v1.0 ship bar remains NOT PASSED. Major blockers: strict historical-vintage headline evidence; public-ready 1,500-2,500 word write-up; 10-minute README cleanup; verified container/hosted-CI run; stronger demo; causal transformer outcome panel remains unavailable.
- Weakest scientific link: historical-vintage/effect-identification evidence. Weakest shipping link: end-to-end packaging/documentation verification.
- Exact next action: construct a strict vintage evaluation fixture from independently dated primary releases (or explicitly fail Gate 1 if density is insufficient), then build the v1.0 ship-bar verifier that refuses release while any required artifact/evidence class is absent.

## Run 012 / v0.13 evidence
- Added fail-closed `radiant.release` v1.0 verifier. It checks executable evidence for every ship-bar item and refuses release unless a passing `strict_historical_vintage` headline eval exists.
- Added two release-verifier falsification tests: retrospective evidence alone cannot pass; strict-vintage evidence can pass when all other artifacts are present.
- Added `docs/limitations.md` preserving retrospective-vintage, battery generalization, transformer identification, announcement-conversion, synthetic-event-study, and illustrative-ontology limitations.
- Fresh primary-source search for additional dated NHGRI 2007-2009/2013 anchors returned no usable results in this run. Existing five anchors remain too sparse and heterogeneous (approximate values + upper bounds) for a defensible dense strict-vintage forecast evaluation. Gate remains failed rather than backfilled from retrospective data.
- 56/56 tests pass locally. `radiant.release --run` reports 7/9 ship gates passing. Remaining failures: 1,500-2,500-word technical write-up and strict no-leak historical-vintage headline evidence.
- Weakest scientific link: strict historical-vintage evidence. Weakest shipping link: technical write-up, now mechanically testable.
- Exact next action: seek an authoritative archived/vintage source with enough contemporaneously published observations to support a genuine rolling evaluation; in parallel complete the technical write-up without weakening the evidence gate.

## Run 013 / v0.14 candidate evidence
- Added a strict historical-vintage fixture from archived BLS Productivity and Costs releases. Preliminary estimates and their later revisions retain independent publication dates and primary-source URLs.
- Added prequential revision replay: each prediction is made at the preliminary-release cutoff using only revisions already published by that cutoff; forecast payloads receive deterministic SHA-256 hashes before resolution.
- Strict-vintage result is deliberately negative: on 7 evaluable releases, median-prior-revision correction MAE is 0.3571 percentage points vs 0.2714 for the no-correction preliminary baseline (31.6% worse). This is retained as falsification evidence; the strict-vintage gate passes information-time integrity, not predictive superiority.
- Retrospective headline evals remain unchanged: sequencing selector MALE 0.1762 vs 0.7836 (-77.5%); battery 0.1461 vs 0.1648 (-11.4%). They remain labeled retrospective.
- Added 1,779-word public-ready technical write-up. Local fail-closed release verifier now reports 9/9 gates passing and one-command `scripts/reproduce.sh` completes successfully.
- Tests: 58/58 passing locally.
- IMPORTANT release caveat: hosted GitHub Actions has not been observed on a live remote repository in this environment. Therefore this artifact is a **v1.0 release candidate**, not yet declared shipped despite the local verifier's 9/9 result. The CI gate must be externally observed green before Phase 2 starts.
- Weakest shipping link: hosted-CI verification. Weakest scientific link: real causal effect identification in the transformer production case; strict-vintage integrity is now exercised but on a small independent BLS domain rather than the sequencing headline domain.
- Exact next action: attach/push the release candidate to the live repository and observe GitHub Actions green; if no remote is available, keep Phase 1 gated and improve the release verifier so `tests_ci_green` distinguishes local reproduction from hosted-CI evidence.

## Run 014 — v0.14-rc2
- Replaced the release verifier's previous proxy for CI with a fail-closed hosted-CI gate.
- Added `radiant.ci_attest`: attestations can only be generated from a GitHub Actions environment and are bound to a 40-hex commit SHA and Actions run ID/URL.
- CI now runs tests, eval, generates hosted attestation, runs the release verifier, and uploads all four evidence artifacts.
- Added falsification tests: local attestation generation is rejected; valid CI environment is commit-bound.
- Full local suite: 60/60 passing. Eval harness green. Release verifier: 9/10 gates; only `hosted_ci_green` is false locally by design.
- GitHub connector inspection found no accessible Radiant repository, so this run could not truthfully produce/observe a hosted Actions run. Existing accessible repos are unrelated and were not modified.
- Binding blocker: create/select the Radiant GitHub repository and push this exact candidate; hosted CI must produce the attestation before v1.0 can ship.

## Run 015 — v0.14-rc3
- Corrected hosted-CI semantics: an attestation generated inside a running workflow proves hosted execution, not eventual green completion.
- Added two-phase release evidence. `--ci` mode can pass inside Actions without claiming final completion; final mode additionally requires `artifacts/completed_ci_run.json` showing GitHub `status=completed`, `conclusion=success`, and the matching commit SHA.
- Added adversarial tests for in-progress, failed, and wrong-commit completed-run evidence. An initial formulation that made CI impossible to complete was rejected and fixed.
- Added ADR 004 and a two-minute interview walkthrough.
- Tests: 63/63 local. Final verifier: 9/11 locally by design; missing hosted execution and completed-success evidence.
- Binding blocker remains external: no accessible Radiant GitHub repository exists in the connected account, so Phase 1 cannot truthfully cross the final ship gate.

## Run 016 — v0.14-rc4
- Added deterministic paired-bootstrap and leave-one-out robustness diagnostics for baseline-vs-system forecast errors.
- Sequencing retrospective result (n=39 paired forecasts): point improvement 77.5%; paired-bootstrap 95% interval 65.8%–85.7%; P(improvement >=50%)=0.9999 under the resampling diagnostic; leave-one-out minimum improvement 76.1%. This strengthens robustness of the retrospective result but does not upgrade its evidence class.
- Battery result (n=6): point improvement 11.4%; paired-bootstrap 95% interval -8.6%–23.8%; leave-one-out minimum -2.6%. This exposes the battery result as fragile and prevents it from being advertised as robust cross-domain generalization.
- Added two robustness tests; full suite 65/65 passing locally.
- Hosted-CI blocker remains external: no accessible Radiant repository exists, and this connector exposes repository-content writes but no repository-creation action. Phase 2 remains gated.
- Exact next action: publish rc4 to a Radiant GitHub repository, observe hosted execution and completed-success evidence for the exact commit, then run final release verifier. If the external repository remains unavailable, continue scientific hardening without weakening the release gate.

## Run 017 — v0.14-rc5
- Added a predeclared specification-sensitivity audit for the causal prequential selector. It reports the full grid rather than cherry-picking the best hyperparameters after outcomes are visible.
- Added two tests for deterministic/comprehensive grid reporting and retention of losing specifications. Full suite: 67/67 passing locally.
- The audit is explicitly robustness evidence only; it cannot upgrade retrospective observations to historical-vintage evidence.
- Hosted-CI release blocker remains unchanged: no accessible Radiant repository exists in the connected GitHub installation, so final release evidence cannot be truthfully manufactured.

## Run 018 — v0.14-rc6
- Found and fixed a physical-validity bug in the quantitative viability LP: previous versions emitted balance constraints only for maintained items, so an unmaintained raw input consumed by a process could be treated as implicitly free even when no external supply existed. The LP now balances every item appearing in inputs, outputs, maintenance, or explicit external supply.
- Added regression tests proving an unproduced raw input makes a network infeasible and that a finite raw-input cap binds at the correct stoichiometric requirement.
- Added `finite_horizon_viability`: explicit initial stocks, per-time maintenance/depreciation, process-rate capacities, external inflow-rate limits, horizon-integrated energy, and a non-depletion criterion. This distinguishes temporary survival by drawing down inherited stock from actual maintenance closure.
- Added falsification case: 10 units of inherited tool stock with 1 unit/time depreciation survives a 5-unit horizon but fails self-maintenance when terminal stock must be restored. Adding a feasible replacement process passes.
- Full suite: 71/71 passing; one-command reproduction passes; eval results unchanged. Final release verifier remains 9/11 by design, missing only hosted execution and completed-success evidence.
- Scientific consequence: topological RAF, steady-flow material closure, finite-horizon survival, and finite-horizon non-depleting self-maintenance are now four distinct computable claims. This materially strengthens physical/resource validity.
- Binding shipping blocker remains external hosted CI. Binding scientific weakness remains real causal effect identification / broader empirical cross-scale validation.
- Exact next action: publish rc6 to the intended Radiant repository and obtain commit-bound hosted execution + completed-success evidence. If externally blocked, next hardening slice should add time-varying finite-horizon stocks/capacities or empirically parameterize one production network rather than adding presentation layers.

## Run 019 — v0.14-rc7
- Added period-resolved `path_viability` with explicit stock trajectories, time-varying process/import capacities, intermediate non-negativity, energy accounting, and terminal reserve/non-depletion constraints.
- Added a temporal falsification case showing that future supply cannot be borrowed backward to satisfy an earlier maintenance obligation; aggregate horizon balance is therefore not sufficient for path feasibility.
- Added temporary-capacity-outage and terminal-replacement tests. One initial test fixture was rejected because inherited stock legitimately bridged the first period; the corrected zero-stock fixture tests the intended temporal impossibility.
- Full suite: 74/74 passing; one-command reproduction passes; forecast metrics unchanged. Final release verifier remains 9/11 by design, missing only hosted execution and completed-success evidence.
- Scientific consequence: Radiant now separates steady-flow closure, aggregate finite-horizon survival/non-depletion, and period-resolved path viability. The binding scientific weakness shifts further toward empirical parameterization rather than solver structure.
- Exact next action: parameterize one real production-network slice with dated public capacity/input evidence and apply path-dependent shortage/knockout analysis with uncertainty. Hosted CI remains the external shipping blocker.

## v0.14-rc8 / Run 020
- Added evidence-backed real LPT production graph from DOE 2022/2024.
- Separated measured facts from seven unknown numeric production parameters.
- Refused to convert cost shares, lead times, import dependence, or test-bed counts into throughput coefficients.
- Added safe structural-knockout semantics; effect sizes remain unidentified.
- 76/76 tests green; final release still 9/11 pending exact-candidate hosted CI execution/completion.

## Run 021 — v0.14-rc9
- Added generic epistemic `Bound` / serial-throughput propagation to the existing partial-identification engine. Unknown stages remain `[0, inf]`; no midpoint or probability distribution is invented.
- Added primary/public LPT evidence at native scope: USITC illustrative finished-transformer weights (110–410 tons across selected designs), Siemens Energy Charlotte announced future full-capacity target (57 new LPTs/year), and Hitachi Energy Varennes qualitative "nearly triple" expansion statement.
- Explicitly rejected two tempting conversions: finished transformer weight -> GOES/copper mass, and "nearly triple" -> a numeric capacity multiplier without an absolute compatible baseline.
- Charlotte example is conservatively `[0,57]` units/year under a serial abstraction because compatible upstream stage capacities remain unknown. This is partial identification, not calibration.
- First implementation accidentally overwrote the pre-existing `partial_identification()` intervention engine, causing two regression failures. Restored and extended the module; final suite 80/80 green and one-command reproduction passes.
- Final release remains 9/11 pending exact-candidate hosted execution and completed-green evidence.
- Exact next action: seek same-site upstream capacity/material bounds or procurement/BOM evidence capable of shrinking `[0,57]`; otherwise use the interval engine to rank which missing measurement would reduce decision uncertainty most.


## Run 022 — v0.14-rc10
- Added DOE 2012 physical core-steel coefficient (80–120 metric tonnes/unit for 300–500 MVA) as scoped interval evidence.
- Added conditional coefficient propagation: 57 units/year would imply 4,560–6,840 tonnes/year core steel only if all units are in that reference class; not asserted as Charlotte actual use.
- Added distribution-free information-requirement analysis. Charlotte has five zero-lower-bound serial stages; isolated finished-output evidence cannot certify positive path throughput.
- 84/84 tests green; one-command reproduction green; release remains 9/11 pending hosted CI.

## Run 023 — v0.14-rc11
- Added January 2026 DOE-funded NLR transmission supply-chain evidence as a typed `published_model_assumption`, not a measured Charlotte BOM.
- NLR reference model: ~600 kg/MVA for LPTs above 100 MVA; assumed mass shares 48% GOES, 30% copper, 12% non-GOES steel, 10% other.
- Added reproducible material-demand calculations and explicit Charlotte MVA sensitivity scenarios. No product-mix midpoint is selected.
- Added NLR national planning scenario evidence: ~1,370–1,510 transformer units/year across modeled scenarios; total transmission expansion implies 94–114 thousand tons GOES/year and 61–74 thousand tons copper/year. NLR states modeled GOES demand exceeds 45% of 2019–2023 apparent consumption.
- 88/88 tests green; one-command reproduction green. Final release remains 9/11 pending exact-candidate hosted execution and completed-green evidence.

## Run 024 — v0.14-rc12
- Added a distribution-free GOES supply-pressure result tied directly to NLR 2026: modeled transmission expansion adds 94–114 kt/y GOES, stated by NLR to exceed 45% of average U.S. apparent consumption in 2019–2023.
- The engine preserves only the identified inequality: incremental demand / historical baseline > 0.45, so absent displacement, inventory drawdown, recycling changes, or supply expansion, total requirements exceed 1.45× the historical baseline. It does not reverse-engineer a point estimate of apparent consumption from the inequality.
- Crucially, this is **not** encoded as a shortage finding. Commerce's Section 232 report provides useful historical context (about 220 kt/y U.S. GOES consumption and ~27 kt imports in 2019), but that is not vintage-compatible evidence of future supply response. The shortage flag therefore remains false.
- Added 2 regression tests enforcing the non-shortage interpretation and no hidden reconstruction of apparent consumption. Full suite 90/90 green; one-command reproduction green.
- Final release remains 9/11 pending exact-candidate hosted execution and completed-green evidence.
- Exact next action: construct a vintage-aligned GOES supply-response panel (domestic production/capacity, imports, exports, inventories where available) before testing whether the NLR planning increment produces an identified adequacy gap. Do not infer shortage from demand pressure alone.

## Run 025 — v0.14-rc13
- Began the vintage-safe GOES supply-response panel by formalizing commodity coverage and observation vintages rather than filling missing years with inferred values.
- Census classification evidence shows GOES flat products span two width classes: 7225.11 (>=600 mm) and 7226.11 (<600 mm). Added a fail-closed coverage validator so a one-code query cannot silently masquerade as total GOES trade.
- Added typed 2019 Commerce historical anchors (~220 kt apparent consumption, ~27 kt imports) with period, publication year, evidence class, unit, and scope. Their descriptive import share is ~12.27%; it is explicitly not a 2026+ supply-capacity estimate.
- Added machine-readable adequacy contract listing missing same-horizon domestic production/capacity, exports, inventory/stock change, and competing-consumption evidence. Adequacy remains unidentified.
- USGS 2026 commodity data were reviewed but are aggregate iron/steel/mineral statistics and do not resolve GOES-specific production response; they were not substituted for GOES data.
- 93/93 tests green; one-command reproduction green. Final release remains 9/11 pending hosted CI execution and completed-green evidence.
- Exact next action: ingest authoritative annual Census/Commerce quantities for both GOES codes, then seek compatible domestic GOES production/capacity and exports before computing a vintage-aligned supply envelope.

## Run 026 — v0.14-rc14 (consolidation + baseline-fairness audit)
- Consolidated README and PROGRESS: removed stale v0.2 / 26-test / old-gate text from the front of both files; the README now opens with a plain-language description and current results.
- Added `radiant/data/baseline_fairness.py`: evaluates the sequencing selector against a predeclared panel of simple baselines (all-history; rolling 8/6/5/4/3; no-change) with paired bootstrap.
- Result: the 77.5% headline is robust only against all-history (and rolling-8/6). Against rolling-5: +9.6%, 95% CI −6.3% to +26.8% (not robust). Against no-change: +23.7%, CI −7.5% to +49.1% (not robust). Rolling-4 (−8.0%) and rolling-3 (−18.0%) beat the selector. Headline downgraded: the defensible finding is that recent data beats old data after a regime shift; the selector itself adds little.
- Wired the audit into `radiant.eval` output and limitations; added 3 tests preserving the negative result. Updated technical write-up, limitations, interview walkthrough; added `docs/FINDINGS.md` (plain-language one-pager).
- Tests: 96/96 passing. Release verifier 9/11 (unchanged; hosted CI still external).
- Next action: push to GitHub and observe hosted CI; then the GOES supply panel.



## Run 027 — v0.14-rc15
- Fixed a release-integrity contradiction: Run 026 showed the sequencing headline failed stronger baselines, but the executable eval gate still passed against all-history. The sequencing CI gate now requires robust success against the complete predeclared simple-baseline panel. It fails, as it should.
- Added causal online aggregation benchmarks. Follow-the-leader MALE = 0.1561 and exponential weights MALE = 0.1641 versus rolling-3 = 0.1493. Both improve on the old selector (0.1762) but neither robustly beats the strongest fixed baseline. Negative result preserved.
- Added ADR 005: fair baselines are release gates, not footnotes. GitHub Actions now invokes `python -m radiant.eval --strict`; report-only eval remains available for reproducibility before the gate passes.
- Corrected GOES acquisition semantics. Coarse HS-6 identity is two headings, but current Commerce/SIMA U.S. import extraction requires four ten-digit HTSUSA codes (`7225110000`, `7226111000`, `7226119030`, `7226119060`), while current exports use a different two-code Schedule B concordance. Coverage is now direction/effective-period specific and incomplete periods fail closed rather than treating missing codes as zero.
- Primary sources consulted for code coverage: U.S. Commerce SIMA steel product HTS list, Commerce export-monitor concordance, and Census international-trade API documentation. No annual trade quantities were fabricated or inferred from those classifications.
- Initial test run after changes failed 1/102 because an existing assertion required the phrase `all-history baseline` in the limitations text. The behavior was correct; the wording regression was fixed and the final suite passes 102/102.
- One-command `scripts/reproduce.sh` completes successfully in report-only mode. Strict evaluation exits non-zero by design. Final release verifier = 8/11: `eval_harness_ci`, `hosted_ci_execution`, and `hosted_ci_completed_green` are false.
- Exact next action: do not optimize further on sequencing outcomes. Freeze a policy and test on new historical-vintage/held-out technology data; in parallel, acquire annual GOES trade quantities using the corrected concordances and locate compatible domestic production/capacity data.

## Run 028 — v0.14-rc16 (release rule fixed; first GOES adequacy result)
- ADR 006 amends ADR 005. Eval rows carry `claim_status`; failed results are withdrawn (published, never asserted) instead of blocking release. The sequencing fair gate still reports `passed: false`. `--strict` now exits 0. Re-claiming a failed row blocks release (tested).
- New `goes_import_floor.py`: sole-producer stated all-electrical-steel capacity (~226.8 kt/yr, upper bound on GOES) against 2019 use (220 kt) plus the NLR grid increment (94–114 kt) gives an import floor of 87.2–107.2 kt/yr = 3.23–3.97× 2019 imports. Break-even requires non-grid use to fall 39.6–48.7%. The 2026 "25% growth" hot-mill statement is not converted; a labeled +25% scenario still leaves 30.5–50.5 kt.
- Rejected: converting hot-mill growth into GOES capacity; using market-research-site consumption figures (e.g., "North America 420 kt"), which conflict with Commerce; using the secondary-source Defense contract figure in calculations.
- Census API query attempted via web fetch; query parameters were stripped, so annual trade quantities were not ingested. Recorded as next action with fallbacks.
- RUN_PROTOCOL section 6 added: owner priorities binding on scheduled runs.
- Tests 109/109; strict eval green; release verifier 9/11.

## Run 029 — v0.14-rc17 (data pipeline + stockpile + handoff)
- Defense Logistics Agency GOES contract (announced 2026-07-01; up to 53,000 short tons FY2025–29, stockpiled) added as an upper adjustment: +9.6 kt/yr max, floor up to 96.8–116.8 kt. Identified floor unchanged.
- `scripts/fetch_goes_trade.py` (stdlib only; HS6 totals + HS10 cross-check; errors recorded, not fatal) and `radiant/data/goes_trade_annual.py` (fail-closed loader: both HS6 headings in KG required; HS10 must match within 2%). The import floor auto-compares against the latest complete year when data exist.
- `.github/workflows/goes-data.yml`: pulls Census data on GitHub (monthly + manual) and commits the CSV. Needed because this environment cannot query the Census API.
- CI simulated locally with GitHub environment variables: tests, strict eval, attestation and `release --ci` all exit 0; only `hosted_ci_completed_green` remains, which requires the real run.
- Added `docs/OWNER_HANDOFF.md` with the exact push/verify steps and prompts.
- Added `scripts/record_completed_ci.py` (records the finished GitHub run and runs the final verifier) with tests.
- Tests 117/117; strict eval green; release verifier 9/11.



## Run 030 — v0.14-rc18 (producer aggregate + transformer-rule status)
- Added primary-source 2025 Cliffs 10-K measurement: 575 thousand net tons of combined stainless/electrical shipments. Explicitly not treated as GOES-specific production.
- Added DOE 2024 final-rule technology-mix fact: about 75% of distribution-transformer market can comply using GOES; the initial proposal likely implied ~95% amorphous shift. No tonnage conversion.
- Added DOE 2026 RFI status: April 2024 standards remain scheduled for compliance April 23, 2029 while DOE re-examines security/capacity/supply-chain effects. RFI is not treated as rescission.
- Retried Census annual trade acquisition; environment failed DNS before an API response, so no quantities were fabricated.
- Tests 118/118; strict eval green under ADR 006; release remains 9/11 pending real hosted GitHub execution.
- Weakest link: annual 2019–2025 GOES trade and GOES-specific domestic output remain missing.
- Exact next action: hosted GitHub push/CI, trigger `goes-data`, then interpret the resulting annual import series and country composition.


## Run 031 — v0.14-rc19 (trade ingestion fails closed)
- Audited the next-action GOES acquisition path before relying on it. Found a release-quality defect: `fetch_goes_trade.py` recorded network/API failures into CSV but returned exit code 0, so the scheduled GitHub workflow could have gone green and committed an unusable error-filled panel.
- Fixed the fetcher to return non-zero whenever any required HS6 annual import/export row is missing or errors. Diagnostic HS10 rows remain non-gating because historical concordances can differ by period.
- Strengthened `goes-data.yml`: installs requirements first, runs the import-floor parser, then the focused GOES trade/import-floor tests before any commit.
- Verified the exact Census variable contract against Census documentation: `CON_QY1_YR` is year-to-date imports-for-consumption quantity 1, `CON_VAL_YR` is year-to-date consumption value, `QTY_1_YR` is export YTD quantity 1, `ALL_VAL_YR` is export YTD total value, and `COMM_LVL` explicitly supports HS6/HS10.
- Added a regression test proving a required HS6 network error makes the fetch command exit 2 while preserving the diagnostic CSV.
- Full suite: 119/119 passing; strict eval green. Simulated GitHub Actions environment produces a valid hosted attestation and `release --ci` exits 0. Final local release remains 9/11 because no real hosted run has executed.
- Direct Census acquisition still times out in this runtime; no quantities were fabricated.
- Exact next action: push this candidate to a real GitHub repository and run `ci` + `goes-data`; a green `goes-data` run now has meaningful fail-closed semantics.

## Run 032 — v0.14-rc20 (ship-bar/eval gate alignment)
- Audited the executable v1.0 release verifier against the written ship bar and found a real loophole: `eval_harness_ci` did not require a measured improvement over an explicit baseline.
- Added `information_integrity_benchmark`: naive latest-revision reconstruction has 9/9 future-information violations on the archived BLS cutoffs; the bitemporal as-of representation has 0/9, a 100% reduction.
- Added this as a narrow `claimed` strict-historical-vintage result. It is explicitly an information-integrity result, not a forecasting-accuracy claim.
- Hardened `release.py`: the eval/CI gate now requires at least one passing claimed row with positive measured improvement. Withdrawn or merely integrity-tagged rows cannot satisfy the positive-evidence requirement.
- Updated release tests to enforce the new contract and added a direct regression test for the 9/9 -> 0/9 leakage result.
- Full suite: 120/120 passing; strict eval green. Final release remains 9/11 solely because real hosted GitHub execution and completed-success evidence are absent.
- Exact next action: publish rc20 to an owned Radiant repository and obtain real hosted CI. After that, trigger fail-closed GOES acquisition; do not advance Phase 2 until final 11/11 evidence exists.


## Run 033 — v0.14-rc22 (exact-candidate CI binding)
- Audited the final two release gates and found a provenance loophole: well-shaped hosted-CI records from an older commit could satisfy the final verifier because their SHA was not compared with the candidate being released.
- `radiant.release` now resolves the checked-out Git commit and requires both the hosted attestation and completed-success record to match that exact SHA. A copied ZIP without Git identity cannot satisfy hosted release gates.
- The two hosted records must also agree on repository, commit SHA, run ID, and run URL; mixed records from different successful runs fail closed.
- Added regression tests for stale-candidate evidence and mixed-run evidence. Full suite: 122/123 passing; strict eval green.
- Updated stale owner-handoff version references and interview/FINDINGS documentation.
- Final local release remains 9/11 because no real hosted run exists; this is now a stronger statement because old or unrelated green CI cannot clear the gate.
- Exact next action: push rc21, obtain one green `ci` run for that exact commit, run `scripts/record_completed_ci.py`, require 11/11, then trigger fail-closed `goes-data`.

## Run 034 — v0.14-rc22 (executable reproduction/demo receipts)
- Audited the remaining locally green ship gates and found three file-presence proxies: `one_command_reproduction` did not prove the command had run, `working_demo` did not prove the demo had run, and `tests_ci_green` accepted a report file without validating return code outside `--run`.
- Unified hosted CI around `bash scripts/reproduce.sh`. The command now runs pytest, strict evaluation, and the end-to-end demo before producing typed `radiant.tests.v1`, `radiant.demo.v1`, and `radiant.reproduction.v1` receipts.
- Hardened `radiant.release`: reproduction and demo gates require passing typed receipts; tests require `returncode == 0`. CI uploads the new receipts and demo output as release evidence.
- Added an adversarial regression test showing failed/stale execution receipts cannot clear those gates. Updated the CI strict-mode regression test to verify strict eval is reached through the one-command reproduction path.
- Full suite: 123/123 passing. `bash scripts/reproduce.sh` succeeds. Final verifier remains 9/11 only because real hosted execution and completed-green evidence for the exact candidate are absent.
- Scientific claims unchanged: bitemporal information integrity is 9/9 -> 0/9 future-information violations; forecasting superiority remains withdrawn; GOES remains a conditional import-floor result, not a shortage finding.
- Exact next action: push rc22, obtain a green hosted `ci` run for its exact SHA, record that completed run, require 11/11, then trigger fail-closed `goes-data`.


## Run 035 — v0.14-rc23 (source-bound execution receipts)
- Adversarially audited Run 034's executable receipts and found a remaining staleness loophole: a previously passing test/demo/reproduction JSON could survive a later source-code or workflow edit and still satisfy local ship gates.
- Added `radiant/source_fingerprint.py`, a deterministic SHA-256 fingerprint over executable/scientific inputs: package code, data, schemas, ontology, scripts, examples, tests, workflows, Dockerfile and requirements. Cache/generated artifacts are excluded.
- Upgraded test, demo and reproduction receipts to v2; each records the source fingerprint present when it ran. The release verifier recomputes the fingerprint and rejects receipts from any different source state.
- Added an adversarial regression test that creates passing receipts, mutates executable source, and proves all three execution gates close.
- No scientific claim changed. Forecasting superiority remains withdrawn; bitemporal information integrity remains 9/9 -> 0/9 future-information violations; GOES remains a conditional import-floor result, not a shortage finding.
- GitHub connector inspection found no existing Radiant repository available to push into, so real hosted CI remains an external ownership/setup blocker rather than something this run can truthfully simulate away.
- Full suite and one-command reproduction rerun after all executable changes: 124/124 passing; strict eval green; local final release remains 9/11 pending exact-candidate hosted CI and completed-success evidence.
- Exact next action: create/select an owned GitHub repository, push rc23, obtain one green `ci` run for that exact SHA, record the completed run, require 11/11, then execute fail-closed `goes-data`.


## Run 036 — v0.14-rc24 (hosted test receipt preservation)
- Audited the exact hosted-CI handoff and found a blocking bug: `scripts/reproduce.sh` correctly emitted a source-bound `radiant.tests.v2` receipt, but the later `python -m radiant.release --run --ci` step overwrote it with an untyped `{returncode,stdout,stderr}` object. The CI job could pass because its gates were computed before that overwrite, yet the downloaded evidence could never satisfy final verification.
- Fixed `radiant.release --run` so rerunning tests writes the same v2 schema and current source fingerprint instead of destroying the receipt contract.
- Added a regression test that executes the `--run` path and verifies the resulting test receipt remains typed, successful, and bound to the current source fingerprint.
- Corrected stale current-status text left from earlier release candidates.
- Scientific claims unchanged: forecasting superiority remains withdrawn; bitemporal integrity remains 9/9 -> 0/9 future-information violations; GOES remains a conditional import-or-stock-draw floor, not a shortage claim.
- Full suite and one-command reproduction rerun after changes: 125/125 passing; strict eval green; local final release remains 9/11 pending exact-candidate hosted CI and completed-success evidence.
- Exact next action: create/select an owned GitHub repository, push rc24, obtain one green `ci` run for that exact SHA, record the completed run, require 11/11, then execute fail-closed `goes-data`.


## Run 037 — v0.14-rc25 (automatic exact-run finalization)
- Audited the remaining hosted handoff and removed an unnecessary manual provenance step. Previously a human had to run `record_completed_ci.py` after CI, creating an avoidable gap between a green hosted run and final 11/11 verification.
- Added `.github/workflows/finalize-release.yml`, triggered only when the named `ci` workflow completes. It runs only for upstream `success`, checks out the exact upstream `head_sha`, downloads evidence from that exact run ID, writes a completed-success receipt from GitHub event identity, and runs the ordinary final release verifier.
- Added `scripts/write_completed_ci_from_env.py` with fail-closed validation of repository, SHA, run ID, canonical GitHub run URL, status and conclusion. It cannot create a success receipt for failed/in-progress/mismatched evidence.
- Added regression tests for failed status/conclusion, mismatched URL, malformed SHA, and workflow binding to the exact upstream SHA/run.
- Scientific claims unchanged: forecasting superiority remains withdrawn; bitemporal integrity remains 9/9 -> 0/9 future-information violations; GOES remains a conditional import-or-stock-draw floor, not a shortage claim.
- Full suite and one-command reproduction rerun after changes: 127/127 passing; strict eval green; local final release remains 9/11 because no real hosted run exists.
- Exact next action: create/select an owned GitHub repository and push rc25. Green `ci` must automatically trigger green `finalize-release` and final 11/11 for the same SHA; then execute fail-closed `goes-data`.


## Run 038 — v0.14-rc26 (clean-container reproduction becomes executable evidence)
- Audited the written ship bar against the release verifier and found that “one-command reproduction from a clean machine/container” was still only proven by a host-side `scripts/reproduce.sh` receipt plus the existence of a Dockerfile. No CI step actually built and ran the Docker image.
- Added `scripts/reproduce_container.sh`: it builds the image with `--pull`, runs the complete reproduction inside the container, and writes `radiant.container_reproduction.v1` only after Docker exits successfully.
- Added `.dockerignore` so Git state, generated artifacts, logs, caches, and archives cannot contaminate the clean build context. `.dockerignore` is now itself source-fingerprinted.
- Hosted `ci` now executes the clean-container path and uploads its source-bound receipt. The release verifier requires both the ordinary reproduction receipt and the clean-container receipt for the single reproduction gate.
- Added regression tests for CI wiring, fail-closed receipt ordering, and clean Docker context. Full suite: 130/130 passing; strict eval and host reproduction green.
- Docker is not installed in this execution runtime, so no clean-container receipt was fabricated. The stricter local verifier is therefore 8/11: clean-container reproduction plus the two hosted-CI gates remain open. This is a deliberate tightening, not a regression in scientific results.
- Scientific claims unchanged: forecasting superiority remains withdrawn; bitemporal integrity remains 9/9 -> 0/9 future-information violations; GOES remains a conditional import-or-stock-draw floor, not a shortage claim.
- Exact next action: push rc26 to an owned GitHub repository. Hosted `ci` must build/run the clean container and clear the reproduction gate; then `finalize-release` must clear the two hosted gates for 11/11; only then run fail-closed `goes-data`.

## Run 039 — v0.14-rc27 (external review; first-hosted-run bug fix; protocol loophole closed)
- Review finding: Runs 031–038 were eight consecutive release-infrastructure runs with no new sourced fact, which violates RUN_PROTOCOL §6.1. The escape clause ("explain why impossible") was used repeatedly with the same network excuse. Added §6.7 (release infrastructure frozen until a real hosted run exists, except fixes for failures seen in a real run log) and §6.8 (network unavailability does not exempt a run from finding a sourced fact).
- Bug fix: `scripts/reproduce_container.sh` ran the container as root while bind-mounting `artifacts/`. On a GitHub runner, root-owned receipts would make the next host step (`python -m radiant.release --run --ci`, which rewrites `artifacts/test_report.json`) fail with permission denied. The container now runs as the host user with HOME=/tmp, no bytecode and no pytest cache. A read-only-tree simulation of that setup passes `scripts/reproduce.sh`. Regression test added.
- Fixed a stale eval limitation string that still said the release gate fails (contradicting ADR 006).
- OWNER_HANDOFF updated: the finalize-release workflow makes the post-CI step automatic; the owner is advised to pause scheduled runs until the first push.
- Tests 131/131; strict eval 0; local release 8/11 (container gate needs Docker, which exists on GitHub runners; hosted gates need a real run). No scientific result changed.



## Run 040 — v0.14-rc28 (embodied GOES imports quantified; steel-only dependence shown incomplete)
- Followed RUN_PROTOCOL §6.7/§6.8 and the owner brief: no GitHub, CI, release-gate, receipt, fingerprint, Docker, or workflow changes. The work session returned to real GOES evidence.
- Searched primary/official sources for the highest-priority missing annual 2020–2025 direct GOES tonnage. No suitable published U.S. tonnage table for that period was found in the sources reviewed, so the run moved to the next queue item: GOES embodied in imported transformer components.
- Added Commerce Section 232 evidence: **68 kt GOES-equivalent** in imported transformer laminations and cores in 2019. Commerce explicitly says customs collect these items in units and that the weight estimate uses Core Coalition public comments; possible double counting from U.S.-origin GOES re-imported in cores is noted as likely minimal. Evidence is therefore typed as an estimate, not measured customs tonnage.
- Added Commerce's reported Core Coalition **96 kt GOES-equivalent estimate for 2020**. Commerce says first-half 2020 trade data validated the direction of the increase; the value remains an industry estimate reported by a federal agency.
- Added DOE's directly counted **842,929 stacked-core import units through October 2021** under HTS **8504.90.9638**, versus 50,267 in 2016. No mass conversion was attempted because no defensible weight distribution was supplied.
- Derived context only: 68 kt embodied GOES in 2019 laminations/cores is ~**2.52×** the 27 kt of direct GOES steel imports already in Radiant. This ratio is computed from the two sourced quantities and is not treated as a new measured fact.
- The identified **87–107 kt/year future import-or-stock-draw floor is unchanged**. Historical derivative imports show the import channel is broader than steel-form trade; they are not a new demand term or domestic production measurement. No shortage is claimed.
- Added regression tests enforcing evidence typing, preserving the floor, and forbidding silent conversion of stacked-core unit counts into GOES mass. First full test run exposed one legacy string-contract failure in `tests/test_goes_trade_annual.py`; fixed the interpretation text without weakening the test. Final: **133/133 tests pass**; `python -m radiant.eval --strict` exits **0**.
- Exact next action: source annual U.S. direct GOES import tonnes for 2020–2025 from an official published table/DataWeb-style export with explicit HTS coverage; if unavailable, move to foreign GOES capacity or 2026 tariff status.

### Run 041 (v0.14-rc29)
- Added producer-primary foreign GOES supply evidence: JFE/JSW's $670M India GOES JV (FY2027 planned full operation) and thyssenkrupp's 2026 Isbergues curtailment (50% capacity Jan-May; shutdown announced Jun-Sep).
- Kept both outside the U.S. import-floor equation because neither source identifies U.S.-available tonnage.
- 134 tests pass; strict eval exits 0. Import floor unchanged at 87.2-107.2 kt/year; no shortage claim.

### Run 042 — quantified foreign GOES capacity
- Added JFE's producer-primary August 2025 plan for 350 kt/year combined India GOES capacity by 2030 (100 kt/year Vijayanagar; 250 kt/year Nashik; Nashik current 50 kt/year).
- Kept it out of the U.S. import-floor arithmetic because nameplate capacity in India is not identified U.S.-available supply.
- Import-or-stock-draw floor remains 87.203815–107.203815 kt/year; no shortage claim.

### Run 043 — current GOES tariff status
Added two official tariff-policy evidence records: the current HTSUS Column 1 general rate for GOES is Free, while 2026 Section 232 treatment places steel articles in headings 7225/7226 under a 50% additional ad valorem duty on full value. Kept tariff parameters out of the physical quantity floor because no import-response elasticity is identified. 136 tests pass; strict eval green. The observed 2020–2025 U.S. GOES import panel remains the binding empirical gap.


### Run 044 — North American embodied-GOES routing
- Added Commerce Section 232 evidence that >99% of Mexican and >90% of Canadian transformer-component exports were destined for the U.S.; neither country had domestic GOES production capability.
- Typed the 90% Canadian figure as a lower bound and refused conversion into GOES mass. Import floor unchanged; no shortage claim.

### Run 045 — 2020 direct-GOES source concentration
- Added DOE-published 2020 U.S. GOES import value: $29M under HS 722511; source shares 85% South Korea, 6% Brazil, 4% Russia.
- Kept value/source shares separate from tonnage; no price-based conversion and no floor change.
- Added regression coverage and reran full tests + strict eval.

### Run 046 — v0.14-rc34 (EU safeguard reaches GOES embodied in transformers)
- Added an official-government summary of Commission Implementing Regulation (EU) 2026/2133: from 2026-09-25, covered transformer cores imported already inside transformers face a provisional EUR 1,140/tonne-of-core duty rather than the quota mechanism; provisional application runs through 2027-02-26.
- Typed this strictly as foreign trade-policy context. No diversion, price elasticity, global-output response, U.S.-available tonnage, or shortage effect is inferred.
- The 87.2–107.2 kt/year conditional U.S. import-or-stock-draw floor is unchanged.
- 139/139 tests pass; strict eval exits 0. Release infrastructure remained frozen under RUN_PROTOCOL §6.7.
- Exact next action: recover an official 2020–2025 U.S. direct-GOES mass observation/panel covering 7225.11 + 7226.11 (or documented descendants); if unavailable, add another quantified official direct/embodied GOES supply observation without manufacturing conversions.

## Run 047 — v0.14-rc35
- Added IEA 2023 global GOES production-capacity context: ~3.8 Mt/year, with almost 85% concentrated in China, Japan, Korea, Russia, and the United States.
- Preserved IEA's 6 Mt/year 2030 GOES demand value as a Net Zero scenario, not observed demand or a shortage claim.
- Added regression coverage proving global capacity/scenario context cannot enter the identified U.S. 87–107 kt/year import floor.
- Verification: 140 tests pass; `python -m radiant.eval --strict` exits 0. Release infrastructure remains frozen under RUN_PROTOCOL §6.7.
- Binding gap: official 2020–2025 U.S. direct-GOES mass panel with explicit HTS coverage.

## Run 048 — v0.14-rc36
- Pursued the binding SIMA/Census mass-panel route first. Commerce's static SIMA page confirms downloadable files incorporate Census and license data and contain quantity/value, but the XLSX payload still could not be fetched in this runtime; no third-party reconstruction was adopted.
- Added JFE producer-primary evidence of an actual foreign-to-U.S. GOES route: JFE's first U.S. JGreeX GOES application/order was for Eaton's U.S. IT data-center transformers via Toyota Tsusho (2024-06-20).
- Kept the order context-only because JFE publishes no mass, price, or recurring annual volume. The 87.2–107.2 kt/year conditional floor is unchanged; no shortage claim.

### Run 049 / v0.14-rc37
- Added Commerce-official product-scope evidence separating direct GOES headings 7225.11/7226.11 from laminations/cores 8504.90.13.
- No fabricated tonnage and no change to the 87–107 kt/year conditional floor.
- SIMA XLSX remains inaccessible in this runtime; official 2020–2025 U.S. direct-GOES mass panel remains binding.

## Run 050 — v0.14-rc38 (distribution-transformer material-demand cross-check)
- Pursued the official 2020–2025 GOES mass panel first; the public Census/USITC documentation confirms quantity-capable official systems, but this runtime still did not yield the requested annual HTS quantity payload. No third-party reconstruction was adopted.
- Added DOE's 2024 final-rule estimate of 225 kt/year current U.S. electrical-steel demand for distribution transformers.
- Separately added the MTC estimate, as reported by DOE, of approximately 175 kt/year GOES consumption for distribution transformers. It remains explicitly stakeholder evidence, not DOE-measured trade data.
- Neither value enters the 87–107 kt/year conditional import floor: 225 kt includes non-GOES material; 175 kt has narrower end-use scope and different provenance/vintage than the 2019 all-use baseline.
- Added a regression test enforcing those scope/provenance boundaries. Full suite: 143/143 passing; strict eval exits 0.
- Exact next action: obtain official 2020–2025 direct-GOES quantities for 7225.11 + 7226.11 U.S. descendants from SIMA/Census/DataWeb; use the new 175/225 kt downstream observations only as cross-checks, not substitute trade mass.

## Run 051 — v0.14-rc39 (official GOES HTS10 scope resolved)
- Pursued the binding direct-GOES panel first. The annual 2020–2025 quantity payload remains unavailable in this runtime, but Commerce primary material resolves the exact U.S. customs decomposition used for GOES: 7225.11.0000, 7226.11.1000, 7226.11.9030, and 7226.11.9060.
- Added that mapping as federal product-scope evidence and a regression test proving it cannot enter the physical import-floor arithmetic or masquerade as recent tonnage.
- This closes the HTS-coverage sub-blocker: Radiant's existing HS10 cross-check is now directly sourced. The remaining blocker is observations, not classification scope.
- Preserved a negative implementation result: the first test collection failed on an unescaped apostrophe in the new evidence string; fixed without weakening evidence or tests.
- Final verification: 144/144 tests pass; strict eval exits 0. Forecasting superiority remains withdrawn; 87.203815–107.203815 kt/year conditional floor unchanged; no shortage claim.
- Exact next action: retrieve 2020–2025 Census/SIMA/DataWeb annual quantities for the now-sourced four-line HTS10 set (and HS6 totals as a consistency check), ingest them fail-closed, then compare observed imports with the conditional floor.

## Run 052 — v0.14-rc40 (GOES trade estimand made executable)
- Audited the unresolved Census ingestion path before accepting any future quantity payload.
- Census primary documentation distinguishes imports-for-consumption quantity (`CON_QY1_YR`) from general-import quantity (`GEN_QY1_YR`). Radiant's material-balance estimand uses imports for consumption; this is now an explicit tested contract rather than an implicit field choice.
- Added regression coverage pinning the Run-051 Commerce four-line HTS10 GOES scope and preventing a silent switch to general-import fields.
- Removed downloader wording that implied HS classification continuity across years without verification. Historical concordance remains fail-closed.
- No recent tonnage was recovered or fabricated; conditional floor unchanged and no shortage claim.
- Exact next action: retrieve December YTD `CON_QY1_YR` for 2020–2025 for HS6 722511/722611 and the four sourced HTS10 lines, verify KG units and HTS10↔HS6 reconciliation, then ingest.

## Run 053 — v0.14-rc41 (external review: headline correction)
- Review of Runs 040–052: protocol now followed; 12 of 13 runs added sourced facts. None moved the number, but Run 040's embodied-core estimate invalidated the headline ratio.
- Finding: "3–4× 2019 imports" divided an all-forms grid increment, netted against a sheet-only baseline, by sheet imports only. Commerce estimates 68 kt of GOES embodied in 2019 core imports versus 27 kt of sheet.
- Added `all_forms_view()`: 2019 all-forms use 288 kt, 95 kt (33.0%) foreign; foreign floor 155.2–175.2 kt/yr = 1.63–1.84× 2019 and 40.6–43.6% of use. Identity test: sheet floor + flat 68 kt cores = all-forms floor.
- Headline rewritten in README, FINDINGS, interview walkthrough, owner handoff and GPT brief. "3–4×" withdrawn as headline; the sheet-channel floor is retained as a conditional framing.
- GPT brief: next priority is newer embodied-core tonnage (now the largest foreign channel); cadence guidance added.
- Tests 148/148; strict eval 0.



## Run 054 — v0.14-rc42 (recent derivative-channel observation)
- New sourced fact: Cleveland-Cliffs federal-docket submission reproducing USITC DataWeb shows 147,652,598 U.S. lamination import units in 2024 under HTS 8504.90.9534 + 8504.90.9634; Mexico supplied 129,877,076.
- January-February 2025: 25,059,726 units, +6% year over year.
- Evidence remains unit counts, not mass; no conversion to GOES tonnes was made.
- Run 053 all-forms headline unchanged; no shortage claimed.
- 149/149 tests pass; strict eval exits 0.


## Run 063 — release-status synchronization
- Corrected stale top-level status text that still described the pre-hosted-CI Run 054 state.
- Radiant v1.0 is recorded as shipped at exact SHA `2044ca5f8a235889a27733f58b3c0cdf5c11a7c8`; hosted finalization evidence has passed the full ship-bar check on that SHA.
- No scientific result, baseline, dataset, model, or withdrawn claim was changed. Historical run entries remain append-only.
- Phase 2 remains selection-gated: no candidate implementation begins without Logan's explicit approval.
- Exact next action: keep Radiant green and maintain the three Phase-2 charters; after explicit approval, start exactly one WIP.
