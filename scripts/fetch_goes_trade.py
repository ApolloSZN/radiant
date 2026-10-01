#!/usr/bin/env python3
"""Download annual U.S. GOES trade from the Census International Trade API.

Run where api.census.gov is reachable (your laptop, Claude Code, GitHub Actions):

    python scripts/fetch_goes_trade.py            # 2019..last full year
    python scripts/fetch_goes_trade.py 2019 2025
    CENSUS_API_KEY=... python scripts/fetch_goes_trade.py   # key optional for this volume

Writes data/goes/goes_trade_annual.csv. Uses December year-to-date values (= full
calendar year). Pulls HS6 totals (722511 + 722611) as the primary series and the sourced U.S.
HTS10 GOES decomposition as a cross-check. Historical classification continuity is
not assumed: the output records the requested codes and the loader fails closed on
missing/mismatched rows. Imports use *imports for consumption* (CON_*), not general
imports (GEN_*), matching the material-balance question.
Only the standard library is used.
"""
from __future__ import annotations
import csv, datetime as dt, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

BASE = 'https://api.census.gov/data/timeseries/intltrade'
HS6 = ('722511', '722611')
# Commerce GOES investigation scope (primary-source mapping; see goes_import_floor.py).
IMPORT_HS10 = ('7225110000', '7226111000', '7226119030', '7226119060')
EXPORT_HS10 = ('7225110000', '7226110000')
OUT = Path(__file__).resolve().parents[1] / 'data/goes/goes_trade_annual.csv'
FIELDS = ['year', 'direction', 'level', 'code', 'quantity', 'unit', 'value_usd', 'status', 'source_url', 'retrieved_at']


def _get(direction: str, year: int, code: str, level: str) -> tuple[list[list[str]] | None, str]:
    if direction == 'imports':
        fields = 'I_COMMODITY,CTY_CODE,CTY_NAME,CON_QY1_YR,UNIT_QY1,CON_VAL_YR'
        params = {'get': fields, 'time': f'{year}-12', 'COMM_LVL': level, 'I_COMMODITY': code}
    else:
        fields = 'E_COMMODITY,CTY_CODE,CTY_NAME,QTY_1_YR,UNIT_QY1,ALL_VAL_YR'
        params = {'get': fields, 'time': f'{year}-12', 'COMM_LVL': level, 'E_COMMODITY': code}
    if os.environ.get('CENSUS_API_KEY'):
        params['key'] = os.environ['CENSUS_API_KEY']
    url = f'{BASE}/{direction}/hs?' + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                body = r.read().decode()
            if not body.strip():
                return None, url  # Census returns 204/empty when no rows exist
            return json.loads(body), url
        except urllib.error.HTTPError as e:
            if e.code == 204:
                return None, url
            if attempt == 2:
                raise
        except Exception:
            if attempt == 2:
                raise
        time.sleep(2 * (attempt + 1))
    return None, url


def _world_total(rows: list[list[str]]) -> tuple[float, str, float]:
    head, data = rows[0], rows[1:]
    ix = {h: i for i, h in enumerate(head)}
    qcol = 'CON_QY1_YR' if 'CON_QY1_YR' in ix else 'QTY_1_YR'
    vcol = 'CON_VAL_YR' if 'CON_VAL_YR' in ix else 'ALL_VAL_YR'
    total = [r for r in data if 'TOTAL FOR ALL COUNTRIES' in (r[ix['CTY_NAME']] or '').upper()]
    use = total if total else [r for r in data if (r[ix['CTY_CODE']] or '').isdigit() and not r[ix['CTY_CODE']].startswith('00')]
    q = sum(float(r[ix[qcol]] or 0) for r in use)
    v = sum(float(r[ix[vcol]] or 0) for r in use)
    unit = use[0][ix['UNIT_QY1']] if use else ''
    return q, unit, v


def main(argv: list[str]) -> int:
    today = dt.date.today()
    y0 = int(argv[1]) if len(argv) > 1 else 2019
    y1 = int(argv[2]) if len(argv) > 2 else today.year - 1
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    out_rows = []
    jobs = []
    for y in range(y0, y1 + 1):
        for d in ('imports', 'exports'):
            jobs += [(y, d, 'HS6', c) for c in HS6]
            jobs += [(y, d, 'HS10', c) for c in (IMPORT_HS10 if d == 'imports' else EXPORT_HS10)]
    for y, d, lvl, c in jobs:
        try:
            rows, url = _get(d, y, c, lvl)
        except Exception as e:  # record, never crash the whole pull
            out_rows.append(dict(year=y, direction=d, level=lvl, code=c, quantity='', unit='', value_usd='',
                                 status=f'error:{type(e).__name__}:{str(e)[:80]}', source_url='', retrieved_at=stamp))
            print(f'{y} {d} {lvl} {c}: ERROR {e}')
            continue
        if rows is None:
            out_rows.append(dict(year=y, direction=d, level=lvl, code=c, quantity='', unit='', value_usd='',
                                 status='no_rows_returned', source_url=url.split('&key=')[0], retrieved_at=stamp))
            continue
        q, unit, v = _world_total(rows)
        out_rows.append(dict(year=y, direction=d, level=lvl, code=c, quantity=q, unit=unit, value_usd=v,
                             status='ok', source_url=url.split('&key=')[0], retrieved_at=stamp))
        print(f'{y} {d:7s} {lvl:4s} {c}: {q:,.0f} {unit}')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(out_rows)
    print(f'wrote {OUT} ({len(out_rows)} rows)')
    bad = [r for r in out_rows if r['level'] == 'HS6' and r['status'] != 'ok']
    if bad:
        print(f'FAIL-CLOSED: {len(bad)} required HS6 rows were not retrieved successfully', file=sys.stderr)
        for r in bad[:12]:
            print(f"  {r['year']} {r['direction']} {r['code']}: {r['status']}", file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
