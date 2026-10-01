# Phase 0 memo — the 2019 contradiction

**Question.** 220 kt consumption − 26.8 kt imports + 45.7 kt exports implies ~239 kt of 2019 U.S. GOES production, above the ~227 kt "capacity" the model treats as a ceiling. Which input is wrong?

**Answer.** The 220 kt. It is not 2019 *sheet* consumption. It is the Core Coalition's estimate of total U.S. GOES use ("per year"), which Commerce repeated with a footnote to the Coalition. Commerce's own percentages put 2019 **sheet** consumption at **145–150 kt** and **all-forms** use (sheet + GOES inside imported cores) at **213–218 kt**, which is the 220 kt figure. The model's 288 kt (220 + 68) counts the 68 kt of cores twice. That overstates all-forms use by about **72 kt**.

## Evidence

| Fact | Value | Type | Interested party | Source |
|---|---|---|---|---|
| "U.S. consumption of GOES is estimated at approximately 220,000 metric tons per year" | 220 kt | secondhand | Core Coalition (fn 64) | FR 2021-24958 (Commerce §232 transformers report, 2021-11-18) |
| 2019 sheet imports "about 27,000 metric tons" | 27 kt | measured | — | same |
| 2019 sheet imports "less than 20 percent of domestic consumption (tonnage)" | <20% | measured | — | same, citing redacted Table VII-11 |
| 2017 sheet import share "a high of 37 percent" | 37% | measured | — | same |
| GOES in imported laminations/cores, 2019 | 68 kt | secondhand | Core Coalition (fn 81) | same |
| All-forms import penetration 2019 "approximately 44 percent" | 44% | estimate | — | same |
| 2020 cores 96 kt, penetration "over 50 percent" with steady sheet trade | >50% | estimate | Core Coalition | same |
| AK Steel GOES capacity "approximately 285,000 tons" (short) | 258.5 kt | stated | AK Steel (petitioner) | USITC Pub. 4491 (2014), pdf p. 153 |
| AK planned GOES capacity "approximately 344,000 tons" | 312 kt | secondhand | AK Steel | 2007 AK release via trade press; FY2008 10-K confirms $268M program, no tonnage |
| Cliffs "up to 250,000 net tons" of all electrical steel | 226.8 kt | stated | Cleveland-Cliffs | Cliffs release 2020-11-02; repeated 2024-04-01 |
| 2019 U.S. GOES exports: total / domestic / re-exports | 45.7 / 34.8 / 10.9 kt | measured | — | UN Comtrade (U.S.-reported), `comtrade_us_goes_forms.csv` |

## Method (code: `radiant/data/goes_research.py::phase0_reconciliation`)

With M = 27 kt and sheet consumption S:
- M/S < 0.20 → S > 135 kt
- (27 + 68)/(S + 68) ≈ 0.44 (read as 0.435–0.445) → S = 145.5–150.4 kt (central 147.9)
- (27 + 96)/(S + 96) > 0.50 in 2020 with steady sheet trade → S < 150 kt

So S = 145.5–150 kt. Implied 2019 production = S − 27 + 45.7 = **164–169 kt**.

Cross-check, independent year: 2017 imports were 67.8 kt at a 37% share → S₂₀₁₇ ≈ 183 kt → production ≈ **162 kt**.

## Re-exports

Census/Comtrade "exports" include re-exports of foreign GOES: 3% (2015) up to 39% (2020), 24% in 2019, and 3% by 2025. Re-exports don't change implied production (the identity is the same whether re-exports are netted from imports or from exports). They do change who used what. Foreign sheet that actually stayed in the U.S. in 2019 was 27.9 − 10.9 = **17.0 kt**, not 27. Domestic-origin exports were 34.8 kt, so the U.S. was a net exporter of sheet even on a domestic basis.

## Verdict on the inputs

| Input | Status |
|---|---|
| 220 kt consumption | **Off.** It is all-forms use (~216 kt), not sheet use (~148 kt). Adding 68 kt of cores on top double counts. |
| ~227 kt capacity | **Consistent.** It is all-electrical-steel capacity (GOES + NOES), and implied GOES production (164–169 kt) sits under it. It stays as an upper bound. AK stated 258.5 kt of GOES-only capacity in 2014, so the true 2019 GOES ceiling may be higher; Phase 1 checks this. |
| 45.7 kt exports | **Correct as total exports**; 10.9 kt of it is re-exports. Domestic exports were 34.8 kt. |

**Implied 2019 utilization:** 164–169 kt against 227 kt (all electrical) is ≤ 74%. Against AK's 258.5 kt GOES figure it is ~64–65%, consistent with Commerce's redacted remark that the plant "cannot operate profitably" at its 2019 utilization.

## What this means for later phases (no headline change yet, per plan rule 7)

The current headline (33% foreign in 2019 → 41–44% floor) uses 288 kt. Phase 5 must rebuild it on ~216 kt all-forms use. With the same 95 kt of foreign GOES, the 2019 foreign share is **~44%** (Commerce's own figure), not 33%.
