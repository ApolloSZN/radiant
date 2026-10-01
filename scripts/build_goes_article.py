#!/usr/bin/env python3
"""Render the Phase 6 article and methods note from templates; every number comes from the code.

    python scripts/build_goes_article.py           # write docs/article/*.md
    python scripts/build_goes_article.py --check   # exit 1 if the rendered files are stale
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from radiant.data import goes_balance as b, goes_research as g  # noqa: E402

PAIRS = {'article.template.md': 'americas-hidden-transformer-steel-dependence.md', 'methods.template.md': 'methods.md'}


def _r(t, fmt='{:.0f}', sep='–'):
    return fmt.format(t[0]) + sep + fmt.format(t[1])


def _p(t):
    return f'{t[0]:.0%}'.rstrip('%') + '–' + f'{t[1]:.0%}'


def values() -> dict[str, str]:
    rows = {r['year']: r for r in b.balance_sheet()}
    h, o = b.headline(), b.outlook()
    p0, rt, emb = g.phase0_reconciliation(), g.phase2_round_trip(), g.phase2_embodied()
    prices = g.phase4_prices()
    r19 = rows[2019]
    na = [rt[y]['DX']['share'] for y in range(2021, 2026)]
    trans19 = (r19['lpt_imported'][0][0] + r19['dt_imported'][0][0], r19['lpt_imported'][0][1] + r19['dt_imported'][0][1])
    units = b._dt_units()
    return {
        'use19': _r(h['all_forms_use_2019_kt']), 'f19': _p(h['foreign_share_2019_all_forms']),
        'sc19': _p(h['foreign_share_2019_sheet_and_cores']), 'f19lo': f"{h['foreign_share_2019_all_forms'][0]:.0%}", 'prod19': _r(p0['implied_production_2019_kt']),
        'prod17': f"{p0['implied_production_2017_kt']:.0f}", 'cap': f'{g.CLIFFS_ELECTRICAL_CAPACITY_2020.value:.0f}',
        'ak14': f'{g.AK_2014_GOES_CAPACITY.value:.0f}', 'sheet19': _r(r19['sheet_consumption'][0]),
        'allsc19': _r(p0['all_forms_consumption_2019_kt']), 'doublecount': f"{p0['double_count_in_288kt_kt']:.0f}",
        'm19': f"{g.comtrade_world_kt(2019, 'M'):.1f}", 'x19': f"{p0['exports_2019_kt']['total']:.1f}",
        'rx19': f"{p0['exports_2019_kt']['re_exports']:.1f}", 'dx19': f"{p0['exports_2019_kt']['domestic']:.1f}",
        'kept19': f"{p0['foreign_sheet_retained_2019_kt']:.0f}",
        'lpt19': _r(r19['lpt_imported'][0]), 'dt19': _r(r19['dt_imported'][0]), 'trans19': _r(trans19),
        'na19': f"{rt[2019]['DX']['share']:.0%}", 'na_recent': f'{min(na):.0%}'.rstrip('%') + '–' + f'{max(na):.0%}',
        'cores25': f"{emb[2025]['cores_goes_kt_index']:.0f}",
        'xv19': f"{emb[2019]['transformers_value_musd'] / 1000:.1f}", 'xv25': f"{emb[2025]['transformers_value_musd'] / 1000:.1f}",
        'dtu19': f'{units[2019] / 1000:.0f},000', 'dtu25': f'{units[2025] / 1000:.0f},000',
        'ppi_up': f"{prices[2025]['transformer_ppi'] / prices[2019]['transformer_ppi'] - 1:.0%}",
        'pg19': f"{prices[2019]['goes_import_usd_per_kg']:.2f}", 'pg23': f"{prices[2023]['goes_import_usd_per_kg']:.2f}",
        'f25': _p(rows[2025]['foreign_share_all_forms'][0]),
        'nochange35': _p(o[2035]['current']['foreign_share']), 'best35': _p(o[2035]['diversion']['foreign_share']),
        'minall': f"{h['foreign_share_min_2026_2035_any_scenario']:.0%}", 'dem35': _r(o[2035]['current']['demand_kt']),
        'dom_cur': f"{o[2035]['current']['domestic_kt']:.0f}", 'dom_best': f"{o[2035]['diversion']['domestic_kt']:.0f}",
        'n_exp': str(len(g.TRANSFORMER_EXPANSIONS)),
        'exp_usd': f"{sum(e['usd_m'] or 0 for e in g.TRANSFORMER_EXPANSIONS) / 1000:.2f}",
    }


def render() -> dict[Path, str]:
    v = values()
    return {ROOT / 'docs/article' / out: (ROOT / 'docs/article' / tpl).read_text().format(**v) for tpl, out in PAIRS.items()}


def main(argv: list[str]) -> int:
    out = render()
    if '--check' in argv:
        stale = [p.name for p, text in out.items() if not p.exists() or p.read_text() != text]
        print('stale: ' + ', '.join(stale) if stale else 'up to date')
        return 1 if stale else 0
    for p, text in out.items():
        p.write_text(text)
        print(f'wrote {p} ({len(text.split())} words)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
