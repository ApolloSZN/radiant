# Radiant deep research plan: U.S. transformer steel (GOES)

**Owner:** Logan · **Written:** 2026-09-30 · **Put this file in the repo at `docs/RESEARCH_PLAN.md`.** It overrides older "next action" lines in run logs and `docs/GPT_BRIEF.md` until it is complete.

## The one question

How much grain-oriented electrical steel (GOES) does the U.S. need for its transformers, how much can be made domestically, and where does the rest come from? Every number must be sourced, dated and typed.

The deliverable is a **year-by-year GOES balance sheet for 2015–2025**, plus a **2026–2035 outlook**, in which every cell carries a source, a date and an evidence type. The headline finding (currently "foreign share rises from ~33% to at least 41–44%") gets rebuilt from that balance sheet, not patched.

## Why now

The Census trade pull (Run 055) exposed a contradiction. 2019 consumption 220 kt − imports 26.8 kt + exports 45.7 kt implies ~239 kt of U.S. production. That is above the ~227 kt "maximum capacity" the model treats as a hard ceiling. The headline rests on numbers that don't fit together, so we map the whole system before computing anything else.

## Rules for every phase

1. **Primary sources first:** government reports, company filings (10-K, 10-Q, annual reports, earnings-call transcripts, investor decks), official trade data, federal rulemaking dockets.
2. **Type every number:** `measured` (official statistics, audited filings), `stated` (company or agency claim), `estimate` (published estimate with a method), `model` (scenario output), `secondhand` (a paywalled report quoted by someone else).
3. **Flag interested parties.** Cleveland-Cliffs, the Core Coalition, trade associations and petitioners in trade cases all have reasons to shape numbers. Record them, labeled.
4. **Market-research numbers** (Wood Mackenzie, BNEF, CRU, consultancies) only as `secondhand` context, never in the core math.
5. **Never convert units to tonnes** (cores, laminations, transformers) without a sourced weight-per-unit or GOES-per-MVA figure. If one is used, the result is `estimate` and shows its method.
6. **Every phase ends with:** an evidence file (`data/goes/research/phase_N.yaml` or `.md`), tests for any number that enters the model, `pytest -q` green, `python -m radiant.eval --strict` exit 0, a plain-English section in `docs/FINDINGS.md`, and `logs/run_NNN.md`.
7. **No headline changes until Phase 5.** Phases 0–4 collect and reconcile. Phase 5 recomputes.

## Phase 0: Resolve the 2019 contradiction (1 session, do first)

**Question:** Which of these is wrong: 220 kt consumption, ~227 kt capacity, or the 45.7 kt export figure?
- Read the Commerce Section 232 GOES report for its exact 2019 (or nearest-year) production, consumption, import and export numbers and definitions.
- Check whether Census exports (`ALL_VAL_YR`, `QTY_1_YR`) include re-exports of foreign goods. If the API splits domestic exports from re-exports, pull domestic only.
- Find AK Steel or Cliffs statements of GOES-specific capacity or output for 2018–2021.

**Done when:** a short memo says which input is off and by how much, and the model stops calling 227 kt an upper bound if the data contradicts it.

## Phase 1: Domestic production, the biggest unknown (1–2 sessions)

**Goal:** a 2010–2025 series for U.S. GOES capacity and output, typed by evidence.
- **AK Steel 10-K and 10-Q, 2010–2019.** Electrical-steel shipments, Butler and Zanesville descriptions, capacity statements, GOES vs non-oriented mentions, export commentary.
- **Cleveland-Cliffs 10-K, 2020–2025, and earnings-call transcripts.** Every GOES, Butler, Zanesville and "electrical steel" mention: volumes, utilization, idlings, price commentary, the DOE grant, the hot-mill expansion, the stockpile contract, any GOES/non-oriented split.
- **Allegheny Technologies (ATI).** When and why it exited GOES (around 2016; verify), and the capacity removed.
- **USITC GOES investigations and five-year reviews** (2014 original; later sunset review). Public tables on U.S. capacity, production, shipments and utilization. Note what is redacted.
- **DOE grid supply-chain report (2022)** and later DOE/NREL work, for any domestic GOES capacity figures.

**Deliverable:** table with year, capacity, production, utilization, source and type. **Done when:** 2019 production is pinned to a range consistent with Phase 0.

## Phase 2: Trade, by country and by form (1–2 sessions)

**Goal:** know where foreign GOES comes from and in what form.
- **Sheet:** per-country imports and exports for the four import and two export codes, 2015–2025. Top sources and destinations each year. Re-export check.
- **Cores and laminations (HTS 8504.90.xx):** units and values by country, 2015–2025. Any official or federal-record weight data. Mexico and Canada share.
- **Finished transformers (HTS 8504.21–8504.23, 8504.33/34):** units, values, and kg where Census reports it, by country. Large power transformer counts (2019: ~617 imported).
- **Round-trip test:** do U.S. sheet exports go mainly to Mexico and Canada, where core makers then ship cores back? Report it as evidence for or against, not as a conclusion.
- **Who the core makers are:** Mexican and Canadian lamination/core and transformer plants (e.g. Prolec GE in Mexico; verify each), and which mills supply them.

**Deliverable:** per-country tables, plus an "embodied GOES" estimate range for each year, where a defensible weight method exists.

## Phase 3: Demand, bottom-up (1–2 sessions)

**Goal:** cross-check the ~288 kt top-down figure with a bottom-up build.
- **Distribution transformers:** DOE 2024 rulemaking (units shipped, core-steel tonnage, GOES vs amorphous share); NREL distribution-transformer demand study; the MTC stakeholder estimate already in the repo.
- **Power transformers:** DOE 2024 large-power-transformer report; units installed and imported; GOES per MVA (the NLR ~600 kg/MVA, 48% GOES model assumption already in the repo) times MVA additions, if MVA data exists.
- **Growth drivers:** data centers, utility capex plans, renewable and storage interconnections (generator step-up units), replacement of an aging fleet. Use published utility or agency figures; label scenarios.
- **Non-transformer GOES uses** (reactors and the like): size them or show they're small.

**Deliverable:** a bottom-up demand table compared with top-down consumption, with the gap explained.

## Phase 4: The market and the money (1 session)

**Goal:** what manufacturers and prices say about tightness.
- **Transformer makers' U.S. and North American expansions since 2022:** Hitachi Energy, Siemens Energy, GE Vernova / Prolec GE, Hyundai Electric, Hyosung HICO, Eaton, WEG, Virginia Transformer, SPX Transformer Solutions, ERMCO, and others. Plant, capacity added, GOES sourcing statements. Sources: company releases, annual reports, earnings calls.
- **Prices:** Census import unit values (already computed: $1.89/kg in 2019 to $3.22/kg in 2025), BLS producer price indexes for transformers and for electrical steel if they exist, and Cliffs commentary on GOES pricing.
- **Lead times and backlogs:** DOE, NIAC and utility filings; Wood Mackenzie only as `secondhand`.
- **Policy timeline:** AD/CVD orders on GOES (which are still in force), Section 232 steel and derivative tariffs, the DOE efficiency rule (2029), the DLA stockpile, DOE grants.

**Deliverable:** a timeline and table of capacity additions, prices and policy events.

## Phase 5: Rebuild the model and the headline (1 session)

- **Balance sheet 2015–2025:** production + sheet imports − sheet exports ± stock = sheet consumption; + embodied imports (cores, transformers) = all-forms use. Each cell sourced.
- **Identity tests in code:** production ≤ capacity; balance closes within a stated tolerance; top-down vs bottom-up demand within a stated tolerance, or the gap is explained.
- **Outlook 2026–2035:** demand scenarios from Phase 3; domestic capacity scenarios from Phase 1 (current, announced expansion, plus export diversion); foreign share as a range, with the key driver named.
- **Rewrite the headline** in README, FINDINGS, the interview walkthrough and OWNER_HANDOFF to whatever survives. One chart: foreign share 2015–2035, measured vs projected.

## Phase 6: Publishable output (after Phase 5)

A 1,500-word piece, "America's hidden transformer-steel dependence," built from the balance sheet: one chart, every number linked, plus a one-page methods note. Its numbers come straight from the code.

## Execution

- **Where:** Claude Code in the local repo, **one phase per session**, in order. Phase 0 must finish before Phase 1.
- **Prompt for each session:** "Execute Phase N of docs/RESEARCH_PLAN.md. Follow its rules. Explain each step in one line first. Finish with at most 8 plain-English lines: what you found, what's still unknown, what changed."
- **Review:** after each phase, bring the summary to Claude chat for a check before starting the next.
- **The GPT scheduled task stays paused** until Phase 5, so two agents don't edit the same files.
- **Estimated total:** 7–10 sessions.

## What would change the story

- Domestic capacity turns out well above 227 kt → foreign-share floor drops (roughly 1 point per 4 kt).
- Exports are mostly re-exports or round-trips → U.S. "net exporter" status is an illusion.
- Embodied imports grew a lot after 2020 → dependence today is higher than 33%.
- Bottom-up demand is far below 288 kt → the baseline is overstated and the whole floor shifts.
