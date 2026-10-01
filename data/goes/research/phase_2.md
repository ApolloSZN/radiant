# Phase 2 memo — trade by country and form

Source: U.S.-reported annual trade via the UN Comtrade public API (reporter 842), `scripts/fetch_comtrade_goes.py` → `comtrade_us_goes_forms.csv`. It agrees with the Census API panel within 1% (exports) and 5% (imports; Comtrade uses general imports, Census consumption imports), 2019–2024. Code: `radiant/data/goes_research.py` (`partner_table`, `phase2_round_trip`, `phase2_embodied`).

### GOES sheet: imports, exports, re-exports (kt, U.S.-reported via UN Comtrade)

| Year | Imports | Top import sources | Domestic exports | to Canada+Mexico | Re-exports | to Canada+Mexico |
|---|---|---|---|---|---|---|
| 2015 | 28.0 | Japan 10.1, Korea 4.1, Russian Federation 3.8 | n/a | n/a | 3.0 | 99% |
| 2016 | 35.6 | Japan 10.4, Russian Federation 5.9, Korea 5.3 | 57.0 | 32% | 4.6 | 100% |
| 2017 | 67.8 | Japan 26.2, Korea 18.9, China 9.1 | 42.8 | 24% | 4.0 | 100% |
| 2018 | 58.9 | Korea 22.8, Japan 17.3, China 4.7 | 41.5 | 22% | 6.0 | 98% |
| 2019 | 27.9 | Korea 13.0, Japan 6.6, Thailand 2.7 | 34.8 | 15% | 10.9 | 100% |
| 2020 | 25.2 | Korea 12.7, Japan 7.8, Russian Federation 2.0 | 18.9 | 36% | 11.9 | 100% |
| 2021 | 42.0 | Japan 23.0, Korea 16.9, Russian Federation 1.2 | 34.6 | 79% | 13.0 | 100% |
| 2022 | 20.1 | Japan 9.8, Korea 6.4, Canada 2.3 | 59.8 | 90% | 11.9 | 100% |
| 2023 | 31.6 | Japan 14.0, Korea 12.4, Canada 1.7 | 40.8 | 82% | 5.1 | 100% |
| 2024 | 35.2 | Korea 15.2, Japan 14.9, Czechia 2.0 | 35.3 | 81% | 2.2 | 100% |
| 2025 | 19.9 | Japan 11.9, Korea 3.9, Czechia 1.2 | 45.0 | 84% | 1.2 | 99% |

### Embodied channels

| Year | Core parts (8504.90) from CA+MX, $M | GOES import price $/kg | GOES in cores, index kt (estimate) | Transformer imports $M | Liquid transformer units (k) | Transformer PPI | GOES in imported LPTs, lower bound kt (estimate) |
|---|---|---|---|---|---|---|---|
| 2015 | 326 | 2.50 | 34 | 2139 | 228 | 230.2 | 21.3 |
| 2016 | 381 | 2.32 | 43 | 2083 | 164 | 227.8 | 21.5 |
| 2017 | 364 | 2.20 | 43 | 1882 | 191 | 234.6 | 16.8 |
| 2018 | 413 | 2.04 | 53 | 2004 | 202 | 245.9 | 16.3 |
| 2019 | 502 | 1.94 | 68 | 2189 | 216 | 252.1 | 17.8 |
| 2020 | 519 | 1.97 | 69 | 2432 | 273 | 255.3 | 20.7 |
| 2021 | 540 | 2.18 | 65 | 2473 | 282 | 299.6 | 16.4 |
| 2022 | 733 | 3.45 | 56 | 3398 | 325 | 396.3 | 14.6 |
| 2023 | 903 | 4.04 | 59 | 5258 | 490 | 416.6 | 21.3 |
| 2024 | 1175 | 3.38 | 91 | 7516 | 498 | 429.7 | 31.9 |
| 2025 | 1376 | 3.32 | 109 | 9308 | 399 | 442.7 | 43.1 |

## Findings

1. **Sheet imports come from Japan and Korea**, every year. Canada and Mexico supply almost no GOES sheet.
2. **The round trip is real, and it started in 2021.** Before 2020, 15–32% of U.S.-made GOES exports went to Canada and Mexico, and most went to Belgium and India. From 2021 to 2025 it was **79–90%**, mainly to Canada, home of JFE Shoji Power Canada (ex-Cogent), the largest North American core maker. Re-exports of foreign GOES go almost entirely to Canada and Mexico in every year. Commerce's 2021 report assumed double counting between sheet exports and core imports was "likely minimal because Canada was not a major destination for U.S. GOES exports." That was true for 2019 and false from 2021. So some of the GOES in imported cores is U.S. steel coming back, and the U.S. "net exporter" status overstates domestic self-sufficiency. This is evidence for the round trip, not a measurement of its size: export destinations are known, but core makers' steel mix is not.
3. **Cores: no weight exists in the trade data.** 8504.90 (transformer, inductor and converter parts) is reported in value only; Comtrade's weights are blank or zero. Canada+Mexico 8504.90 imports rose from $502M (2019) to $1,376M (2025). Scaling Commerce's 68 kt (2019) by that value deflated by the GOES import price gives **~109 kt in 2025** (index, `estimate`). The range used later is 68–109 kt. Counter-evidence: the lamination unit counts in Run 054 fell 17% in 2024, and 8504.90 also contains non-core parts.
4. **Finished transformers: Comtrade's tonnes are not real.** Every country has the same kg per dollar within a year (0.132 kg/$ for 8504.23 in 2019), so the weights were calculated from value. A test now blocks their use. Measured instead: transformer imports rose from **$2.19B (2019) to $9.31B (2025)**. Liquid-transformer units went from 216k to 399k, while the BLS transformer price index rose 76%.
5. **A floor for GOES inside imported large power transformers.** Commerce counted 617 imported LPTs over 100 MVA in 2019. Even if each were exactly 100 MVA, NLR's 288 kg GOES per MVA gives **at least 17.8 kt**. Scaled by the real value of 8504.23 imports, that becomes **at least 43 kt in 2025**. Smaller transformers are left out, so the transformer channel is larger than this.

## Who makes the cores (stated sources)
- **JFE Shoji Power Canada (ex-Cogent Power), Burlington ON** — largest North American core maker; owned by Tata until 2019, when Tata-owned Orb Steel (UK) was a major supplier; now owned by the trading arm of Japanese mill JFE.
- **Corefficient, Monterrey MX** (Kloeckner Metals) — core supplier to the U.S., Canada and Mexico.
- **Prolec GE, Monterrey MX** — transformer maker; GE Vernova moved to acquire it fully.
- Commerce (2021): Canada (68%) and Mexico (29%) supplied over 95% of U.S. lamination/core imports.

## Still unknown
- The GOES tonnage in imported cores after 2020 (no weights collected).
- How much of Canadian/Mexican core output uses U.S. vs Japanese/Korean GOES.
- GOES in imported distribution transformers.
