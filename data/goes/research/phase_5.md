# Phase 5 memo — the balance sheet and the rebuilt headline

Code: `radiant/data/goes_balance.py`. Tables: `scripts/build_goes_balance_tables.py`. Chart: `scripts/build_goes_chart.py` → `docs/figures/goes_foreign_share.svg`. Every cell is a (low–high) range in kt GOES with its evidence type. "model" rows depend on the production range, because U.S. GOES output is identified only for 2017 and 2019.

## Accounting
- Sheet use = production + sheet imports − sheet exports.
- All-forms use = sheet use + GOES in imported cores + GOES in imported finished transformers.
- Domestic-origin GOES = production − domestic exports + U.S. steel that comes back inside imports (0 up to exports to Canada/Mexico).
- Foreign share = 1 − domestic-origin / all-forms use. Re-exports are foreign steel passing through.

## Balance sheet 2015–2025 (kt)

| Year | Production | Sheet imports | Re-exports | Domestic exports (to CA+MX) | Sheet use | GOES in cores | in imported LPTs | in imported DTs | All-forms use | Foreign share, all forms | Foreign share, sheet+cores | Type |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 162–259 | 28 | 3 | 97 (n/a) | 90–187 | 34–68 | 44–142 | 33–41 | 202–438 | 46%–81% | 27%–59% | model |
| 2016 | 162–259 | 36 | 5 | 57 (18) | 136–232 | 43–68 | 45–143 | 23–29 | 247–473 | 36%–72% | 20%–49% | model |
| 2017 | 162 | 68 | 4 | 43 (10) | 183 | 43–68 | 35–112 | 27–34 | 289–397 | 55%–70% | 43%–52% | estimate |
| 2018 | 162–259 | 59 | 6 | 42 (9) | 173–270 | 53–68 | 34–109 | 29–36 | 289–483 | 41%–69% | 30%–50% | model |
| 2019 | 164–169 | 28 | 11 | 35 (5) | 146–151 | 68 | 37–118 | 31–39 | 282–376 | 51%–65% | 36%–40% | estimate |
| 2020 | 162–227 | 25 | 12 | 19 (7) | 156–221 | 68–69 | 43–142 | 39–49 | 307–481 | 42%–66% | 26%–37% | model |
| 2021 | 162–227 | 42 | 13 | 35 (27) | 156–221 | 65–68 | 34–142 | 40–50 | 296–481 | 39%–69% | 23%–43% | model |
| 2022 | 162–227 | 20 | 12 | 60 (54) | 110–175 | 56–68 | 30–142 | 47–58 | 243–443 | 28%–73% | 4%–43% | model |
| 2023 | 162–227 | 32 | 5 | 41 (33) | 148–213 | 59–68 | 44–142 | 70–88 | 321–510 | 43%–73% | 19%–44% | model |
| 2024 | 162–227 | 35 | 2 | 35 (29) | 160–224 | 68–91 | 66–142 | 71–89 | 365–546 | 49%–74% | 25%–50% | model |
| 2025 | 162–227 | 20 | 1 | 45 (38) | 136–200 | 68–109 | 90–142 | 57–71 | 350–522 | 47%–74% | 18%–52% | model |

Production in model years ranges from 162 kt (lowest identified) to the stated ceiling (258.5 kt GOES-only to 2019; 226.8 kt all electrical steel from 2020). That range drives most of the width in those years.

## Identity checks (`identity_checks()`)
- Production ≤ capacity in identified years: **pass** (164–169 kt ≤ 226.8 / 258.5).
- Balance closes: 2019 sheet use from U.S.-reported trade (146–151 kt) vs from Commerce's percentages (145.5–150 kt), within 3%: **pass**.
- Top-down vs bottom-up 2019 (Phase 3): ranges overlap: **pass**. Gap explained by 10–100 MVA transformers and non-transformer uses (7–66 kt residual).

## Outlook 2026–2035 (model)

| Year | Demand (kt) | No change: domestic kt / foreign share | Expansion | Best case (expansion + no exports) |
|---|---|---|---|---|
| 2026 | 334–498 | 112 / 67%–78% | 112 / 67%–78% | 157 / 53%–68% |
| 2030 | 382–657 | 121 / 68%–82% | 163 / 57%–75% | 208 / 46%–68% |
| 2035 | 410–756 | 121 / 70%–84% | 163 / 60%–78% | 208 / 49%–72% |

Demand = 2019 all-forms use × NREL distribution-transformer capacity growth (1.6–3.4%/yr) + NLR transmission increment (94–114 kt/yr, phased in by 2030), minus DOE's amorphous shift (48 kt/yr from 2029) on the low side. Domestic supply = identified 2019 output (166 kt), minus 2025-level exports (45 kt), minus the DLA stockpile through 2029 (9.6 kt/yr). Expansion adds Cliffs' stated +25% at Butler from 2028 (capped at 226.8 kt). Best case also keeps all exports at home.

**Key driver:** demand growth meets a single domestic mill whose output is fixed in every scenario but the best case. Expanding the mill and keeping its exports at home cuts the 2035 foreign share by about 20 points (70–84% → 49–72%). It cannot get it below ~46% in any year.

## Headline: what survives

| | Old (Run 053) | New (Run 061) |
|---|---|---|
| 2019 U.S. GOES use, all forms | 288 kt | **282–376 kt** (sheet 146–151 + cores 68 + imported transformers 68–157) |
| 2019 foreign share | 33% | **51–65%** all forms; 36–40% sheet + cores only |
| Forward view | ≥41–44% floor | **≥46% in every scenario through 2035**; 70–84% in 2035 with no change |
| Status | withdrawn | estimate (2019) / model (other years, outlook) |

Why the old headline failed: (1) the 220 kt "consumption" was already all-forms use (Core Coalition), so adding 68 kt of cores double counted them; (2) sheet imports weren't netted for re-exports (10.9 kt in 2019); (3) imported finished transformers were left out on the claim that it "cancels". It does not cancel: that steel is almost all foreign, so leaving it out biases the share down.

**Plan's "what would change the story" — outcomes:**
- Domestic capacity well above 227 kt? No new evidence. AK stated 258.5 kt GOES in 2014, but 2019 output was only 164–169 kt.
- Exports mostly re-exports or round trips? Re-exports are a minority (3–39%). But since 2021, 79–90% of domestic exports go to Canadian/Mexican core makers, so the "net exporter" status is partly a round trip.
- Embodied imports grew after 2020? Yes: cores ~68 → ~109 kt (index), transformer import units +84% (DTs), real LPT import value ×2.4.
- Bottom-up demand far below 288 kt? Sheet + cores (~216 kt) was below 288. Adding imported transformers brings total use to 282–376 kt.
