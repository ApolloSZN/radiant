#!/usr/bin/env python3
"""Print the Phase 5 balance sheet and outlook as Markdown tables (the chart's table view)."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from radiant.data import goes_balance as b  # noqa: E402


def kt(v):
    lo, hi = v
    return f'{lo:.0f}' if abs(hi - lo) < 0.5 else f'{lo:.0f}–{hi:.0f}'


def pc(v):
    return f'{v[0]:.0%}–{v[1]:.0%}'


def main() -> int:
    print('| Year | Production | Sheet imports | Re-exports | Domestic exports (to CA+MX) | Sheet use | GOES in cores | in imported LPTs | in imported DTs | All-forms use | Foreign share, all forms | Foreign share, sheet+cores | Type |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in b.balance_sheet():
        print(f"| {r['year']} | {kt(r['production'][0])} | {kt(r['sheet_imports'][0])} | {kt(r['re_exports'][0])} | "
              f"{kt(r['domestic_exports'][0])} ({kt(r['domestic_exports_to_canada_mexico'][0]) if r['domestic_exports_to_canada_mexico'][1] == 'measured' else 'n/a'}) | {kt(r['sheet_consumption'][0])} | "
              f"{kt(r['cores'][0])} | {kt(r['lpt_imported'][0])} | {kt(r['dt_imported'][0])} | {kt(r['all_forms_use'][0])} | "
              f"{pc(r['foreign_share_all_forms'][0])} | {pc(r['foreign_share_sheet_and_cores'][0])} | {r['foreign_share_all_forms'][1]} |")
    print('\n| Year | Demand (kt) | No change: domestic kt / foreign share | Expansion | Best case (expansion + no exports) |')
    print('|---|---|---|---|---|')
    for y, d in b.outlook().items():
        cells = ' | '.join(f"{d[k]['domestic_kt']:.0f} / {pc(d[k]['foreign_share'])}" for k in ('current', 'expansion', 'diversion'))
        print(f"| {y} | {kt(d['current']['demand_kt'])} | {cells} |")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
