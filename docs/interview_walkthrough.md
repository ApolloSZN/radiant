# Radiant — interview explanation guide

## 30-second version

Radiant is an evidence-first system for testing claims about industrial and technological systems. It separates what is measured, what is only bounded, and what is assumed, and it tracks when each fact became knowable.

Its main finding: in 2019 about a third of the transformer steel America used came from abroad, mostly hidden inside imported transformer cores. The grid buildout pushes that to at least 41–44%, even if America's only producer made nothing but that steel at full capacity. I originally headlined it as "3–4× more imports," but that only counted steel arriving as sheets. Once a Commerce estimate of steel inside imported cores was in the data, I corrected my own headline. My early forecasting result also failed a fair-baseline test, so I withdrew it.

## Two-minute version

Radiant started as a cross-scale adaptive-system architecture, but I forced it into executable claims. At the bottom is a bounded adaptive-system kernel. I keep RAF autocatalytic closure separate from material viability: a network can be topologically self-enabling and still fail because its stocks, rates, energy, capacity, maintenance or timing are insufficient. The viability layer therefore has steady-state, finite-horizon and period-resolved stock-flow tests.

The evidence layer is bitemporal. Every observation has the date it describes and the date it became knowable. That lets the forecast harness replay historical cutoffs without importing later revisions. Forecasts are hashed before resolution and scored later.

The most important evaluation lesson came from DNA-sequencing costs. My causal selector initially reduced MALE from 0.7836 to 0.1762 versus an all-history trend, which is a 77.5% improvement. I then audited it against a predeclared panel of recent-window and no-change baselines. A rolling-3 trend gets 0.1493 and beats the selector by about 18%. I also implemented follow-the-leader and exponential-weights online learners; they improve on my selector but still do not robustly beat rolling-3. So I downgraded the claim and changed CI: the scientific release gate is red now. The project cannot ship v1.0 by pointing to the weak comparator.

On the industrial side I encoded a large-power-transformer production network with evidence-typed parameters, LP constraint resolution and partial identification. One defensible result is that projected grid expansion requires an identified **87–107 kt/year minimum of GOES imports or stock drawdown** under the stated baseline conditions, even using the sole U.S. producer's all-electrical-steel capacity as a generous upper bound on GOES supply. I still do not call a shortage because imports can respond. The latest evidence also shows why steel-form trade is incomplete: Commerce estimated **68 kt of GOES entered inside imported laminations and cores in 2019**, versus about 27 kt imported directly as GOES steel, and DOE later counted **842,929 stacked-core imports through October 2021** under HTS 8504.90.9638. I keep those as context because the tonnage estimates use industry weight assumptions and the 2021 customs quantity is in units, not tonnes.

The engineering point is that Radiant treats negative and unidentified results as valid outputs. Tests, ADRs, provenance, Docker reproduction, a public write-up and release gates are part of the research system rather than packaging added afterward.

## Likely follow-up questions

### "Why isn't the 77.5% result your headline anymore?"
Because it was conditional on a weak comparator. The all-history trend cannot adapt to the sequencing regime shift. Once I compared against recent-window trends, rolling-3 and rolling-4 beat my selector. The 77.5% number is still true for that one comparison, but it is not evidence of a general forecasting advantage.

### "Did you try to fix the selector after that?"
Yes, but I avoided post-hoc hyperparameter hunting. I implemented two standard causal online aggregation formulations: follow-the-leader and exponential weights with a deterministic time-varying learning rate. They improved MALE to 0.1561 and 0.1641 respectively, but rolling-3 is still better at 0.1493. I preserved the negative result.

### "Why make CI fail?"
Because the repo had an inconsistency: the docs admitted the headline failed a fair-baseline audit, but the release harness still passed by using all-history. I changed the executable gate so a falsified claim cannot be used as release evidence; the current positive gate is the separately measured bitemporal leakage reduction.

### "Isn't picking rolling-3 after seeing the data also post-hoc?"
It is not being proposed as the new deployed model. It is the strongest member of a predeclared simple-baseline panel used as a conservative evaluation benchmark. The next valid predictive test should freeze a policy before evaluating genuinely held-out or historical-vintage series.

### "What did the transformer work actually establish?"
It established some accounting and physical bounds, not a unique bottleneck. In 2019, reported U.S. production, imports, exports and utilization imply that even full use of existing domestic nameplate capacity would not have eliminated imports. For GOES, projected demand pressure is large, but adequacy remains unidentified until the supply side is assembled.

### "What was the latest data-engineering bug?"
I had modeled GOES as two six-digit commodity headings, which is correct at the coarse classification level but unsafe for direct current U.S. import extraction. Commerce currently splits the narrow-width heading across three ten-digit HTS codes, so total current imports need four codes. Exports use a different, coarser concordance. I changed the ingestion contract to be direction- and effective-period-specific and to fail on missing codes.

### "How did you get the steel number?"
Three public numbers: the sole producer's stated capacity for all electrical steel (an upper limit on the steel in question), 2019 U.S. consumption from the Commerce Department, and a 2026 DOE-funded lab estimate of extra grid demand. Demand minus the most domestic supply could be gives the minimum imports. I also report how far everyday demand would have to fall for the gap to close (about 40–49%). I refused to turn a vague "25% expansion" quote into a steel figure.

### "Why did you change the release rule again?"
The earlier fix made the project unshippable unless it won at forecasting. The honest rule is simpler: you can't claim what failed. Failed results are withdrawn and published, and claiming one again requires passing the same fair test.

### "What would you do next?"
For forecasting, freeze the algorithm and evaluate on new held-out or strict historical-vintage technology series rather than tuning on sequencing again. For the industrial case, the 2025 10-K now gives 575 thousand net tons of combined stainless-and-electrical shipments, but not GOES alone, so I refused to relabel it as GOES output. The next binding measurement is annual 2019–2025 Census GOES trade and a GOES-specific production split if one can be sourced.


## Run 031 reliability example
**30 seconds:** Before trusting the automated trade pipeline, I tested its failure behavior. I found that a Census outage could write error rows but still make GitHub Actions green. I changed the downloader to fail closed on any required HS6 row and added a regression test. So a green data job now means the required annual totals were actually retrieved, not merely that a CSV file exists.

**Likely follow-up — Why is this important?** Because provenance is not enough if acquisition failures are silently accepted. In an evidence system, the data pipeline itself is part of the scientific claim. I kept HS10 as a diagnostic because detailed tariff codes can change historically, while the stable HS6 pair is the required aggregate.

## Run 032 gate-integrity example
**30 seconds:** I audited the release verifier against its own written ship bar and found a loophole: it required strict historical-vintage evidence, but not an actual measured win over a baseline. I closed that loophole and added a concrete benchmark. A naive latest-revision reconstruction leaks future BLS revisions at all 9 historical cutoffs; Radiant's as-of representation leaks at 0 of 9, a 100% reduction. CI now requires at least one positive claimed baseline comparison, so a negative forecast cannot accidentally satisfy the positive-evidence gate.

**Likely follow-up — Is that a forecasting win?** No. It is an information-integrity win. The BLS predictive correction is still worse than the no-correction baseline and remains published as a negative result. The positive claim is narrower: bitemporal replay prevents a specific, measured class of look-ahead leakage.


## Run 033 release-provenance example
**30 seconds:** I audited the last two CI gates and found they validated the shape of GitHub evidence but did not bind it to the exact commit being released. That means stale green evidence could theoretically be reused. I changed the verifier so the attestation and completed run must match the checked-out commit and each other on repository, SHA, run ID, and URL. I added regression tests for both stale-commit and mixed-run attacks.

**Likely follow-up — Why not trust a green badge?** A green badge says some commit passed. Reproducible release evidence has to say this exact candidate passed. The verifier now makes that distinction executable.


## Run 034 interview update

**30 seconds:** I audited the release checker itself and found that some ship gates were based on file existence. I changed CI so the same one-command reproduction path actually runs tests, strict eval, and the demo, then emits machine-readable receipts. The release checker now validates those receipts and rejects stale or failed ones.

**Two minutes:** Radiant already had a release verifier, but I treated that verifier as code that also needed adversarial testing. I found three evidence gaps: the reproduction gate only checked for a script and Dockerfile, the demo gate only checked that the demo source existed, and the tests gate could accept a test-report file without validating success. I unified CI around `scripts/reproduce.sh`. That command runs pytest, the strict eval, and the demo, and only then emits typed reports. The release verifier requires those passing reports. I added a negative test that supplies failed reproduction/demo/test receipts and verifies the gates stay closed. The scientific outputs did not change; this is release-integrity work that makes the 11/11 claim harder to fake accidentally.

**Likely follow-up — did this make the science better?** Not directly. It made the reproducibility and deployment claim more defensible. I keep that separate from scientific evidence.

**Likely follow-up — why not call v1.0 now?** The exact rc22 commit still has to run on real hosted GitHub Actions and finish green. Local simulation is not substituted for that external receipt.


## Run 035 source-binding example
**30 seconds:** I found that even a real passing receipt can become stale if code changes afterward. I added a deterministic fingerprint over the executable and scientific inputs. Tests, demo, and reproduction now record that fingerprint, and the release verifier rejects them if the current source differs. I added a regression test that deliberately changes source after a green run and proves the gates close.

**Likely follow-up — isn't the Git commit enough?** Hosted CI is commit-bound, but the local ship gates also need to fail closed before hosted evidence exists. Source-bound receipts make the invariant explicit and testable in both environments.


## Run 036 hosted-evidence handoff example
**30 seconds:** I traced the exact artifact lifecycle through hosted CI and found a bug that would have made final release impossible. The reproduction step wrote a source-bound test receipt, but a later release command overwrote it with an older schema after the gate had already been evaluated. CI could look green while the downloaded evidence was unusable. I fixed the writer and added a regression test for the persisted artifact, not just the in-memory gate.

**Likely follow-up — why did tests not catch this earlier?** Earlier tests checked whether the release gate passed, not the state of the evidence file after the command completed. The new regression test checks the artifact that the next stage actually consumes.


## Run 037 automatic finalization example
**30 seconds:** The last release step still depended on a human copying a successful GitHub run into the release evidence. I replaced that with a separate workflow that fires only after CI completes successfully, checks out the exact CI SHA, downloads that exact run's evidence, writes a validated completion receipt, and runs the final 11/11 verifier. I added negative tests for failed runs and identity mismatches.

**Likely follow-up — can the finalizer bless a failed run?** No. GitHub gates the job on upstream success, and the receipt writer independently requires `completed` plus `success`, a valid SHA/run ID, and a canonical run URL. The ordinary release verifier then cross-checks that receipt against the attestation from the upstream CI run and the checked-out commit.

## Run 038 clean-container reproducibility example
**30 seconds:** I found that our “clean reproduction” release gate was still a proxy: we had a Dockerfile and a successful host reproduction, but CI never actually built and ran the container. I tightened the gate. CI now builds the Docker image, runs the entire test/eval/demo reproduction inside it, and only then emits a source-bound receipt. Because Docker is unavailable in the current sandbox, I refused to fake that receipt, so the local ship score intentionally dropped until real hosted CI runs it.

**Likely follow-up — why is a lower gate count progress?** Because the old green gate overstated what had been demonstrated. A release gate is useful only if it executes the property it claims to verify. Tightening a false-positive gate increases reproducibility even when the immediate score falls.


## Run 040 embodied-GOES evidence example
**30 seconds:** Direct GOES import statistics miss steel that arrives already fabricated into transformer cores. Commerce estimated 68 thousand metric tons of GOES entered the U.S. inside imported laminations and cores in 2019, versus about 27 thousand tonnes imported directly as GOES steel. DOE then reported 842,929 stacked-core import units through October 2021 under HTS 8504.90.9638. I did not turn the unit count into tonnes because the data do not provide a defensible weight distribution.

**Likely follow-up — did this change the 87–107 kt import floor?** No. It strengthens the evidence that the U.S. already depends on foreign GOES through derivative products, but those historical core imports are a supply channel, not an extra term in the future-demand equation. The 68 kt and 96 kt figures also rely on Core Coalition weight estimates reported by Commerce, so they are kept distinct from measured customs tonnage.

**Likely follow-up — why is this important?** Because looking only at HTS codes for GOES sheet can materially understate dependence. The physical material can cross the border after being cut and assembled into laminations or cores, so a serious supply model has to track both steel-form and embodied-material trade without double counting.

### Run 041 follow-up: what do we know about foreign GOES supply?
**30 seconds:** Foreign supply is not static. JFE and JSW are building a $670M dedicated GOES operation in India for full operation in FY2027, while thyssenkrupp reported its French Isbergues GOES site at 50% capacity in early 2026 with a June-September shutdown. I record those as supply context, not tonnes available to the U.S., because neither source gives that quantity.

**Likely follow-up — did this reduce the U.S. import floor?** No. The 87-107 kt/year result is a conditional U.S. material-balance floor. A foreign investment amount or utilization percentage cannot be subtracted from it without evidence for actual GOES tonnage available to U.S. buyers.

### Run 042 GOES follow-up
A producer-primary JFE announcement now quantifies a major foreign expansion: the JSW-JFE Indian GOES system is planned to reach 350 kt/year by 2030, versus 50 kt/year currently stated at Nashik, with 100 kt/year planned at Vijayanagar and 250 kt/year at Nashik. Radiant treats that as future foreign nameplate capacity, not as U.S.-available supply, so it does not subtract it from the 87–107 kt/year U.S. conditional import floor.

### Run 043 follow-up: are tariffs already included in the GOES result?
No. The physical floor is a quantity balance, not a price model. I verified that current GOES headings have a Free ordinary Column 1 rate but are within the 50% Section 232 steel-article coverage in the 2026 proclamation. I store that as policy context and refuse to invent an import-response elasticity. The next useful observation is still actual annual import tonnage after 2019.


### Run 044 follow-up
A useful nuance is that U.S. customs data on GOES sheet miss indirect dependence. Commerce found >99% of Mexican and >90% of Canadian transformer-component exports went to the U.S., while neither country produced GOES domestically. I keep that as routing evidence only—not tonnes—because component weights are not identified.

### Run 045 follow-up
**If asked what the 2020 trade evidence adds:** DOE reports $29M of direct GOES imports under HS 722511 in 2020, with 85% of import value from South Korea. I kept that as measured concentration evidence rather than dividing dollars by an assumed steel price to manufacture tonnes. The mass panel is still an explicit missing measurement.

## Run 046 trade-policy propagation example
**30 seconds:** I found a current EU safeguard that illustrates why GOES dependence has to be modeled through finished products, not only steel sheet. From September 25, 2026, the EU applies a EUR 1,140-per-tonne duty to covered transformer cores even when the core arrives inside a finished transformer. I encoded that as foreign policy context but did not pretend it changes U.S. supply, because no diversion effect is identified.

**Likely follow-up — why does this matter for Radiant?** It shows a real regulator treating the material constraint as a value-chain problem: restricting sheet alone can be bypassed by moving fabrication abroad. Radiant already separately tracks direct GOES, laminations/cores, and finished-transformer channels, so this is an external check on that decomposition. It still does not identify U.S. import tonnes or a shortage.


## Run 047 global-capacity context
**30 seconds:** I added an IEA system-level check: global GOES production capacity is about 3.8 million tonnes per year and almost 85% is concentrated in five countries. IEA's Net Zero scenario has GOES demand reaching 6 million tonnes per year by 2030. I keep that 6 Mt figure explicitly as a scenario, not observed demand, and I do not use global nameplate capacity as U.S.-available supply.

**Likely follow-up — does 6 Mt versus 3.8 Mt prove a shortage?** No. They are not same-date observed supply and demand: 3.8 Mt is current capacity context in the report, while 6 Mt is a 2030 scenario demand trajectory. Capacity can expand and utilization matters. The comparison identifies a scale-up requirement, not an identified shortage.

## Run 048 U.S. foreign-supply-route example
**30 seconds:** I separated “foreign capacity exists” from “foreign GOES can actually reach U.S. transformer buyers.” JFE documents a 2024 grain-oriented-steel order for Eaton's U.S. data-center-transformer business, delivered through Toyota Tsusho. That proves a real supply route, but the release gives no tonnes, so I do not use it to reduce the 87–107 kt/year import floor.

**Likely follow-up — why is one order useful if there is no tonnage?** It falsifies the stronger assumption that foreign capacity is purely hypothetical for U.S. buyers, while still leaving the magnitude unidentified. The model represents those as different evidence claims rather than filling the missing quantity with an assumption.

### Run 049 follow-up: why separate steel from cores?
**30 seconds:** Commerce's own safeguard notice classifies GOES sheet under 7225.11/7226.11 and transformer laminations/cores separately under 8504.90.13. Radiant now encodes that distinction so a direct-steel import series cannot be mistaken for total foreign GOES dependence.

**Likely follow-up — did this change the 87–107 kt result?** No. It improves measurement scope, not the quantity inputs. The missing 2020–2025 U.S. mass series is still unresolved.

### Run 050 follow-up: what is the downstream GOES demand scale?
**30 seconds:** DOE's 2024 transformer rule estimates about 225 thousand metric tons per year of electrical steel is used in U.S. distribution transformers. The same federal record reports an industry estimate of about 175 thousand tonnes of GOES specifically. I keep those evidence classes separate: the first is DOE's all-core-steel demand estimate, the second is a stakeholder GOES estimate. Neither gets added to the import-floor equation because that would mix scopes or double count demand.

**Likely follow-up — why not replace the 220 kt baseline with 175 kt?** They measure different things and vintages. The 220 kt condition is 2019 apparent GOES consumption across uses; 175 kt is a later stakeholder estimate for distribution transformers only. Substituting one for the other would silently change the estimand. The useful next test is the official annual import-mass panel.

### Run 051 follow-up: which U.S. tariff lines actually define the direct-GOES query?
**30 seconds:** Commerce's GOES investigation identifies four U.S. customs lines: 7225.11.0000 plus 7226.11.1000, 7226.11.9030, and 7226.11.9060. Radiant's importer already cross-checked those lines, but Run 051 added the primary-source justification and a regression test. It resolves classification scope, not the missing 2020–2025 tonnage.

**Two minutes:** The trade-data blocker had been described too broadly as “get 7225.11 plus 7226.11.” At HS6 that is fine for a top-level total, but a defensible U.S. customs check should say exactly which tariff/statistical lines represent GOES. Commerce's GOES investigation provides that mapping and says its Census import statistics used those same four lines. I encoded it as scope evidence rather than pretending it is a recent trade observation. The annual ingestion path can therefore validate HS6 totals against a sourced HTS10 decomposition. What remains missing is the actual annual quantity payload for 2020–2025. The physical floor is unchanged.

**Likely follow-up — why not call the trade panel solved?** Classification and observations are different. This run identifies what to query; it does not provide the requested years' quantities. Treating scope metadata as measured mass would be exactly the evidence-type error Radiant is designed to prevent.

### Run 052 — why the trade API semantics matter
**30 seconds:** Census exposes both general imports and imports for consumption. Radiant's material balance needs the latter, so I made `CON_QY1_YR` an executable ingestion contract instead of an undocumented implementation detail. I also pinned the four Commerce-sourced GOES HTS10 lines as the cross-check and removed an unsafe assumption that classification is automatically stable through time.

**Two minutes:** An official source can still be the wrong measurement if its accounting basis differs from the model. Census defines `CON_QY1_YR` as year-to-date imports for consumption and separately exposes `GEN_QY1_YR` for general imports. The GOES constraint model is about material entering U.S. consumption, so the ingestion path must use `CON_*`. I added a regression test that inspects the generated request and fails if it switches semantics, plus a test pinning the four GOES tariff lines sourced from Commerce. I did not claim this solved the missing panel—the actual 2020–2025 payload is still absent—but it prevents the eventual panel from passing merely because it is official-looking.

**Likely follow-up — why not use general imports?** General imports include goods entering U.S. customs territory, including entries into bonded warehouses/FTZ treatment that are not the same accounting concept as consumption entries. The physical-balance comparison should use a consistent consumption concept unless an ADR explicitly changes the estimand.

### Run 054 follow-up: do we have newer evidence that imported transformer components still matter?
**30 seconds:** Yes. A 2025 Cleveland-Cliffs federal-docket filing reproduces USITC DataWeb counts showing about 147.7 million imported lamination units in 2024 under two transformer-part HTS lines, with Mexico supplying about 129.9 million. January-February 2025 was 6% above the same 2024 period. I did not convert those counts to GOES tonnes because the source gives units, not weights.

**Likely follow-up — why doesn't this update the 41–44% headline?** The headline is a mass balance. A count of laminations cannot replace a mass estimate without a defensible weight distribution. The newer table confirms that the derivative channel persists, but the latest embodied-GOES tonnage remains unidentified.
