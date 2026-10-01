"""Load annual GOES trade written by scripts/fetch_goes_trade.py (fail closed).

A year is usable only if BOTH HS6 headings (722511, 722611) returned rows in kilograms
for that direction. HS10 rows, when complete, must sum to the HS6 total within 2%;
otherwise the year is flagged rather than silently accepted.
"""
from __future__ import annotations
import csv
from pathlib import Path

DEFAULT_PATH = Path('data/goes/goes_trade_annual.csv')
HS6 = ('722511', '722611')
KG_UNITS = {'KG', 'KGS', 'KILOGRAMS'}


def load_annual_goes_trade(path: str | Path = DEFAULT_PATH) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    rows = list(csv.DictReader(p.open()))
    years = sorted({int(r['year']) for r in rows})
    out = {}
    for y in years:
        for d in ('imports', 'exports'):
            yr = [r for r in rows if int(r['year']) == y and r['direction'] == d]
            h6 = {r['code']: r for r in yr if r['level'] == 'HS6'}
            ok6 = all(c in h6 and h6[c]['status'] == 'ok' and h6[c]['unit'].upper() in KG_UNITS for c in HS6)
            entry = {'complete': ok6, 'tonnes': None, 'hs10_check': 'not_available', 'source_urls': [h6[c]['source_url'] for c in HS6 if c in h6]}
            if ok6:
                t6 = sum(float(h6[c]['quantity']) for c in HS6) / 1000.0
                entry['tonnes'] = t6
                h10 = [r for r in yr if r['level'] == 'HS10']
                if h10 and all(r['status'] == 'ok' for r in h10):
                    t10 = sum(float(r['quantity']) for r in h10 if r['unit'].upper() in KG_UNITS) / 1000.0
                    entry['hs10_check'] = 'match' if t6 == 0 or abs(t10 - t6) / t6 <= 0.02 else f'mismatch hs10={t10:.0f}t'
                elif h10:
                    entry['hs10_check'] = 'hs10_incomplete_for_year (codes may differ by period)'
            out.setdefault(y, {})[d] = entry
    return out


def latest_complete_imports(trade: dict | None) -> tuple[int, float] | None:
    if not trade:
        return None
    ys = [y for y, v in trade.items() if v.get('imports', {}).get('complete')]
    if not ys:
        return None
    y = max(ys)
    return y, trade[y]['imports']['tonnes']
