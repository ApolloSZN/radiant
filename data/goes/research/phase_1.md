# Phase 1 memo — domestic GOES production

**Bottom line.** The one U.S. GOES producer (AK Steel, now Cleveland-Cliffs) has never published GOES-only output. Every public production number is **derived** from trade and Commerce percentages. Capacity is a company claim, and its definition changed from GOES-only (2014) to all electrical steel (2020).

## Production, capacity and utilization

| Year | Capacity (kt) | Type | Production (kt) | Type | Utilization | Notes |
|---|---|---|---|---|---|---|
| c.2009 | 312 (planned) | secondhand, AK | — | — | — | 344,000 short tons per 2007 AK release (trade press); FY2008 10-K confirms a $268M GOES program, no tonnage |
| 2007–08 | — | — | — | — | — | AK stainless+electrical shipments 1,072 / 957 k short tons (measured aggregate; upper bound only) |
| 2014 | 258.5 | stated, AK (petitioner) | redacted | — | — | USITC Pub. 4491: "GOES production capacity is approximately 285,000 tons" |
| 2016 | — | — | — | — | — | ATI exits GOES; Bagdad, PA finishing plant closed (ATI FY2016 10-K). Capacity removed not disclosed |
| 2017 | — | — | ≈162 | estimate | ≈71% of 227 | Commerce 37% sheet import share + Comtrade trade |
| 2019 | — | — | 164–169 | estimate | 72–74% of 227; ~64–65% of 258.5 | Phase 0 |
| 2020 | 226.8 | stated, Cliffs | — | — | — | "up to 250,000 net tons" of all electrical steel (GOES + NOES); repeated 2024 |
| 2020–25 | — | — | — | — | — | Cliffs stainless+electrical shipments (k net tons): 416 (Mar–Dec 2020), 674, 763, 682, 567, 552. Measured aggregate; GOES share undisclosed |
| 2023 | — | — | — | — | — | 70 k short-ton NOES line at Zanesville (GOES finishing plant) |
| 2025–30 | — | — | — | — | — | DLA stockpile: up to 53,000 short tons of GOES over five years (stated ceiling) |
| 2028 | +25% at Butler | stated, Cliffs | — | — | — | Q2 2026 call: induction reheat furnaces; baseline unstated |

## Corrections and cross-checks
- **Repo error fixed.** `goes_import_floor.py` recorded Cliffs FY2025 stainless+electrical shipments as 575 k net tons. The 10-K table says **552** (567 in 2024). "575" in that 10-K is the **$575 million** revenue decrease. Context-only entry; the floor is unaffected.
- **NLR 2026** says 94 kt is "more than 45%" of average 2019–2023 apparent consumption, so that average is **below ~209 kt**. That's consistent with ~148 kt of sheet use and rules out 220 or 288 kt as a sheet baseline. NLR's source is USITC DataWeb trade data, and its production side is undocumented, so it's typed `estimate`.
- **DOE 2022:** LPT makers estimated domestic GOES meets "about 20%" of their demand (secondhand, interviews). DOE also notes the domestic mill cannot make the highest grades. Quality, not just tonnage, limits domestic supply for LPTs.

## Still unknown
- GOES-only capacity after 2014, and how much the 2023 NOES line took from it.
- Annual production in any year other than 2017 and 2019.
- Whether "250,000 net tons" (2020) is all electrical steel or GOES; Cliffs' own context is GOES, but the words say "electrical steel".
