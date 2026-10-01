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
    """U.S.-reported world total net weight (kt) for a flow (M, X, DX, RX); None if absent.

    Some world rows carry value but no weight (e.g. 2016 imports of 722611); then the partner rows,
    which do carry weight, are summed for that code instead.
    """
    if not Path(path).exists():
        return None
    rows = [r for r in csv.DictReader(Path(path).open())
            if int(r['year']) == year and r['flow'] == flow and r['hs6'] in codes]
    total, found = 0.0, False
    for c in codes:
        world = [r for r in rows if r['hs6'] == c and r['partner_code'] == '0']
        if world and world[0]['net_kg'] != '':
            total, found = total + float(world[0]['net_kg']), True
            continue
        parts = [float(r['net_kg']) for r in rows if r['hs6'] == c and r['partner_code'] != '0' and r['net_kg'] != '']
        if parts:
            total, found = total + sum(parts), True
    return total / 1e6 if found else None


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


# --- Phase 2: trade by country and form ----------------------------------------------
NORTH_AMERICA = ('Canada', 'Mexico')
CORE_PARTS_HS6 = ('850490',)
LIQUID_TRANSFORMERS_HS6 = ('850421', '850422', '850423')

DOE2022_GOES_SHARE_OF_TRANSFORMER_WEIGHT = Fact(
    'DOE2022_HEGEDIC2016_CORE_40PCT', 0.40, 'GOES core share of transformer weight', 'c. 2016', '2022-02',
    'secondhand', '', 'https://www.energy.gov/sites/default/files/2022-02/Electric%20Grid%20Supply%20Chain%20Report%20-%20Final.pdf',
    'DOE 2022 grid supply chain review, p. 13: "The core steel made of GOES accounts for 40% (Hegedic et al., 2016) of the '
    'transformer weight." Context is LPT end-of-life.')
NLR2026_GOES_SHARE_OF_LPT_WEIGHT = Fact(
    'NLR2026_TP_6A40_97167_TABLE3_GOES', 0.48, 'GOES mass fraction (LPT reference model, >=100 MVA)', '2026', '2026-01',
    'model', '', 'https://docs.nlr.gov/docs/fy26osti/97167.pdf', 'NLR reference material model: 600 kg/MVA, 48% GOES.')
COMMERCE2021_DOUBLE_COUNT_CAVEAT = Fact(
    'COMMERCE2021_ROUND_TRIP_ASSUMED_MINIMAL', 0.0, 'qualitative', '2019', '2021-11-18', 'stated', '', FR2021,
    '"this number could include double counting from U.S. exports of GOES that is then imported into the United States in '
    'the form of cores, but this is likely minimal because Canada was not a major destination for U.S. GOES exports".')
COGENT_JFE_CANADA = Fact(
    'MAGNETICS2019_COGENT_JFE_SHOJI', 0.0, 'qualitative', '2019-', '2019', 'stated', 'JFE Shoji',
    'https://magneticsmag.com/jfe-gains-foothold-in-na-with-acquisition-of-cogent-power-from-tata-steel/',
    'JFE Shoji bought Cogent Power (Burlington, Ontario) from Tata Steel in 2019; described as the largest North American '
    'transformer-core maker (mitre, wound, amorphous cores). Commerce notes Tata-owned Orb Steel (UK) had been a major '
    'supplier to Cogent.')
COREFFICIENT_MEXICO = Fact(
    'COREFFICIENT_MONTERREY', 0.0, 'qualitative', '2026', '2026', 'stated', 'Corefficient (Kloeckner Metals)',
    'https://corefficientsrl.com/', 'Monterrey, Mexico core maker (Kloeckner Metals) supplying the U.S., Canada and Mexico.')
PROLEC_GE_MEXICO = Fact(
    'GEVERNOVA_PROLEC_GE', 0.0, 'qualitative', '2025', '2025', 'stated', 'GE Vernova',
    'https://www.gevernova.com/news/press-releases/ge-vernova-fully-acquire-prolec-ge-joint-venture',
    'Prolec GE (Monterrey) transformer maker; GE Vernova moved to acquire the full joint venture.')

# BLS PPI, power/distribution/specialty transformer manufacturing (PCU335311335311), annual mean of monthly values.
TRANSFORMER_PPI = {2015: 230.2, 2016: 227.8, 2017: 234.6, 2018: 245.9, 2019: 252.1, 2020: 255.3, 2021: 299.6,
                   2022: 396.3, 2023: 416.6, 2024: 429.7, 2025: 442.7}
COMMERCE2019_LPT_IMPORT_UNITS = 617  # HTS 8504.23.0080 (>100 MVA), FR 2021-24958 Figure VIII-3 (USITC DataWeb)
NLR2026_LPT_GOES_KG_PER_MVA = 600.0 * 0.48  # NLR reference model: 600 kg/MVA x 48% GOES

PHASE2_FACTS = (DOE2022_GOES_SHARE_OF_TRANSFORMER_WEIGHT, NLR2026_GOES_SHARE_OF_LPT_WEIGHT, COMMERCE2021_DOUBLE_COUNT_CAVEAT,
                COGENT_JFE_CANADA, COREFFICIENT_MEXICO, PROLEC_GE_MEXICO)


def _partner_rows(path: Path = COMTRADE_PATH) -> list[dict]:
    return [r for r in csv.DictReader(Path(path).open()) if r['partner_code'] != '0']


def _sum(rows, codes, year, flow, field, partners=None) -> float:
    return sum(float(r[field] or 0) for r in rows if r['hs6'] in codes and int(r['year']) == year and r['flow'] == flow
               and (partners is None or r['partner'] in partners))


def partner_table(year: int, flow: str, codes: tuple[str, ...] = GOES_HS6, top: int = 5, path: Path = COMTRADE_PATH) -> list[tuple[str, float]]:
    """Top partners by net weight (kt) for one year and flow."""
    rows = _partner_rows(path)
    by: dict[str, float] = {}
    for r in rows:
        if r['hs6'] in codes and int(r['year']) == year and r['flow'] == flow:
            by[r['partner']] = by.get(r['partner'], 0.0) + float(r['net_kg'] or 0) / 1e6
    return sorted(by.items(), key=lambda kv: -kv[1])[:top]


def phase2_round_trip(path: Path = COMTRADE_PATH) -> dict[int, dict]:
    """Share of U.S. GOES sheet exports going to Canada + Mexico, the core-making countries."""
    rows, out = _partner_rows(path), {}
    for y in range(2015, 2026):
        d = {}
        for flow in ('DX', 'RX'):
            tot = _sum(rows, GOES_HS6, y, flow, 'net_kg')
            na = _sum(rows, GOES_HS6, y, flow, 'net_kg', NORTH_AMERICA)
            d[flow] = {'kt': tot / 1e6, 'to_canada_mexico_kt': na / 1e6, 'share': na / tot if tot else None}
        out[y] = d
    return out


def phase2_embodied(path: Path = COMTRADE_PATH) -> dict[int, dict]:
    """GOES in imported cores and finished transformers, by year: measured values, estimated tonnes.

    Cores (8504.90 from Canada + Mexico): no weight is reported. Index = Commerce's 68 kt (2019) scaled by the
    real value of these imports, deflated by the U.S. GOES import unit value. Range = [2019 level, index].
    Caveat: 8504.90 also holds non-core parts; Run 054's lamination unit counts fell 17% in 2024 while this index rose.
    Finished transformers: Comtrade's weights for 8504.21-.34 are imputed from value (every partner has the same
    kg per dollar within a year), so they are not used. Instead a lower bound for large power transformers:
    Commerce's 617 imported LPTs in 2019 x 100 MVA (the class minimum) x NLR's 288 kg GOES/MVA = 17.8 kt, scaled to
    other years by the real value of 8504.23 imports (deflated by the BLS transformer PPI). Smaller transformers
    are excluded, so this is a floor on the transformer channel, not an estimate of it.
    """
    rows, out = _partner_rows(path), {}
    v19 = _sum(rows, CORE_PARTS_HS6, 2019, 'M', 'value_usd', NORTH_AMERICA)
    p19 = _sum(rows, GOES_HS6, 2019, 'M', 'value_usd') / _sum(rows, GOES_HS6, 2019, 'M', 'net_kg')
    base = COMMERCE_2019_EMBODIED_CORES.value
    lpt19 = COMMERCE2019_LPT_IMPORT_UNITS * 100.0 * NLR2026_LPT_GOES_KG_PER_MVA / 1e6  # kt
    t19 = _sum(rows, ('850423',), 2019, 'M', 'value_usd')
    for y in range(2015, 2026):
        v = _sum(rows, CORE_PARTS_HS6, y, 'M', 'value_usd', NORTH_AMERICA)
        p = _sum(rows, GOES_HS6, y, 'M', 'value_usd') / _sum(rows, GOES_HS6, y, 'M', 'net_kg')
        idx = base * (v / v19) / (p / p19)
        t = _sum(rows, ('850423',), y, 'M', 'value_usd')
        out[y] = {
            'cores_value_canada_mexico_musd': v / 1e6,                     # measured
            'goes_import_unit_value_usd_per_kg': p,                       # measured
            'cores_goes_kt_index': idx,                                   # estimate
            'cores_goes_kt_range': tuple(sorted((base, idx))),            # estimate
            'transformers_value_musd': _sum(rows, LIQUID_TRANSFORMERS_HS6 + ('850432', '850433', '850434'), y, 'M', 'value_usd') / 1e6,
            'liquid_transformer_units': _sum(rows, LIQUID_TRANSFORMERS_HS6, y, 'M', 'qty'),  # measured
            'transformer_ppi': TRANSFORMER_PPI[y],                        # measured
            'lpt_goes_kt_lower_bound': lpt19 * (t / t19) / (TRANSFORMER_PPI[y] / TRANSFORMER_PPI[2019]),  # estimate
        }
    return out


# --- Phase 3: demand, bottom-up ------------------------------------------------------
DOE_DT_RULE = 'https://www.energy.gov/sites/default/files/2024-04/dt_ecs_fr.pdf'
DOE_LPT_2024 = ('https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer'
                '%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf')

DOE2024_DT_CORE_STEEL = Fact(
    'DOE2024_DT_CORE_STEEL_225KT', 225.0, 'kt/year core steel, all U.S. distribution transformers', 'current (rule, 2024)',
    '2024-04', 'estimate', '', DOE_DT_RULE,
    'Final rule p. 537: "the U.S. annual demand for core steel in distribution transformer applications (estimated to be '
    'approximately 225,000 metric tons)". Covers all DTs sold in the U.S., so it includes cores of imported DTs.')
DOE2024_LIQUID_DT_CORE_STEEL = Fact(
    'DOE2024_LIQUID_DT_CORE_STEEL_185KT', 185.0, 'kt/year core steel, liquid-immersed DTs', 'no-new-standards case',
    '2024-04', 'estimate', '', DOE_DT_RULE,
    'Final rule p. 210: "~185,000 metric tons for liquid-immersed distribution transformers assumed in the no-new standards '
    'case"; ~146,000 t stays GOES under the adopted standard; ~48,000 t of amorphous replaces GOES (from 2029).')
CLIFFS2023_AMORPHOUS_SHARE = Fact(
    'DOE2024_RULE_CLIFFS_AMORPHOUS_3PCT', 0.03, 'amorphous share of DT market', 'c. 2023', '2024-04', 'stated',
    'Cleveland-Cliffs', DOE_DT_RULE,
    'Final rule p. 501, Cliffs comment: amorphous cores "currently constitutes about three percent of the market for '
    'distribution transformers".')
MTC2024_DT_GOES = Fact(
    'MTC2024_DT_GOES_175KT', 175.0, 'kt/year GOES for U.S. DTs', 'c. 2023', '2024-04-22', 'stated', 'MTC (commenter)',
    'https://public-inspection.federalregister.gov/2024-07480.pdf', 'Stakeholder comment recorded in the DOE rule.')
DOE2024_LPT_WEIGHT = Fact(
    'DOE2024_LPT_WEIGHT_150_400T', 150.0, 't per LPT (low end; high end 400)', '2024', '2024-07', 'stated', '',
    DOE_LPT_2024, '"LPTs typically weigh between 150 and 400 tons" (DOE LPT Resilience Report, p. 2).')
DOE2024_LPT_DEMAND_2027 = Fact(
    'DOE2024_LPT_DEMAND_900_UNITS_2027', 900.0, 'units/year (>60 MVA)', 'by 2027', '2024-07', 'estimate', '',
    DOE_LPT_2024, '"U.S. demand for new transformers (> 60MVA) was ~750 units" in 2019, "expected to increase to ~900 '
    'units annually by 2027".')
DOE2024_SHEET_PENETRATION_RANGE = Fact(
    'DOE2024_GOES_SHEET_PENETRATION_12_37', 0.12, 'share (low; high 0.37)', '2015-2019', '2024-07', 'secondhand', '',
    DOE_LPT_2024, '"imported GOES as low as 12 percent, or as high as 37 percent between 2015-2019" (citing Commerce).')
NREL2024_DT_CAPACITY_2050 = Fact(
    'NREL2024_92076_DT_CAPACITY_2050', 1.6, 'x 2021 DT capacity needed in 2050 (low; high 2.6)', '2021-2050',
    '2024-11-27', 'model', '', 'https://nrel.gov/docs/fy25osti/92076.pdf',
    'NREL: DT capacity needed in 2050 is 160-260% of 2021; 60-80 million units in service, ~55% older than 33 years.')

PHASE3_FACTS = (DOE2024_DT_CORE_STEEL, DOE2024_LIQUID_DT_CORE_STEEL, CLIFFS2023_AMORPHOUS_SHARE, MTC2024_DT_GOES,
                DOE2024_LPT_WEIGHT, DOE2024_LPT_DEMAND_2027, DOE2024_SHEET_PENETRATION_RANGE, NREL2024_DT_CAPACITY_2050)

# Commerce 2019 unit balance, FR 2021-24958 Figure VIII-3 (BIS survey production; USITC DataWeb trade): measured.
COMMERCE2019_UNITS = {  # (production, imports, exports)
    'dt_liquid_lt_650kva': (1_035_055, 210_999, 33_871),
    'dt_liquid_650_10000kva': (23_298, 8_240, 3_029),
    'power_10_100mva': (1_640, 594, 99),
    'lpt_gt_100mva': (137, 617, 4),
}


def phase3_demand_comparison() -> dict:
    """2019 bottom-up GOES use by transformer class vs top-down supply including finished-transformer imports (kt)."""
    p0 = phase0_reconciliation()
    dt_goes = (MTC2024_DT_GOES.value, DOE2024_DT_CORE_STEEL.value * (1 - CLIFFS2023_AMORPHOUS_SHARE.value))
    goes_per_lpt_t = (DOE2024_LPT_WEIGHT.value * DOE2022_GOES_SHARE_OF_TRANSFORMER_WEIGHT.value,
                      400.0 * NLR2026_GOES_SHARE_OF_LPT_WEIGHT.value)
    u = COMMERCE2019_UNITS
    dt_prod = u['dt_liquid_lt_650kva'][0] + u['dt_liquid_650_10000kva'][0]
    dt_imp = u['dt_liquid_lt_650kva'][1] + u['dt_liquid_650_10000kva'][1]
    dt_exp = u['dt_liquid_lt_650kva'][2] + u['dt_liquid_650_10000kva'][2]
    dt_ac = dt_prod + dt_imp - dt_exp
    lpt_prod, lpt_imp, lpt_exp = u['lpt_gt_100mva']
    lpt_ac = lpt_prod + lpt_imp - lpt_exp
    rng = lambda k, pair: (k * pair[0], k * pair[1])
    bottom_up = {
        'distribution_transformers': dt_goes,                                   # estimate (DOE / MTC, c. 2023)
        'large_power_transformers': rng(lpt_ac / 1000, goes_per_lpt_t),         # estimate
        'power_10_100mva': None, 'non_transformer_uses': None,                  # no in-scope intensity: unquantified
    }
    dt_import_share = dt_imp / dt_ac
    top_down = {
        'sheet_consumption': p0['sheet_consumption_2019_kt'],
        'cores_imported': (COMMERCE_2019_EMBODIED_CORES.value,) * 2,
        'lpt_imported': rng(lpt_imp / 1000, goes_per_lpt_t),
        'dt_imported': rng(dt_import_share, dt_goes),
        'power_10_100mva_imported': None,
    }
    tot = lambda d: (sum(v[0] for v in d.values() if v), sum(v[1] for v in d.values() if v))
    # Domestic check: sheet + cores (what U.S. transformer plants use) vs GOES in U.S.-made transformers.
    dom_need = (dt_goes[0] * (dt_prod - dt_exp) / dt_ac + lpt_prod * goes_per_lpt_t[0] / 1000,
                dt_goes[1] * (dt_prod - dt_exp) / dt_ac + lpt_prod * goes_per_lpt_t[1] / 1000)
    sc = p0['sheet_consumption_2019_kt']
    dom_supply = (sc[0] + COMMERCE_2019_EMBODIED_CORES.value, sc[1] + COMMERCE_2019_EMBODIED_CORES.value)
    bu, td = tot(bottom_up), tot(top_down)
    return {
        'goes_per_lpt_t': goes_per_lpt_t, 'dt_import_unit_share': dt_import_share,
        'bottom_up_kt': bottom_up, 'bottom_up_total_known_kt': bu,
        'top_down_kt': top_down, 'top_down_total_kt': td,
        'ranges_overlap': bu[1] >= td[0] and td[1] >= bu[0],
        'domestic_transformer_need_kt': dom_need, 'domestic_goes_supply_kt': dom_supply,
        'residual_for_medium_power_and_other_kt': (dom_supply[0] - dom_need[1], dom_supply[1] - dom_need[0]),
        'evidence_type': 'estimate',
    }
