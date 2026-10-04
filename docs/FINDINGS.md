# What Radiant found, in plain language

## Run 061 (Research plan Phase 5) — rebuilt from a full balance sheet: most U.S. transformer steel is foreign

![Foreign share of U.S. GOES use, 2015–2035](figures/goes_foreign_share.svg)

GOES reaches American transformers three ways: as sheet, inside imported cores, and inside finished imported transformers. Phases 0–4 sourced each one. Counting all three, the U.S. used about **282–376 kt of GOES in 2019, and 51–65% of it was foreign.** Counting only sheet and cores, as Commerce did, the foreign share was 36–40%. America's only mill made about 164–169 kt that year, comfortably inside its ~227 kt ceiling. It also exported 35 kt, and since 2021 most exports have gone to the Canadian and Mexican core makers.

Looking ahead, demand grows with distribution-transformer replacement and the transmission build-out. Under every scenario tested, the foreign share stays at **46% or more through 2035** (49–72% in 2035), even if Cleveland-Cliffs adds 25% at Butler and keeps every ton at home. With no change it reaches 70–84%. Building more transformer plants in the U.S. does not change this. The steel inside them still has to come from somewhere, and only one U.S. mill makes it.

What we can't claim: a shortage, prices, or timing. Only 2017 and 2019 production can be inferred, so other years use a stated model range. The core and transformer channels are estimates with methods shown in `data/goes/research/`.

## Run 053 — WITHDRAWN in Run 061. The "3–4× more imports" headline was wrong; this correction was also wrong
*Withdrawn: the 288 kt base counted the 68 kt of cores twice (the 220 kt was already all-forms use), sheet imports were not netted for re-exports, and imported finished transformers were left out. Kept below as a negative result (ADR 006).*
The old headline compared the future import floor with 2019 **sheet** imports only (27 kt). Run 040 recorded Commerce's estimate that another **68 kt of GOES arrived already built into imported transformer cores** in 2019. The national-lab grid number counts all GOES in new transformers, no matter where the cores are made, so the fair comparison counts foreign steel in every form on both sides.

Like for like: the U.S. used about **288 kt of GOES in all forms in 2019, and about 95 kt (33%) of it was foreign**. Add the grid buildout and, even if America's only producer made nothing but GOES at full capacity, foreign GOES must reach **at least 155–175 kt a year: 1.6–1.8× 2019, or 41–44% of U.S. use.** The old 87–107 kt sheet number is the same physics, but only holds if core imports stay flat; dividing it by sheet imports overstated the jump.

What we can claim: foreign dependence rises substantially and can't be closed domestically under the stated conditions. What we can't: a shortage, prices, or timing. The 68 kt figure is a Commerce estimate from industry weight data, not customs tonnage, so the most valuable next fact is any newer estimate of GOES inside imported cores.


## Run 040 — finished cores reveal a second import channel that the steel-only number misses
The Commerce Department's Section 232 transformer investigation estimated that the United States imported **68 thousand metric tons of GOES already embodied in transformer laminations and cores in 2019**. That is separate from the roughly **27 thousand metric tons of GOES imported as steel** that year, so the embedded-core estimate alone was about **2.5 times** the direct-steel import volume. Commerce explicitly warns that customs records count these core products in units rather than weight; its 68 kt figure uses weight estimates supplied in Core Coalition public comments, so Radiant records it as an estimate rather than a measured customs tonnage. Commerce also reports the Coalition's **96 kt estimate for 2020** and says first-half 2020 trade data supported the direction of the increase.

A later DOE supply-chain review gives a directly counted follow-on indicator: U.S. imports under **HTS 8504.90.9638 (stacked cores for incorporation into transformer parts) reached 842,929 units through October 2021**, up from 50,267 units in 2016. Radiant does **not** convert those units into tonnes because no defensible core-weight distribution is supplied. Together, the sources show that steel-form trade materially understates foreign GOES dependence because GOES also crosses the border inside fabricated cores. The **87–107 kt/year future import-or-stock-draw floor is unchanged**: these historical derivative imports describe the existing supply channel; they are not an additional demand term or a new domestic-supply measurement. No shortage is claimed.

Primary sources: U.S. Department of Commerce, Bureau of Industry and Security, *The Effect of Imports of Transformers and Transformer Components on the National Security* (completed 2020-10-15; published 2021), section VII.5; U.S. Department of Energy, *Electric Grid Supply Chain Review: Large Power Transformers and High Voltage Direct Current Systems* (2022-02-24).


## Run 039 — no new finding; one bug that would have broken the first GitHub run was fixed
The last eight runs improved release checks but found nothing new about the world. The main finding stands: the grid buildout needs at least 87–107 thousand tonnes a year of imported transformer steel (3–4× 2019). The next real progress requires putting the project on GitHub so the trade-data job can run.


## Run 030 — newer producer data does not justify pretending we know GOES output
Cleveland-Cliffs' FY2025 Form 10-K reports **575 thousand net tons of combined stainless and electrical-steel shipments**. That is a useful measured company output, but the filing does not split stainless, non-oriented electrical steel, and GOES. Radiant therefore records it as context and **does not substitute it for GOES production or capacity**. This is exactly the kind of aggregate number that can create a false precision if relabeled.

DOE's April 2024 final distribution-transformer rule also materially changed the demand-side interpretation: DOE says roughly **75% of the market can meet the final standard using GOES**, versus an initial proposal that likely would have shifted about **95% of the market to amorphous alloy**. On June 15, 2026 DOE opened a new RFI about national-security, domestic-capacity and supply-chain impacts, but stated the 2024 standards are still scheduled for compliance on **April 23, 2029**. An RFI is not a rescission. These facts strengthen the case for keeping GOES in the demand model, but neither supplies a defensible tonnage conversion, so the **87–107 kt/year conditional import floor is unchanged**.

The annual Census pull was retried in this environment and failed at DNS/network access before any response was returned. No trade quantities were inferred or fabricated. The GitHub workflow remains the executable acquisition path.

## Run 029 — the military is also stockpiling this steel
The Defense Department announced on July 1, 2026 that it is buying up to 53,000 short tons of this steel from the same single U.S. producer over five years, to stockpile. That's up to about 9,600 tonnes a year that can't go into grid transformers. If the full amount is drawn, the minimum import need rises from 87–107 to about **97–117 thousand tonnes a year**. The main finding doesn't depend on this; it only makes the gap bigger.

We also built the pipeline for real annual trade data (2019 onward). It runs automatically on GitHub and plugs recent import levels into the finding when it arrives.


## Run 028 — the grid needs 3–4× more imported transformer steel

### What we tested
Can America's only maker of transformer steel (grain-oriented electrical steel, GOES) cover what the grid buildout needs?

### What we found
Cleveland-Cliffs says it can make up to about 227 thousand tonnes a year of *all* electrical steel. GOES is only part of that, so this is the most it could possibly make. The U.S. used about 220 thousand tonnes of GOES in 2019. A 2026 national-lab model says grid expansion adds 94–114 thousand tonnes a year.

Add those up and, even if the factory made nothing but GOES at full speed, the country needs at least **87–107 thousand tonnes a year from imports: about 3–4 times what it imported in 2019.** The only way that floor disappears is if everyday (non-grid) demand for this steel drops by 40–49%.

Cliffs announced a hot-mill expansion described as "25% growth," due by 2028. We did not turn that into a GOES number because they didn't state one. Even if every bit of it became GOES, imports would still need to exceed 2019 levels.

### What changed from before
Before: "big pressure, adequacy unknown." Now: domestic supply alone is identified as insufficient, with a specific minimum import requirement.

### What we can claim / cannot claim
We can claim the import floor under the stated conditions. We cannot claim there will be a shortage (imports might supply it), anything about prices or tariffs, or when the demand arrives.

### Why it matters
Utilities, transformer makers, grid planners and policymakers are betting on a buildout that depends on imports of a steel the U.S. also restricts with tariffs. This puts a number on that dependence.

## Run 028 — the release rule was fixed
Run 027 made the project fail its checks unless it won a forecasting contest. The evidence says it can't win, and forecasting isn't the goal. Now a failed result is **withdrawn**: it is published as a failure and never claimed. Nothing claimed has failed, so the checks pass honestly.


## Run 027 — the release gate was lying, so it is red now

### What was broken

Run 026 proved that Radiant's sequencing forecaster did **not** beat the strongest simple recent-window baselines. The documentation said that clearly, but the executable release harness still gave the forecasting row a pass because it compared the selector with the weak all-history trend line.

That meant the repo could say "the headline does not survive a fair baseline" while CI still treated the old headline as good enough. That contradiction is now fixed.

### What changed

The sequencing release gate now uses the full predeclared baseline panel. The system has to robustly beat all of those simple baselines, not just the easiest one.

On the same 39 paired sequencing forecasts:

- strongest fixed simple baseline: **rolling-3**, MALE **0.1493**
- original Radiant selector: MALE **0.1762**
- Radiant selector vs rolling-3: **18.0% worse**

So the scientific eval gate is now correctly **FAILED**.

The old 77.5% improvement versus all-history is still recorded because it really happened, but it is now a diagnostic, not release evidence.

### We also tried two standard online learners

To test whether the problem was just Radiant's particular selector, Run 027 added two causal online aggregation methods. Neither can see the current target before forecasting.

- **Follow-the-leader:** MALE **0.1561**. Better than the old Radiant selector, but still **4.6% worse** than rolling-3. Its paired-bootstrap interval against rolling-3 crosses zero.
- **Exponential weights:** MALE **0.1641**. Better than the old selector, but **9.9% worse** than rolling-3. Its paired-bootstrap interval also crosses zero.

So a generic adaptive meta-learner does not rescue the forecasting claim. The honest result is stronger now: **this sequencing dataset has not demonstrated that adaptive model selection adds value beyond a very simple recent-window trend.**

That is a negative result, and it stays in the repo.

## Run 027 — GOES trade coverage was too coarse

The previous GOES supply-panel code correctly knew that grain-oriented electrical steel spans two six-digit headings: 7225.11 and 7226.11. But that is not enough to query current U.S. import data safely.

Commerce's current SIMA product list splits the narrow-width import heading into three separate ten-digit HTSUSA codes. Current import coverage is therefore:

- `7225110000`
- `7226111000`
- `7226119030`
- `7226119060`

The current export concordance is different and coarser:

- `7225110000`
- `7226110000`

Radiant now stores those as **direction-specific, effective-period code sets** instead of pretending one timeless list works for imports, exports and historical years. The aggregator fails if a period is missing one required code rather than treating an omitted code as zero.

This matters because an incomplete commodity query can produce a clean-looking but systematically understated GOES import series.

It still does **not** mean the GOES supply panel is complete. We have corrected the acquisition contract; we have not yet ingested the full annual historical quantities.

## Earlier findings that still stand

### 1. Idle U.S. transformer factories could not have ended imports

In 2019 the U.S. made about 137 large power transformers, imported about 617 and exported about 4. Reported factory utilization was about 40%, implying about 342 units/year of domestic nameplate capacity. Even at full utilization, maintaining 2019 apparent consumption would still have required roughly 410 imported units per year.

This identifies a capacity arithmetic fact. It does not identify why utilization was low.

### 2. Grid expansion creates major GOES pressure, but a shortage is not identified

A 2026 DOE-funded national-lab model implies transmission expansion may require about 94–114 thousand tonnes of GOES per year, more than 45% of recent U.S. apparent consumption. Radiant records that as major supply pressure, not a shortage forecast.

A shortage claim still requires compatible evidence for domestic production/capacity, imports, exports, inventories or stock changes, and competing uses.

### 3. Other negative results are retained

- Battery-price selector: nominally 11.4% better on only six paired forecasts; not robust enough for a general claim.
- Strict historical BLS revision test: the correction model is 31.6% worse than doing nothing. The useful result is that the replay machinery respects what was knowable at each historical cutoff.

## What this adds up to now

Radiant's strongest feature is not a forecasting edge. It is that the architecture can expose when a claim depended on a weak baseline, when a trade series is incomplete, when a supply-chain parameter is unidentified, and when a historical backtest is using information that was not available at the time.

The v1.0 gate is now harder and more honest. The next valid path is **not** to tune another sequencing selector on the same 39 outcomes until it wins. The next predictive evaluation should freeze the algorithm and test it on genuinely held-out or historical-vintage technology series. In parallel, the GOES case can continue with the corrected commodity-code acquisition contract.


## Run 031 — a green data job now means the steel data actually arrived

### What was broken
The annual GOES downloader was designed to keep going when one Census request failed. That is useful for diagnostics, but it also returned success after writing `error:` rows. On GitHub, that could have made the monthly data workflow look green and even commit a CSV that Radiant could not use.

### What changed
Required six-digit GOES totals are now fail-closed. If either required heading fails for imports or exports in any requested year, the downloader still writes the diagnostic CSV but exits with an error. The GitHub job also runs the GOES parser and focused tests before it is allowed to commit data. Ten-digit rows remain a cross-check rather than a hard requirement because the detailed tariff codes can change across years.

### What we verified
The field names in the downloader match the current Census International Trade API documentation: imports-for-consumption use year-to-date quantity `CON_QY1_YR` and value `CON_VAL_YR`; exports use `QTY_1_YR` and `ALL_VAL_YR`; `COMM_LVL` supports HS6 and HS10. This removes the earlier uncertainty about whether the script was asking Census for invented fields.

### What this does not prove
It does not add annual trade observations. This runtime still cannot complete the Census requests. The import-floor finding therefore stays at **87–107 kt/year conditional minimum imports or stock drawdown**, with no shortage claim. The value of this run is reliability: the next hosted data run cannot silently convert retrieval failure into apparent evidence.

## Run 032 — the release gate now proves an actual baseline improvement

### What was wrong
The written v1.0 ship bar required a measured improvement over an explicit baseline, enforced in CI. The executable release verifier did not actually require that. It only required a passing strict historical-vintage row. That meant the BLS replay could satisfy the release evidence gate even though its predictive correction was worse than doing nothing. The documentation was stricter than the code.

### What changed
Radiant now has an explicit information-integrity benchmark. At each of the nine archived BLS preliminary-release cutoffs, a naive latest-revision reconstruction uses a value that was only published later: **9/9 future-information violations**. The bitemporal as-of representation uses the preliminary value available at the cutoff: **0/9 violations**, a **100% reduction**. This is a measured improvement over an explicit baseline, but it is deliberately labeled as information integrity rather than predictive accuracy.

The release verifier now requires at least one passing `claimed` evaluation row with positive measured improvement. A merely passing integrity row or a withdrawn result cannot satisfy that gate. The failed sequencing forecasting claim remains withdrawn, and the BLS correction model remains a negative predictive result.

### Why it matters
This closes a governance gap between Radiant's stated ship bar and its executable gate. The project now has a real CI-enforced positive result: the bitemporal evidence system eliminates demonstrated future-information leakage on the archived BLS panel. It still does **not** have evidence of superior forecasting accuracy, and no such claim is made.


## Run 033 — hosted CI evidence must belong to the exact release candidate

### What was wrong
The final release verifier checked that the hosted-CI attestation and completed-run record looked valid, but it did not compare their commit SHA with the candidate being released. In principle, an old successful GitHub run could therefore be copied into a newer checkout and clear the final hosted gates.

### What changed
Final verification now binds both hosted records to the checked-out Git commit. It also requires the attestation and completed-run record to describe the same repository, commit, run ID, and run URL. A ZIP without Git commit identity cannot claim final hosted verification, and evidence from two different runs cannot be mixed.

### What this proves — and does not prove
It proves the release machinery is stricter about provenance: when Radiant eventually reports 11/11, the hosted success must belong to the exact candidate being released. It does not add a scientific result or clear the hosted gates today. Radiant remains 9/11 until rc21 itself runs successfully on GitHub.


## Run 034 — executable ship-bar evidence, not file-presence proxies

The release verifier still had a meaningful weakness after Run 033. Three local gates could pass from file presence rather than evidence that the relevant behavior had actually executed: the reproduction gate checked only that `scripts/reproduce.sh` and the Dockerfile existed; the demo gate checked only that `examples/demo.py` existed; and outside `--run`, the tests gate accepted any `test_report.json` file without checking its return code. GitHub CI also did not execute the demo.

Run 034 fixes that. The single reproduction command now runs the full test suite, strict evaluation, and the demo; it writes typed test, demo, and reproduction reports only after those stages succeed. GitHub CI calls this exact reproduction command before creating its hosted attestation. The final release verifier requires a passing `radiant.reproduction.v1` report, a passing `radiant.demo.v1` report, and a test report with return code zero. A deliberately failed/stale execution-artifact fixture is rejected by regression test.

This does not change any scientific claim. The positive measured result remains the narrow bitemporal information-integrity result (9/9 future-information violations for the latest-revision baseline versus 0/9 for as-of replay). The forecasting advantage remains withdrawn, and GOES remains a conditional import-floor result rather than a shortage claim. The practical change is that three v1.0 gates now require executable receipts instead of merely plausible files.


## Run 035 — execution receipts are now bound to the source they tested
Run 034 made tests, demo, and reproduction executable, but its JSON receipts were still reusable after a later source edit. Run 035 closes that gap. Radiant now fingerprints the executable/scientific input tree and writes that fingerprint into each execution receipt. The release verifier recomputes it. If code, data, workflow, tests, scripts, Docker configuration, or ontology changes after the run, the old receipts no longer clear the gates. An adversarial regression test mutates source after creating passing receipts and confirms that tests, demo, and reproduction all fail closed. This changes no scientific result; it strengthens reproducibility provenance.


## Run 036 — hosted CI no longer destroys its own final evidence
The hosted workflow had a subtle self-invalidating path. `scripts/reproduce.sh` created a valid source-bound v2 test receipt, but the later release verifier's `--run` option reran pytest and overwrote that file with an older untyped JSON shape. CI could still report success because the gate state was calculated before the overwrite, but the evidence artifact downloaded afterward could never pass the final verifier. Run 036 fixes the writer so `--run` preserves the v2 schema and source fingerprint. A regression test executes that exact path and checks the persisted receipt. This changes no scientific result; it removes a blocker that would otherwise have made 11/11 impossible even after a genuinely green hosted run.


## Run 037 — successful hosted CI now finalizes itself
The remaining hosted release process still required a human to query GitHub after CI, download the evidence, and write the completed-run receipt. That was not a scientific weakness, but it was an avoidable reproducibility and handoff gap. Run 037 adds a second GitHub Actions workflow triggered by completion of the named `ci` workflow. It only runs when the upstream conclusion is `success`, checks out the exact upstream SHA, downloads the artifact from the exact upstream run ID, constructs the completed-run receipt from GitHub's workflow-run identity, and then invokes the same fail-closed final verifier. A helper validates the canonical repository/run URL, 40-hex SHA, numeric run ID, and completed/success state. Negative tests show failed, in-progress, malformed, and mismatched records cannot be converted into success evidence. This changes no scientific result; it turns the last manual evidence-transfer step into executable infrastructure.

## Run 038 — the clean-machine claim is now tested, not inferred
The v1.0 ship bar says a stranger must be able to reproduce Radiant from a clean machine/container with one command. The prior executable gate proved that the host-side reproduction script had run and that a Dockerfile existed, but it did not prove the Docker image itself built or that Radiant passed inside it. That was a real gap between the written claim and executable evidence. Run 038 adds a fail-closed container wrapper that builds the image and executes the full reproduction inside it. Only after Docker exits successfully does it create a source-bound container-reproduction receipt. Hosted CI now runs this path and uploads the receipt. The release verifier requires it. This runtime has no Docker binary, so the receipt was deliberately not simulated; locally the stricter release count falls from 9/11 to 8/11 until hosted CI performs the clean build. No scientific result changed.

## Run 041 — foreign GOES supply is expanding in India while a European site was curtailed

Two producer-primary facts add supply-side context without pretending to quantify U.S. availability. JFE Steel announced on February 13, 2024 that its 50:50 JSW joint venture in Bellary, India is dedicated to conventional and high-permeability GOES, with **$670 million** planned investment and full operation targeted for fiscal 2027. The release does not state tonnes of capacity, so Radiant records the investment and schedule but does not turn them into supply tonnage.

On March 26, 2026, thyssenkrupp Electrical Steel said its Isbergues, France GOES site had been running at **50% of total capacity since January 2026** and would be fully shut from June through September 2026. That is a producer statement about utilization, not audited output, and it does not identify U.S.-available supply.

Together these facts show why “foreign capacity” cannot be represented as one static number: new GOES production is being built while existing European production can be curtailed. Neither fact changes Radiant's **87–107 kt/year conditional U.S. import-or-stock-draw floor**, and neither establishes a shortage.

## Run 042 — a quantified foreign GOES expansion, without pretending it is U.S. supply

JFE Steel's August 4, 2025 expansion announcement supplies the tonnage that its earlier JV announcement did not. JFE and JSW plan **350,000 tonnes/year of GOES capacity in India by 2030**: 100,000 tpy at Vijayanagar and 250,000 tpy at Nashik. Nashik's stated current capacity is 50,000 tpy. Vijayanagar is planned for full production by 2027; Nashik expansion is phased from 2028 through 2030.

This is useful supply-side evidence, but it does **not** reduce Radiant's U.S. import floor. It is announced future nameplate capacity aimed at Indian demand, not observed output or tonnes demonstrably available for export to the United States. The U.S. conditional floor therefore remains **87–107 kt/year of imports or stock drawdown**, and Radiant still does not claim a shortage. The most important missing observation remains annual U.S. direct GOES imports for 2020–2025 with explicit HTS coverage.

## Run 043 — current GOES tariff status is now explicit evidence

The current U.S. tariff schedule and 2026 Section 232 proclamations resolve another supply-context ambiguity. The HTSUS lists the ordinary Column 1 general rate for GOES under 7225.11 and 7226.11 as **Free**, but that is not the total border charge. Proclamation 11021 imposed a **50% additional Section 232 duty on the full customs value of steel articles** effective April 6, 2026, and Proclamation 11032's Annex I-A explicitly includes headings 7225 and 7226 in the 50% steel-article list.

Radiant records the base rate and additional Section 232 rate separately. It does not infer how much imports fall, prices rise, sourcing changes, or domestic output responds. Those would require measured post-policy observations or an identified elasticity. The **87–107 kt/year conditional import-or-stock-draw floor is unchanged**, and no shortage claim is made.


## Run 044 — North American transformer-component routing exposes another embodied-GOES channel

Commerce's Section 232 transformer investigation reports that **more than 99% of Mexico's transformer-component exports** and **more than 90% of Canada's** went to the United States. The same report says neither country had domestic GOES production capability, so their increased lamination/core production required imported GOES. This strengthens the evidence that direct U.S. GOES-sheet customs tonnage is an incomplete measure of U.S. foreign-GOES dependence: material can be imported first by Canada or Mexico and then enter the United States embodied in transformer components.

Radiant stores the Canadian 90% figure only as a published lower bound and keeps Mexico's >99% statement in the scope note. It does not convert either share into GOES tonnes, because the report does not provide the required component-weight/GOES-content distribution. The **87–107 kt/year conditional import-or-stock-draw floor is unchanged**, and no shortage is claimed. The binding empirical gap remains official annual U.S. direct GOES import tonnes for 2020–2025 with explicit HTS coverage.

## Run 045 — official 2020 direct-GOES trade value identifies source concentration, not mass

DOE's Electric Grid Supply Chain report records **$29 million of U.S. GOES imports in 2020 under HS 722511** and reports that **85% of import value came from South Korea, 6% from Brazil, and 4% from Russia**, citing USA Trade Online. This is a useful measured observation because it identifies how concentrated the direct-GOES import channel was in 2020. It is not the missing mass series: the published figure is dollars, covers HS 722511 rather than the complete 7225.11 + 7226.11 scope, and supplies no evidenced unit price with which to convert value into tonnes. Radiant therefore stores the value and source shares as context only. The conditional **87–107 kt/year** import-or-stock-draw floor is unchanged and no shortage is claimed.

## Run 046 — the EU now prices GOES dependence inside finished transformers

A current official trade-policy fact adds another reason not to model GOES as a sheet-only market. The Czech Ministry of Industry and Trade's summary of Commission Implementing Regulation (EU) 2026/2133 states that the EU provisional safeguard applies from 25 September 2026 through 26 February 2027 and reaches transformer cores even when they enter already incorporated in finished transformers. Those incorporated cores are not quota-managed; instead they face a specific duty of **EUR 1,140 per tonne of core**. The underlying measure also covers GOES and standalone laminations/cores.

This is useful supply-chain evidence, but it is not a U.S. quantity observation. Radiant therefore records the EUR 1,140/t duty as foreign policy context only. It does not assume that the measure diverts any tonnes to the United States, changes global production, or changes the U.S. **87–107 kt/year** conditional import-or-stock-draw floor. The missing 2020–2025 U.S. direct-GOES mass panel remains the binding empirical gap.


## Run 047 — global GOES capacity is concentrated, and scenario demand can outrun today's nameplate

IEA Energy Technology Perspectives 2023 reports about **3.8 million tonnes/year of global GOES production capacity**, with China, Japan, Korea, Russia, and the United States accounting for **almost 85%**. In the IEA Net Zero Emissions scenario, GOES demand doubles to **6 Mt/year over 2022–2030**. This is useful system-level context because it puts the U.S. 87–107 kt/year conditional import requirement against a concentrated global production base.

Radiant keeps the two numbers differently typed: 3.8 Mt/year is reported global capacity context; 6 Mt/year is an IEA scenario trajectory, not observed demand. Neither is treated as U.S.-available supply, and neither establishes a shortage. The U.S. import-floor calculation is unchanged. The binding empirical gap remains the official 2020–2025 U.S. direct-GOES mass panel with explicit HTS coverage.

## Run 048 — a foreign GOES producer documents an actual U.S. data-center-transformer supply route

JFE Steel announced on June 20, 2024 that its grain-oriented JGreeX steel had been selected by a U.S. manufacturer of IT data-center transformers. JFE describes this as the **first JGreeX application in the United States** and says the order would be delivered to **Eaton Corporation through Toyota Tsusho**. This is stronger than treating foreign nameplate capacity as implicitly available to U.S. buyers: it documents an actual producer-to-U.S.-transformer supply route.

The release does **not** state order mass, price, or recurring annual volume. Radiant therefore records one documented order/application as routing evidence and refuses to turn it into tonnes. It cannot be subtracted from the **87–107 kt/year conditional import-or-stock-draw floor**, and it does not establish that foreign supply is sufficient or that a shortage exists. The official 2020–2025 direct-GOES mass panel remains the binding measurement gap.

## Run 049 — official product scope separates direct GOES from embodied cores

U.S. Commerce's March 27, 2026 notice on the EU GOES safeguard identifies the covered tariff headings explicitly: **7225.11.00 and 7226.11.00 for GOES**, and **8504.90.13 for steel laminations and cores**. This is not the missing U.S. tonnage panel, but it resolves an important measurement-design issue with an official source: direct GOES steel and embodied transformer-core trade are distinct customs channels and should not be silently pooled.

Radiant now records that mapping as typed scope evidence. It does not turn the three headings into a quantity, and it does not change the **87–107 kt/year conditional import-or-stock-draw floor**. The attempted Commerce SIMA workbook retrieval still failed in this runtime even though Commerce's static-table page confirms the non-license workbook incorporates Census and license data. The binding empirical gap therefore remains annual 2020–2025 U.S. direct-GOES tonnes with verified U.S. HTS descendants.

## Run 050 — DOE quantifies the distribution-transformer core-steel demand scale
DOE's April 2024 final distribution-transformer rule estimates **225,000 metric tons/year** of current U.S. electrical-steel demand for distribution transformers. In the same rulemaking, DOE records an MTC stakeholder estimate of approximately **175,000 metric tons/year of GOES consumption for distribution transformers**. These are not equivalent evidence: 225 kt is DOE's all-core-electrical-steel demand estimate, while 175 kt is a stakeholder GOES estimate preserved in the federal record.

Radiant keeps both outside the 87–107 kt/year import-floor equation. The 225 kt figure includes non-GOES core material and would double-count demand if added to the existing baseline; the 175 kt figure is not a measured customs series and covers distribution transformers rather than total GOES use. The result therefore does **not** change the conditional floor or establish a shortage. It does materially ground the scale of one major downstream demand channel and gives a new cross-check for the still-missing 2020–2025 direct-import mass panel.

## Run 051 — official U.S. GOES HTS10 coverage resolved
The missing recent mass panel had two separate uncertainties: the quantity payload itself and the exact U.S. statistical lines that should be summed. Commerce's GOES investigation resolves the second. It identifies GOES under **7225.11.0000, 7226.11.1000, 7226.11.9030, and 7226.11.9060**, and its historical import table says Census data were queried using those four lines.

Radiant now stores that mapping as federal product-scope evidence and regression-tests it. This is useful because the annual ingestion code's HS10 cross-check already expects exactly these lines; the code was previously plausible but insufficiently sourced. It still does **not** create the missing 2020–2025 quantities, and the written Commerce product description is dispositive rather than the codes themselves. The 87–107 kt/year conditional import-or-stock-draw floor is unchanged and no shortage is claimed.

The first test run after editing failed at Python collection because an apostrophe in the new evidence string was not escaped. That implementation failure was fixed without changing the evidence or test condition. Final verification is 144/144 tests passing; strict evaluation exits 0. The forecasting-superiority claim remains withdrawn.

## Run 052 — trade-ingestion semantics hardened before accepting the missing panel
The remaining GOES blocker is not just “get a number”; the number has to answer the same physical question as the material balance. Census documents separate **imports for consumption** (`CON_QY1_YR`) from **general imports** (`GEN_QY1_YR`). Radiant's downloader already requested the consumption series, but that choice was implicit and untested. Run 052 makes it an executable contract and ties the HTS10 cross-check to the four-line Commerce scope established in Run 051.

This matters because a future contributor could otherwise substitute a plausible official quantity with different accounting semantics and still make the pipeline appear complete. A new regression test now fails if the importer silently changes from `CON_QY1_YR`/`CON_VAL_YR` to general-import fields, or if the four-code GOES cross-check drifts. The downloader documentation also removes the overbroad claim that the HS classification is automatically stable across all years; historical continuity must be checked rather than assumed.

No 2020–2025 quantity payload was recovered in this runtime, so the conditional **87.203815–107.203815 kt/year** floor is unchanged and no shortage is claimed. This run improves falsifiability/reproducibility rather than adding a new tonnage observation.

## Run 054 — the derivative channel is still large in 2024–2025, but the newer customs table is in units, not tonnes

A June 2025 Cleveland-Cliffs submission in Commerce docket BIS-2025-0023 includes a USITC DataWeb table for U.S. imports of laminations for incorporation into stacked transformer cores under HTS 8504.90.9534 and 8504.90.9634. It reports **147,652,598 units in 2024**, down 17% from 177,844,193 in 2023; Mexico supplied 129,877,076 of the 2024 units. For January-February 2025, the table reports **25,059,726 units**, 6% above the same period of 2024.

This is useful recent evidence that the embodied-GOES derivative channel remained quantitatively large after the 2019/2020 Commerce estimates. It does **not** update the 68 kt (2019) or 96 kt (2020 estimate) embodied-GOES mass values: these newer tariff lines report pieces/units, and there is no defensible weight-per-unit distribution in the source. Radiant therefore records the counts but refuses to turn them into tonnes or annualize the two-month 2025 observation. The Run 053 headline remains unchanged: about 33% foreign in 2019, rising to a conditional floor of 41–44% under the modeled grid increment. No shortage is claimed.

## Run 055 — measured U.S. GOES trade, 2019–2025: direct imports are flat-to-down, and the U.S. is a net exporter

The Census International Trade API (imports for consumption; four-code HTS10 GOES scope) now supplies annual tonnage. Census reports no quantity at the HS6 level, so tonnes come from HTS10 kilograms; in every year the HTS10 lines add up to exactly 100% of the HS6 dollar value, so nothing is missing.

| Year | Imports (kt) | Exports (kt) | Net imports (kt) |
|---|---|---|---|
| 2019 | 26.8 | 45.7 | −18.9 |
| 2020 | 26.2 | 30.6 | −4.4 |
| 2021 | 41.8 | 47.7 | −5.8 |
| 2022 | 20.0 | 71.9 | −51.9 |
| 2023 | 31.4 | 45.8 | −14.4 |
| 2024 | 35.2 | 37.5 | −2.3 |
| 2025 | 19.8 | 43.8 | −24.0 |

Census's 2019 import figure (26.8 kt) matches the Commerce anchor already used in the model (27 kt) to within 1%, which confirms the 2019 baseline. Direct GOES sheet imports did **not** rise after 2019: they peaked at 41.8 kt in 2021 and were 19.8 kt in 2025, 26% below 2019. Import prices did rise, from about $1.89/kg to $3.22/kg, so import dollars went up while tonnes went down.

This does **not** change the 41–44% all-forms finding. That number is a forward-looking floor: how much foreign GOES the U.S. would need if grid demand grows and the domestic producer is capped. The trade data shows the direct-sheet channel is not moving toward it. 2025 direct imports are about one-fifth of the 87–107 kt sheet floor (4.4–5.4×). Any foreign supply that does arrive must therefore come mostly as cores, laminations and finished transformers, which this dataset does not weigh. No shortage is claimed.

## Run 056 (Research plan Phase 0) — the 220 kt "consumption" already includes imported cores

The Run 055 trade data exposed a contradiction: 220 kt of 2019 use, minus imports, plus exports, implied ~239 kt of U.S. production, more than the ~227 kt capacity in the model. Phase 0 traced each input to its source.

The 220 kt is not a Commerce measurement. Commerce's 2021 report repeats it as an estimate "per year" and footnotes it to the Core Coalition, a group of core importers. Commerce's own percentages pin down what it means. Sheet imports were "less than 20 percent" of 2019 consumption, all-forms imports (sheet plus GOES inside cores) were "approximately 44 percent", and 2020 was projected "over 50 percent". Only one picture satisfies all three: about **148 kt of sheet consumption** and about **216 kt of total GOES use**, which is the 220 kt. The model's 288 kt adds the 68 kt of cores a second time.

With the corrected inputs, implied 2019 U.S. production is **164–169 kt**, inside the ~227 kt electrical-steel capacity. A 2017 check using Commerce's 37% figure gives ~162 kt. U.S. "exports" also include re-exports of foreign steel: 10.9 of 45.7 kt in 2019, so foreign sheet that actually stayed in the U.S. was ~17 kt.

The headline is not changed yet (the plan reserves that for Phase 5). Commerce's own 2019 foreign share for all forms was ~44%, not the 33% Radiant reports. Phase 5 will rebuild the floor on the corrected base. Details: `data/goes/research/phase_0.md`.

## Run 057 (Research plan Phase 1) — U.S. GOES output is never published; it can only be inferred

Cleveland-Cliffs, the only U.S. producer, reports GOES inside a "stainless and electrical" line and never on its own. In 2014 its predecessor AK Steel told the USITC its GOES capacity was about 285,000 short tons (~258 kt). In 2020 Cliffs described "up to 250,000 net tons" of all electrical steel (~227 kt). The only production figures available are inferred from trade data and Commerce's percentages: about **162 kt in 2017** and **164–169 kt in 2019**, roughly 72–74% of the 227 kt ceiling. ATI left GOES in 2016. A 70 kt non-oriented line opened in 2023 at the plant that finishes GOES. Cliffs says a Butler upgrade will add about 25% to GOES output by 2028, from an undisclosed base.

This run also corrects a repo error. Cliffs' FY2025 stainless+electrical shipments were **552** thousand net tons, not 575. "575" was a dollar figure in the same 10-K. The headline is unchanged (Phase 5). Details: `data/goes/research/phase_1.md`.

## Run 058 (Research plan Phase 2) — U.S. GOES now goes to Canada and Mexico and comes back inside cores

GOES sheet imports still come from Japan and Korea. The change is on the export side. Before 2020, most U.S.-made GOES exports went to Belgium and India. Since 2021, **79–90% have gone to Canada and Mexico**, where North America's core makers are; Canada alone took 22–42 kt a year. Commerce's 2021 report assumed little U.S. steel came back inside imported cores because Canada wasn't a big buyer. That stopped being true after 2020, so part of America's "net exporter" status is a round trip.

GOES embodied in imports grew. Cores have no weight data, but Canada/Mexico core-part imports rose from $502M (2019) to $1.38B (2025). Deflated by the GOES price, that implies about 109 kt of GOES in 2025, up from Commerce's 68 kt (an estimate with a stated method). Finished-transformer imports quadrupled in dollars, to $9.3B, while prices rose 76%. The GOES inside imported large power transformers alone was at least 18 kt in 2019 and at least 43 kt in 2025. Comtrade's transformer "tonnes" were calculated from value, so Radiant does not use them. Headline unchanged until Phase 5. Details: `data/goes/research/phase_2.md`.

## Run 059 (Research plan Phase 3) — counting imported transformers, U.S. GOES use was ~280–375 kt in 2019

A bottom-up build by transformer type confirms the corrected base, and it also exposes what the old one missed. Distribution transformers use about 175–218 kt of GOES a year (DOE's 2024 rule and an industry comment). Large power transformers weigh 150–400 tons each, with 40–48% of that GOES, so the 750 bought in 2019 held 45–144 kt. Adding the GOES inside **imported finished transformers** to sheet and cores gives **281–375 kt** of total U.S. use in 2019. The bottom-up sum of known classes is 220–362 kt. The two ranges overlap.

The 216 kt "all forms" figure (Commerce, and Radiant after Phase 0) still leaves out imported transformers: about 37–118 kt in LPTs and 31–39 kt in distribution transformers in 2019. That is as large as the 68 kt in imported cores. The domestic side closes: U.S. transformer plants needed about 152–206 kt for the DTs and LPTs they built, inside the 213–218 kt of sheet and imported cores they had. Headline unchanged until Phase 5. Details: `data/goes/research/phase_3.md`.

## Run 060 (Research plan Phase 4) — prices doubled, lead times tripled, and the plan's AD/CVD premise was wrong

The money tells the same story as the tonnes. The price of imported GOES roughly doubled between 2019 and 2023 ($1.94 to $4.04/kg) and was still about 70% higher in 2025. The BLS transformer price index rose 76% over 2019–2025. Lead times went from about a year in 2021 to about 2–3 years in 2024, and LPTs were quoted at up to five years. Distribution-transformer waits eased to about 30 weeks by mid-2025. Eleven transformer-plant expansions since 2022 disclose about $1.46 billion of investment, mostly in power transformers. None says where its GOES will come from, and most of the companies are foreign-owned.

One correction to the research plan: no anti-dumping or countervailing duty orders on GOES are in force. The 1994 orders were revoked in 2006, and the 2014 cases all failed at the USITC. GOES, and since August 2025 cores and laminations, face the Section 232 steel tariff, now 50%. Mexico is exempt from any transformer action under a 2020 monitoring deal. Details: `data/goes/research/phase_4.md`.

## Run 062 (Research plan Phase 6) — the publishable piece

`docs/article/americas-hidden-transformer-steel-dependence.md` (about 1,570 words, one chart, every number linked to a source) and `docs/article/methods.md` (one page) tell the Phase 5 result for a general reader. The text is rendered from templates by `scripts/build_goes_article.py`, so every figure comes straight from `goes_balance`. A test fails if the article falls out of date with the code. No new numbers were introduced in this run.


## Run 063 — release-status synchronization

Radiant v1.0 remains frozen at exact release SHA `2044ca5f8a235889a27733f58b3c0cdf5c11a7c8`. The maintenance work in this run changes documentation only: it synchronizes repository-facing status with the hosted release evidence already produced for that exact SHA. It does not change models, datasets, baselines, tests, or scientific claims.

The positive evaluation remains **bitemporal information integrity**, not predictive superiority: replaying historical BLS observations with latest revisions leaks future information at **9/9** tested cutoffs, while the as-of replay produces **0/9** leakage violations. The earlier forecasting-advantage claim remains withdrawn. GOES results also remain bounded as previously documented; this run adds no new shortage claim or effect size.

The maintenance head passed hosted CI, including the normal reproduction path, clean-container reproduction, CI attestation, and release verification. What can be claimed is therefore narrow: the status-document correction does not regress the shipped executable system. What cannot be claimed is any new scientific capability or forecast improvement.

The binding next program action is Phase-2 candidate approval. Until that approval exists, Radiant should remain frozen except for regression repair and release-documentation maintenance.
