"""Phase 5 of docs/RESEARCH_PLAN.md: the U.S. GOES balance sheet (2015-2025), outlook (2026-2035), headline.

Accounting (kt GOES, every cell a (low, high) range with an evidence type):
  sheet consumption S  = production P + sheet imports M - sheet exports X
  all-forms use     U  = S + GOES in imported cores + GOES in imported finished transformers
  domestic-origin   D  = P - domestic exports DX + R, where R is U.S. GOES that came back inside imported
                         cores/transformers (0 <= R <= domestic exports to Canada + Mexico)
  foreign share        = 1 - D / U

Re-exports (RX) are foreign steel passing through: M - RX is the foreign sheet that stays.
Production is identified only for 2017 and 2019 (Phase 0/1). Other years use a labelled model range:
from the lowest identified output (162 kt) to the stated ceiling (258.5 kt GOES-only to 2019, AK 2014;
226.8 kt all electrical steel from 2020, Cliffs). Inputs come from ``goes_research``.
"""
from __future__ import annotations

from radiant.data import goes_research as r

YEARS = range(2015, 2026)
P_MODEL_LOW = 162.0  # lowest identified production (2017), kt


def _production(year: int) -> tuple[tuple[float, float], str]:
    p0 = r.phase0_reconciliation()
    if year == 2019:
        return p0['implied_production_2019_kt'], 'estimate (Commerce percentages + trade)'
    if year == 2017:
        v = p0['implied_production_2017_kt']
        return (v, v), 'estimate (Commerce 37% share + trade)'
    cap = r.AK_2014_GOES_CAPACITY.value if year < 2020 else r.CLIFFS_ELECTRICAL_CAPACITY_2020.value
    return (P_MODEL_LOW, cap), 'model (lowest identified output to stated ceiling)'


def _transformers(year: int, emb: dict, units: dict) -> tuple[tuple[float, float], tuple[float, float]]:
    """GOES in imported LPTs and in imported distribution transformers (kt ranges)."""
    p3 = r.phase3_demand_comparison()
    lpt19, dt19 = p3['top_down_kt']['lpt_imported'], p3['top_down_kt']['dt_imported']
    f = emb[year]['lpt_goes_kt_lower_bound'] / emb[2019]['lpt_goes_kt_lower_bound']  # real-value index of 8504.23
    if year <= 2019:
        lpt = (lpt19[0] * f, lpt19[1] * f)
    else:
        # The 8504.23 mix shifted to smaller units after 2019, so neither units nor value scale cleanly.
        # Floor: real-value index on the 60 t/unit floor. Ceiling: DOE 900 LPTs/yr x 82% imported x 192 t.
        ceiling = r.DOE2024_LPT_DEMAND_2027.value * 0.82 * p3['goes_per_lpt_t'][1] / 1000
        lpt = (lpt19[0] * f, max(lpt19[0] * f, ceiling))
    u = units[year] / units[2019]  # measured DT import units (8504.21 + 8504.22)
    return lpt, (dt19[0] * u, dt19[1] * u)


def _dt_units() -> dict[int, float]:
    rows = r._partner_rows()
    return {y: r._sum(rows, ('850421', '850422'), y, 'M', 'qty') for y in YEARS}


def balance_sheet() -> list[dict]:
    """One row per year; every number is a (low, high) range in kt with its evidence type."""
    emb, rt, units = r.phase2_embodied(), r.phase2_round_trip(), _dt_units()
    rows = []
    for y in YEARS:
        m, x, rx = (r.comtrade_world_kt(y, f) for f in ('M', 'X', 'RX'))
        dx = rt[y]['DX']['kt'] or (x - rx)
        dx_na = rt[y]['DX']['to_canada_mexico_kt'] or 0.0
        p, p_type = _production(y)
        kind = 'estimate' if p_type.startswith('estimate') else 'model'
        s = (p[0] + m - x, p[1] + m - x)
        cores = emb[y]['cores_goes_kt_range']
        lpt, dt = _transformers(y, emb, units)
        use = (s[0] + cores[0] + lpt[0] + dt[0], s[1] + cores[1] + lpt[1] + dt[1])
        # Low foreign share: most domestic (max P, all U.S. steel sent to Canada/Mexico returns, min embodied).
        embodied_lo = cores[0] + lpt[0] + dt[0]
        back = min(dx_na, embodied_lo)          # returning U.S. steel, inside any embodied channel
        back_sc = min(dx_na, cores[0])          # sheet+cores view: it can only come back inside cores
        d_hi, d_lo = p[1] - dx + back, p[0] - dx
        f_lo, f_hi = (m - rx) + embodied_lo - back, (m - rx) + cores[1] + lpt[1] + dt[1]
        d_hi_sc = p[1] - dx + back_sc
        f_sc_lo, f_sc_hi = (m - rx) + cores[0] - back_sc, (m - rx) + cores[1]
        rows.append(dict(
            year=y,
            production=(p, p_type),
            sheet_imports=((m, m), 'measured (U.S.-reported via UN Comtrade)'),
            sheet_exports=((x, x), 'measured'), domestic_exports=((dx, dx), 'measured'),
            re_exports=((rx, rx), 'measured'),
            domestic_exports_to_canada_mexico=((dx_na, dx_na), 'measured' if rt[y]['DX']['share'] is not None else 'not reported'),
            sheet_consumption=(s, f'{kind} (identity)'),
            cores=(cores, 'estimate (Commerce 2019 anchor x real value index; secondhand anchor)'),
            lpt_imported=(lpt, 'estimate (DOE weights x Commerce/DOE units)'),
            dt_imported=(dt, 'estimate (2019 DT GOES x import share, scaled by measured units)'),
            all_forms_use=(use, kind),
            foreign_share_all_forms=((f_lo / (f_lo + d_hi), f_hi / (f_hi + d_lo)), kind),
            foreign_share_sheet_and_cores=((f_sc_lo / (f_sc_lo + d_hi_sc), f_sc_hi / (f_sc_hi + d_lo)), kind),
        ))
    return rows


def identity_checks() -> dict:
    """Plan Phase 5 identity tests, evaluated on the identified years."""
    rows = {row['year']: row for row in balance_sheet()}
    commerce_s = r.phase0_reconciliation()['sheet_consumption_2019_kt']
    s19 = rows[2019]['sheet_consumption'][0]
    return {
        'production_le_capacity': all(rows[y]['production'][0][1] <= r.AK_2014_GOES_CAPACITY.value for y in (2017, 2019)),
        # Balance closes: S from U.S.-reported trade vs S implied by Commerce's percentages (tolerance 3%).
        'balance_closes_2019': all(abs(a - b) / b < 0.03 for a, b in zip(s19, commerce_s)),
        'top_down_vs_bottom_up_overlap_2019': r.phase3_demand_comparison()['ranges_overlap'],
        'gap_explained': 'bottom-up omits 10-100 MVA transformers and non-transformer uses (residual 7-66 kt)',
    }


# --- Outlook 2026-2035 (all model) ---------------------------------------------------
NREL_GROWTH = (0.016, 0.034)        # DT capacity 160-260% of 2021 by 2050 -> compound annual growth
NLR_GRID_INCREMENT = (94.0, 114.0)  # kt/yr GOES for transmission build-out (NLR 2026), phased in 2026-2030
EFFICIENCY_RULE_SHIFT = 48.0        # kt/yr liquid-DT core steel moving GOES -> amorphous from 2029 (DOE 2024)
DLA_STOCKPILE = 53_000 * r.SHORT_TON_T / 1000 / 5  # kt/yr withheld 2025-2029 (stated ceiling)


def outlook(years=(2026, 2030, 2035)) -> dict:
    """Foreign share of all-forms GOES use under demand x domestic-supply scenarios.

    Demand: 2019 identified all-forms use grown at NREL's DT capacity growth (1.6-3.4%/yr from 2019), plus the
    NLR transmission increment phased in linearly to full by 2030, minus the DOE rule's amorphous shift from 2029
    on the low side. Domestic supply available to U.S. users:
      current   identified 2019 output, exports at the 2025 level
      expansion +25% at Butler by 2028 (Cliffs), capped at 226.8 kt, exports at the 2025 level
      diversion expansion with all exports kept at home (the old floor's optimistic assumption)
    The DLA stockpile is subtracted through 2029.
    """
    base = {row['year']: row for row in balance_sheet()}[2019]['all_forms_use'][0]
    p19 = r.phase0_reconciliation()['implied_production_2019_kt']
    p_mid = sum(p19) / 2
    dx25 = r.phase2_round_trip()[2025]['DX']['kt']
    cap = r.CLIFFS_ELECTRICAL_CAPACITY_2020.value
    out = {}
    for y in years:
        ramp = min(1.0, (y - 2025) / 5)
        dem = (base[0] * (1 + NREL_GROWTH[0]) ** (y - 2019) + NLR_GRID_INCREMENT[0] * ramp
               - (EFFICIENCY_RULE_SHIFT if y >= 2029 else 0.0),
               base[1] * (1 + NREL_GROWTH[1]) ** (y - 2019) + NLR_GRID_INCREMENT[1] * ramp)
        stock = DLA_STOCKPILE if y <= 2029 else 0.0
        expanded = min(cap, p_mid * (1 + r.CLIFFS_BUTLER_GOES_PLUS25.value)) if y >= 2028 else p_mid
        sup = {'current': p_mid - dx25 - stock, 'expansion': expanded - dx25 - stock, 'diversion': expanded - stock}
        out[y] = {k: {'demand_kt': dem, 'domestic_kt': d, 'foreign_share': (1 - d / dem[0], 1 - d / dem[1])}
                  for k, d in sup.items()}
        out[y]['evidence_type'] = 'model'
    return out


def headline() -> dict:
    rows = {row['year']: row for row in balance_sheet()}
    o = outlook()
    return {
        'foreign_share_2019_all_forms': rows[2019]['foreign_share_all_forms'][0],
        'foreign_share_2019_sheet_and_cores': rows[2019]['foreign_share_sheet_and_cores'][0],
        'all_forms_use_2019_kt': rows[2019]['all_forms_use'][0],
        'foreign_share_2025_all_forms_model': rows[2025]['foreign_share_all_forms'][0],
        'foreign_share_2035_min_across_scenarios': min(o[2035][k]['foreign_share'][0] for k in ('current', 'expansion', 'diversion')),
        'foreign_share_min_2026_2035_any_scenario': min(o[y][k]['foreign_share'][0] for y in o for k in ('current', 'expansion', 'diversion')),
        'withdrawn': 'Run 053 headline (33% in 2019 -> at least 41-44%): the 288 kt base double counted 68 kt of cores, '
                     'sheet imports were not netted for re-exports, and finished-transformer imports were omitted.',
        'key_driver': 'GOES inside imported finished transformers and cores, not sheet imports',
    }
