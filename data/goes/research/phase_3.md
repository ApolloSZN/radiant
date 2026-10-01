# Phase 3 memo — demand, bottom-up

**Question.** Does a bottom-up build of U.S. GOES use, by transformer class, match the top-down figure?

**Answer.** Yes, once finished-transformer imports are counted. In 2019 the U.S. used roughly **280–375 kt of GOES in all forms**, including steel inside imported transformers. That is more than the 216 kt (sheet + cores) Commerce counted, because Commerce, like Radiant until now, left finished transformers out.

## 2019, kt GOES (code: `goes_research.phase3_demand_comparison`)

| Bottom-up (where it's used) | kt | Type | Basis |
|---|---|---|---|
| Distribution transformers | 175–218 | estimate | MTC 175 kt (stakeholder); DOE 225 kt core steel × 97% GOES (Cliffs: amorphous ≈3%) |
| Large power transformers (>100 MVA) | 45–144 | estimate | 750 units (Commerce) × 60–192 t GOES each (DOE: LPTs weigh 150–400 t; GOES share 40% DOE/Hegedic to 48% NLR) |
| Power transformers 10–100 MVA | — | gap | 2,135 units (Commerce), but no sourced GOES intensity in scope |
| Non-transformer uses (reactors, generators) | — | gap | Commerce: market "dominated by transformers"; no tonnage found |
| **Known total** | **220–362** | | |

| Top-down (where it comes from) | kt | Type |
|---|---|---|
| Sheet consumption (U.S. mill + imported sheet) | 145–150 | estimate (Phase 0) |
| GOES in imported cores/laminations | 68 | secondhand (Commerce/Core Coalition) |
| GOES in imported LPTs | 37–118 | estimate: 617 units × 60–192 t |
| GOES in imported distribution transformers | 31–39 | estimate: 17.7% unit import share × DT GOES |
| GOES in imported 10–100 MVA units | — | gap (594 units) |
| **Total** | **281–375** | |

The ranges overlap. The bottom-up side is missing medium power transformers and other uses; the top-down side is missing imported medium power units. Vintages differ: DOE's DT tonnage is a 2023–24 "current" figure, against 2019 trade and unit counts.

**Domestic identity.** U.S.-made distribution transformers and LPTs need 152–206 kt of GOES, against 213–218 kt of sheet + imported cores available to U.S. plants. That leaves 7–66 kt for medium power transformers and non-transformer uses, which is plausible. The Phase 0 base closes.

## Growth drivers (labelled)
- DT capacity needed in 2050: 160–260% of 2021 (NREL 2024, model). That is ~1.6–3.4%/yr compound.
- LPT demand: ~750 units (2019) → ~900/yr by 2027 (DOE 2024, estimate).
- Transmission build-out: 94–114 kt/yr of GOES (NLR 2026, model; already in Radiant).
- DOE efficiency rule (compliance 2029-04-23): ~48 kt/yr of liquid-DT core steel shifts from GOES to amorphous; ~146 kt stays GOES (DOE, estimate). DOE issued an RFI in June 2026 re-examining it.
- Units shipped: ~1.5 M DTs in 2021; 1.4–2.4 M added or replaced each year (CRS R48933, 2026).

## Cross-check from Phase 1 and 2
DOE 2024 says imported GOES sheet ran "12 to 37 percent" of consumption in 2015–2019. 37% is 2017 (Commerce). 12% matches 2016 if imports are counted as 22 kt (the 2016 world row with a missing weight), giving ~183 kt of sheet use, consistent with the 2017 estimate.

## Still unknown
GOES intensity of 10–100 MVA power transformers; non-transformer GOES use; the LPT MVA mix (it drives the 45–144 kt spread).
