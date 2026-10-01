"""Typed evidence and reconciliations for docs/RESEARCH_PLAN.md (GOES balance sheet).

Every number carries an evidence type from the plan's rules:
  measured   official statistics or audited filings
  stated     company or agency claim
  estimate   published estimate with a method (or a derived estimate whose method is in code here)
  model      scenario output
  secondhand a figure known only through someone else's report
and an ``interested_party`` flag for sources with a stake in the number.

Phases 0-4 only collect and reconcile. Nothing here changes the published headline;
Phase 5 (``goes_balance``) recomputes it.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

COMTRADE_PATH = Path('data/goes/research/comtrade_us_goes_forms.csv')
GOES_HS6 = ('722511', '722611')
SHORT_TON_T = 0.90718474
EVIDENCE_TYPES = {'measured', 'stated', 'estimate', 'model', 'secondhand'}


@dataclass(frozen=True)
class Fact:
    fact_id: str
    value: float
    unit: str
    period: str
    published: str
    evidence_type: str
    interested_party: str  # '' when none
    source: str
    note: str


FR2021 = 'https://www.govinfo.gov/content/pkg/FR-2021-11-18/pdf/2021-24958.pdf'

# --- Phase 0: the 2019 contradiction -------------------------------------------------
COMMERCE_2019_CONSUMPTION_CORE_COALITION = Fact(
    'COMMERCE2021_GOES_CONSUMPTION_220KT', 220.0, 'kt/year', '"per year" (c. 2019)', '2021-11-18', 'secondhand',
    'Core Coalition (core/lamination importers)', FR2021,
    'Commerce: "U.S. consumption of GOES is estimated at approximately 220,000 metric tons per year"; footnote 64 '
    'cites Core Coalition public comments. Not a Commerce measurement, and not defined as sheet-only.')
COMMERCE_2019_SHEET_IMPORTS = Fact(
    'COMMERCE2021_GOES_IMPORTS_2019', 27.0, 'kt', '2019', '2021-11-18', 'measured', '', FR2021,
    '"The United States imported about 27,000 metric tons of GOES in 2019" (Census basis).')
COMMERCE_2019_SHEET_IMPORT_SHARE_MAX = Fact(
    'COMMERCE2021_GOES_SHEET_PENETRATION_2019', 0.20, 'share (upper bound)', '2019', '2021-11-18', 'measured', '',
    FR2021, '"based on production and trade data for GOES (Table VII-11), imports accounted for less than 20 percent '
    'of domestic consumption (on a tonnage basis) in 2019." Table VII-11 itself is redacted.')
COMMERCE_2017_SHEET_IMPORT_SHARE = Fact(
    'COMMERCE2021_GOES_SHEET_PENETRATION_2017', 0.37, 'share', '2017', '2021-11-18', 'measured', '', FR2021,
    '"This is down from a high of 37 percent in 2017, prior to imposition of the steel tariffs."')
COMMERCE_2019_EMBODIED_CORES = Fact(
    'COMMERCE2021_EMBODIED_CORES_2019', 68.0, 'kt GOES', '2019', '2021-11-18', 'secondhand',
    'Core Coalition (core/lamination importers)', FR2021,
    '68,000 t of GOES imported in laminations and cores; footnote 81: core trade is counted in units, weight is the '
    'Core Coalition estimate.')
COMMERCE_2019_ALL_FORMS_IMPORT_SHARE = Fact(
    'COMMERCE2021_GOES_ALL_FORMS_PENETRATION_2019', 0.44, 'share (approximately)', '2019', '2021-11-18', 'estimate',
    '', FR2021, '"Based on these figures, the import penetration for GOES was approximately 44 percent in 2019."')
COMMERCE_2020_EMBODIED_CORES = Fact(
    'COMMERCE2021_EMBODIED_CORES_2020', 96.0, 'kt GOES', '2020 (estimate)', '2021-11-18', 'secondhand',
    'Core Coalition (core/lamination importers)', FR2021,
    '"Based on the Coalition\'s estimate of 2020 core imports of 96,000 metric tons, and assuming steady U.S. GOES '
    'production and export and import levels, import penetration is estimated to reach over 50 percent this year."')
AK_2014_GOES_CAPACITY = Fact(
    'USITC4491_AK_GOES_CAPACITY_2014', 285_000 * SHORT_TON_T / 1000, 'kt/year GOES', '2014', '2014-09',
    'stated', 'AK Steel (petitioner)', 'https://www.usitc.gov/publications/701_731/pub4491_.pdf',
    'USITC Pub. 4491 (pdf p. 153) quoting AK Steel: "Under current market conditions, its GOES production capacity '
    'is approximately 285,000 tons." Short tons. GOES-only, unlike the 2020 Cliffs 250,000 t all-electrical figure.')
AK_2007_GOES_CAPACITY_PLAN = Fact(
    'AK2007_GOES_CAPACITY_PLAN', 344_000 * SHORT_TON_T / 1000, 'kt/year GOES (planned)', 'on completion c. 2009',
    '2007-10-23', 'secondhand', 'AK Steel', 'https://www.thefabricator.com/thefabricator/news/metalsmaterials/'
    'ak-steel-to-expand-electrical-steel-production-capacity',
    'Trade-press copies of an AK release: GOES capacity "approximately 344,000 tons annually" after the $180M '
    'Butler/Zanesville projects. AK FY2008 10-K confirms $268M of GOES capacity investment but states no tonnage.')
CLIFFS_ELECTRICAL_CAPACITY_2020 = Fact(
    'CLIFFS2020_ELECTRICAL_CAPACITY', 250_000 * SHORT_TON_T / 1000, 'kt/year all electrical steel', '2020',
    '2020-11-02', 'stated', 'Cleveland-Cliffs', 'https://www.clevelandcliffs.com/news/news-releases/detail/10/'
    'cleveland-cliffs-applauds-president-trumps-actions-to',
    'Up to 250,000 net tons/year of electrical steel (GOES + NOES). Repeated by Cliffs officials in 2024 '
    '(Butler Eagle, 2024-04-01). Upper bound on GOES, not a GOES figure.')

PHASE0_FACTS = (COMMERCE_2019_CONSUMPTION_CORE_COALITION, COMMERCE_2019_SHEET_IMPORTS,
                COMMERCE_2019_SHEET_IMPORT_SHARE_MAX, COMMERCE_2017_SHEET_IMPORT_SHARE, COMMERCE_2019_EMBODIED_CORES,
                COMMERCE_2019_ALL_FORMS_IMPORT_SHARE, COMMERCE_2020_EMBODIED_CORES, AK_2014_GOES_CAPACITY,
                AK_2007_GOES_CAPACITY_PLAN, CLIFFS_ELECTRICAL_CAPACITY_2020)


def comtrade_world_kt(year: int, flow: str, codes: tuple[str, ...] = GOES_HS6, path: Path = COMTRADE_PATH) -> float | None:
    """U.S.-reported world total net weight (kt) for a flow (M, X, DX, RX); None if absent."""
    if not Path(path).exists():
        return None
    vals = [float(r['net_kg']) for r in csv.DictReader(Path(path).open())
            if r['partner_code'] == '0' and int(r['year']) == year and r['flow'] == flow and r['hs6'] in codes
            and r['net_kg'] != '']
    return sum(vals) / 1e6 if vals else None


def phase0_reconciliation(path: Path = COMTRADE_PATH) -> dict:
    """Back out 2019 sheet consumption from Commerce's own percentages, then implied production.

    Three Commerce statements bound sheet apparent consumption S (kt), with M = 27 kt sheet imports:
      M / S < 0.20                                 (2019 sheet penetration "less than 20 percent")
      (M + 68) / (S + 68) in [0.435, 0.445)        (2019 all-forms penetration "approximately 44 percent")
      (M + 96) / (S + 96) > 0.50                   (2020: "over 50 percent", steady sheet trade)
    """
    m, c19, c20 = COMMERCE_2019_SHEET_IMPORTS.value, COMMERCE_2019_EMBODIED_CORES.value, COMMERCE_2020_EMBODIED_CORES.value
    lo_sheet = max(m / COMMERCE_2019_SHEET_IMPORT_SHARE_MAX.value, (m + c19) / 0.445 - c19)
    hi_sheet = min((m + c19) / 0.435 - c19, (m + c20) / 0.50 - c20)
    central = (m + c19) / COMMERCE_2019_ALL_FORMS_IMPORT_SHARE.value - c19
    x19 = comtrade_world_kt(2019, 'X', path=path)
    dx19, rx19, m19 = (comtrade_world_kt(2019, f, path=path) for f in ('DX', 'RX', 'M'))
    prod = None if x19 is None else (lo_sheet - m + x19, hi_sheet - m + x19)
    m17, x17 = comtrade_world_kt(2017, 'M', path=path), comtrade_world_kt(2017, 'X', path=path)
    s17 = None if m17 is None else m17 / COMMERCE_2017_SHEET_IMPORT_SHARE.value
    return {
        'sheet_consumption_2019_kt': (lo_sheet, hi_sheet),
        'sheet_consumption_2019_central_kt': central,
        'all_forms_consumption_2019_kt': (lo_sheet + c19, hi_sheet + c19),
        'core_coalition_220kt_matches_all_forms': lo_sheet + c19 <= 220.0 * 1.03 and hi_sheet + c19 >= 220.0 * 0.97,
        'double_count_in_288kt_kt': 220.0 + c19 - (central + c19),
        'implied_production_2019_kt': prod,
        'production_within_all_electrical_capacity': None if prod is None else prod[1] <= CLIFFS_ELECTRICAL_CAPACITY_2020.value,
        'exports_2019_kt': {'total': x19, 'domestic': dx19, 're_exports': rx19},
        'foreign_sheet_retained_2019_kt': None if m19 is None or rx19 is None else m19 - rx19,
        'sheet_consumption_2017_kt': s17,
        'implied_production_2017_kt': None if s17 is None or x17 is None else s17 - m17 + x17,
        'evidence_type': 'estimate',
        'method': 'Commerce percentages (FR 2021-24958) + U.S.-reported trade (UN Comtrade, reporter 842)',
    }


# --- Phase 1: domestic production ----------------------------------------------------
CLIFFS_10K = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000764065&type=10-K'
# Stainless + electrical shipments (thousand net tons), Cliffs 10-K steel-shipments tables. Measured, but GOES is a
# small, undisclosed part of this aggregate: an upper bound only. 2020 covers 2020-03-13 onward (AK acquisition).
CLIFFS_STAINLESS_ELECTRICAL_KNT = {2020: 416, 2021: 674, 2022: 763, 2023: 682, 2024: 567, 2025: 552}
AK_STAINLESS_ELECTRICAL_KNT = {2007: 1072.0, 2008: 957.1}  # AK FY2008 10-K "Tons shipped by product category"

ATI_GOES_EXIT_2016 = Fact(
    'ATI2016_10K_GOES_EXIT', 2016.0, 'year of exit', '2016', '2017-02', 'measured', 'ATI',
    'https://www.sec.gov/Archives/edgar/data/1018963/000101896317000007/atify201610-k.htm',
    'ATI exited "the unprofitable grain-oriented electrical steel (GOES) product line" in early 2016 and permanently '
    'closed the Bagdad, PA GOES finishing facility. Capacity removed is not disclosed.')
CLIFFS_ZANESVILLE_NOES_2023 = Fact(
    'AIST2023_CLIFFS_ZANESVILLE_NOES', 70_000 * SHORT_TON_T / 1000, 'kt/year NOES', '2023-07', '2023-07-27',
    'stated', 'Cleveland-Cliffs', 'https://www.aist.org/cleveland-cliffs-commissions-noes-expansion',
    '70,000-ton non-oriented (Motor-Max) expansion commissioned at Zanesville, the GOES finishing plant. Shares the '
    'electrical-steel footprint; no stated effect on GOES.')
CLIFFS_BUTLER_GOES_PLUS25 = Fact(
    'CLIFFS_Q2_2026_CALL_BUTLER_GOES_PLUS25', 0.25, 'relative increase in GOES output at Butler', 'completion 2028',
    '2026-07', 'stated', 'Cleveland-Cliffs', 'https://www.clevelandcliffs.com/_assets/_c7d9d552b544a2a36f31808074ad8c21/'
    'clevelandcliffs/db/1111/12098/file/Q2+2026+Earnings+Call+Transcript.pdf',
    '"we are going to be producing more grain-oriented electrical steels as the -- it\'s estimated 25% increase on that '
    'plant specifically with the completion of our induction furnaces in the hot strip mill of Butler." Baseline unstated.')
DOE2022_STAKEHOLDER_DOMESTIC_SHARE = Fact(
    'DOE2022_GRID_SUPPLY_CHAIN_LPT_GOES_20PCT', 0.20, 'share of LPT-maker GOES demand met domestically',
    'c. 2021', '2022-02', 'secondhand', 'LPT manufacturers (interviews)',
    'https://www.energy.gov/sites/default/files/2022-02/Electric%20Grid%20Supply%20Chain%20Report%20-%20Final.pdf',
    '"Some interviewees estimated that domestic supply meets about 20% of domestic demand" (LPT makers only).')
NLR2026_APPARENT_CONSUMPTION_BOUND = Fact(
    'NLR2026_GOES_AC_2019_2023_BOUND', 94.0 / 0.45, 'kt/year (upper bound on 2019-2023 average)', '2019-2023',
    '2026', 'estimate', '', 'https://docs.nlr.gov/docs/fy26osti/97167.pdf',
    'NLR: 94-114 kt/yr of transmission GOES is "more than 45%" of 2019-2023 average apparent consumption, so the '
    'average is below ~209 kt. Source is USITC DataWeb (trade); the production side of NLR\'s figure is undocumented.')

PHASE1_FACTS = (ATI_GOES_EXIT_2016, CLIFFS_ZANESVILLE_NOES_2023, CLIFFS_BUTLER_GOES_PLUS25,
                DOE2022_STAKEHOLDER_DOMESTIC_SHARE, NLR2026_APPARENT_CONSUMPTION_BOUND)


def phase1_production_table(path: Path = COMTRADE_PATH) -> list[dict]:
    """Year-by-year U.S. GOES capacity / production evidence, 2007-2028. None means no source exists."""
    p0 = phase0_reconciliation(path)
    cap20 = CLIFFS_ELECTRICAL_CAPACITY_2020.value
    rows = [
        dict(year=2009, capacity_kt=AK_2007_GOES_CAPACITY_PLAN.value, capacity_type='secondhand (planned, GOES)',
             production_kt=None, production_type=None, note='AK expansion program; FY2008 10-K confirms $268M, no tonnage'),
        dict(year=2014, capacity_kt=AK_2014_GOES_CAPACITY.value, capacity_type='stated (GOES only, AK, petitioner)',
             production_kt=None, production_type=None, note='USITC Pub. 4491; U.S. producer data redacted (AK + ATI)'),
        dict(year=2016, capacity_kt=None, capacity_type=None, production_kt=None, production_type=None,
             note='ATI exits GOES; Cliffs/AK becomes sole producer'),
        dict(year=2017, capacity_kt=None, capacity_type=None,
             production_kt=(p0['implied_production_2017_kt'],) * 2 if p0['implied_production_2017_kt'] else None,
             production_type='estimate (Commerce 37% share + Comtrade trade)', note=''),
        dict(year=2019, capacity_kt=None, capacity_type=None, production_kt=p0['implied_production_2019_kt'],
             production_type='estimate (Commerce percentages + Comtrade trade)', note='Phase 0'),
        dict(year=2020, capacity_kt=cap20, capacity_type='stated (all electrical steel, Cliffs)', production_kt=None,
             production_type=None, note='Repeated 2024. GOES-only capacity not disclosed after 2014'),
        dict(year=2023, capacity_kt=None, capacity_type=None, production_kt=None, production_type=None,
             note='70 kt NOES line commissioned at Zanesville (shares the electrical-steel footprint)'),
        dict(year=2028, capacity_kt=None, capacity_type='stated: +25% GOES at Butler (baseline unstated)',
             production_kt=None, production_type=None, note='Cliffs Q2 2026 call'),
    ]
    for r in rows:
        prod = r['production_kt']
        r['utilization_vs_all_electrical'] = None if prod is None else (prod[0] / cap20, prod[1] / cap20)
        r['aggregate_upper_bound_knt'] = CLIFFS_STAINLESS_ELECTRICAL_KNT.get(r['year']) or AK_STAINLESS_ELECTRICAL_KNT.get(r['year'])
    return rows
