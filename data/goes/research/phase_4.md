# Phase 4 memo — the market and the money

Code: `radiant/data/goes_research.py` (`TRANSFORMER_EXPANSIONS`, `LEAD_TIMES`, `POLICY_TIMELINE`, `phase4_prices`).

## Prices (measured)

| Year | GOES import $/kg (U.S.-reported) | BLS transformer PPI (PCU335311335311) |
|---|---|---|
| 2015 | 2.50 | 230.2 |
| 2016 | 2.32 | 227.8 |
| 2017 | 2.20 | 234.6 |
| 2018 | 2.04 | 245.9 |
| 2019 | 1.94 | 252.1 |
| 2020 | 1.97 | 255.3 |
| 2021 | 2.18 | 299.6 |
| 2022 | 3.45 | 396.3 |
| 2023 | 4.04 | 416.6 |
| 2024 | 3.38 | 429.7 |
| 2025 | 3.32 | 442.7 |

GOES import prices fell from 2015 to 2019, then **doubled by 2023** ($1.94 → $4.04/kg) and stayed ~70% above 2019 into 2025. Transformer prices rose **76%** from 2019 to 2025, with most of the jump in 2021–22. BLS publishes **no** electrical-steel PPI; none was found.

## Lead times
- LPTs: 36 months commonly quoted, up to 60 (DOE 2024, stated).
- All transformers: ~50 weeks (2021) → ~120 weeks average (2024); LPTs and GSUs 80–210 weeks (NIAC draft 2024, secondhand).
- Distribution transformers: ~2 years at peak (4× pre-2022), down to ~30 weeks by Q2 2025 (CRS 2026, secondhand).

## Transformer-plant expansions announced since 2022

| Company | Site | Product | $M | Capacity | Online | Type |
|---|---|---|---|---|---|---|
| Hitachi Energy | South Boston, VA | large power transformers | 457 | largest LPT plant in the U.S. | 2028 | secondhand |
| Hitachi Energy | Reynosa, MX (+VA, PA) | distribution transformers (MX) | 155 | $70M new DT factory in Mexico | c. 2026 | secondhand |
| Siemens Energy | Charlotte, NC | large power transformers | 150 | new LPT factory; first units early 2026 | 2026 | stated |
| HD Hyundai Electric | Montgomery, AL (2nd plant) | extra-high-voltage power transformers | 200 | +50% EHV capacity; 765 kV | 2027-04 | secondhand |
| Hyosung HICO | Memphis, TN | power transformers (to 765 kV) | 208 | +50% (new facility); >$300M since 2019 | c. 2027 | secondhand |
| Prolec GE | Goldsboro, NC | medium power transformers | 140 | doubles medium-power capacity | c. 2026 | secondhand |
| Eaton | Jonesville, SC | three-phase transformers | — | third U.S. three-phase plant | 2027 | secondhand |
| WEG | Washington, MO | specialty/power transformers | 77 | +50% | by 2028 | secondhand |
| Virginia Transformer | Rincon, GA | power transformers | — | +~70%; 400 jobs | from 2026 | secondhand |
| SPX Transformer Solutions | Waukesha, WI | power transformers | 70 | 200+ jobs | c. 2025 | secondhand |
| ERMCO | West Tennessee | distribution transformers | — | three-phase project; 400 jobs; $54.1M tax-credit financing | phased | secondhand |

About **$1.46 billion** of disclosed investment across 11 announcements. Most add power-transformer capacity (Hitachi, Siemens, Hyundai, Hyosung, Prolec GE, Virginia Transformer, WEG, SPX). **None states where its GOES will come from.** Most of these makers are foreign-owned (Japan/Switzerland, Germany, Korea ×2, Brazil) and historically used foreign GOES. More U.S. transformer assembly does not automatically mean more U.S. GOES.

## Policy timeline
- **1994-06** — AD orders on GOES from Japan and Italy; CVD on Italy. [source](https://www.govinfo.gov/content/pkg/FR-2006-03-28/pdf/E6-4477.pdf)
- **2006-03-14** — Those orders revoked: domestic industry did not take part in the sunset review. [source](https://www.govinfo.gov/content/pkg/FR-2006-03-28/pdf/E6-4477.pdf)
- **2014-10/11** — USITC negative final determinations on GOES from all 7 countries: no AD/CVD orders issued. [source](https://www.usitc.gov/press_room/news_release/2014/er1023mm2.htm)
- **2016** — ATI exits GOES; AK Steel becomes the sole U.S. producer. [source](https://www.sec.gov/Archives/edgar/data/1018963/000101896317000007/atify201610-k.htm)
- **2018-03** — Section 232: 25% tariff on steel, including GOES. [source](https://www.everycrsreport.com/reports/R48933.html)
- **2019-05-17** — U.S.-Mexico joint statement on steel (transshipment monitoring). [source](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2020/november/ustr-statement-successful-conclusion-steel-negotiations-mexico)
- **2020-11-05** — Mexico monitors exports of laminations/cores made from non-North American GOES; Mexico excluded from any Section 232 transformer action. [source](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2020/november/ustr-statement-successful-conclusion-steel-negotiations-mexico)
- **2021-11-18** — Commerce publishes Section 232 transformer/GOES report (finding: imports threaten national security). [source](https://www.govinfo.gov/content/pkg/FR-2021-11-18/pdf/2021-24958.pdf)
- **2024-03** — DOE grant up to $75M for Butler Works induction slab reheat furnaces (electrical steel). [source](https://www.sec.gov/Archives/edgar/data/764065/000076406525000058/clf-20241231.htm)
- **2024-04** — DOE distribution-transformer efficiency rule; compliance 2029-04-23; ~75% of market can comply with GOES. [source](https://www.energy.gov/sites/default/files/2024-04/dt_ecs_fr.pdf)
- **2025-06** — Section 232 steel tariff raised to 50%. [source](https://www.everycrsreport.com/reports/R48933.html)
- **2025-08-15** — Commerce adds DT cores and laminations to Section 232 derivatives at 50%. [source](https://www.everycrsreport.com/reports/R48933.html)
- **2026-06-15** — DOE RFI re-examines the DT standard; compliance date still 2029-04-23. [source](https://www.energy.gov/cmei/articles/doe-issues-request-information-rfi-energy-conservation-standards-distribution)
- **2026-07-01** — DLA awards Cliffs GOES stockpile IDIQ (up to $400M; up to 53,000 short tons stated). [source](https://www.steelmarketupdate.com/2026/07/06/cliffs-awarded-400m-goes-contract-from-department-of-war/)

**Correction to the plan:** `RESEARCH_PLAN.md` Phase 4 says AD/CVD orders on GOES "are still in force". They are not. The 1994 orders were revoked in 2006, and all seven 2014 cases ended in negative injury findings. GOES imports face **Section 232** tariffs (25% from 2018, 50% from June 2025), and since August 2025 so do DT cores and laminations. Mexico's 2020 agreement excluded Mexican laminations, cores and transformers from any Section 232 transformer action. In return, Mexico monitors exports made from non-North American GOES.

## What the market says about tightness
Prices and lead times both point to a tight 2021–2024 transformer market that eased somewhat in 2025 for distribution transformers. GOES import prices doubled while import tonnage fell. That pattern fits tariff-constrained supply better than a demand shortfall. Comtrade cannot separate the two; Phase 5 treats it as context, not a parameter.
