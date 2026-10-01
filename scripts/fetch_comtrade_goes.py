#!/usr/bin/env python3
"""Download U.S. GOES-related trade by partner from the UN Comtrade public preview API (no key).

    python scripts/fetch_comtrade_goes.py            # 2015..2025
    python scripts/fetch_comtrade_goes.py 2019 2019

UN Comtrade republishes the U.S. Census annual series reported by the United States (reporter 842).
Unlike the Census API (key required since 2026), it is keyless and splits exports into domestic
exports (DX) and re-exports of foreign goods (RX). Flows: M = imports, X = total exports.
HS6 only. Comtrade flags weights it estimated (net_kg_estimated); keep that flag when using kg.

Writes data/goes/research/comtrade_us_goes_forms.csv. Standard library only.
"""
from __future__ import annotations
import csv, datetime as dt, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

BASE = 'https://comtradeapi.un.org/public/v1/preview/C/A/HS'
PARTNERS_URL = 'https://comtradeapi.un.org/files/v1/app/reference/partnerAreas.json'
GROUPS = {
    'goes_sheet': ('722511', '722611'),
    'transformer_parts': ('850490',),  # includes laminations and cores, but also other parts
    'transformers': ('850421', '850422', '850423', '850432', '850433', '850434'),
}
FLOWS = ('M', 'X', 'DX', 'RX')
OUT = Path(__file__).resolve().parents[1] / 'data/goes/research/comtrade_us_goes_forms.csv'
FIELDS = ['year', 'flow', 'hs6', 'partner_code', 'partner', 'net_kg', 'net_kg_estimated', 'qty', 'qty_unit',
          'qty_estimated', 'value_usd', 'source_url', 'retrieved_at']


def _json(url: str) -> dict:
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.loads(r.read().decode())
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    return {}


def _partners() -> dict[int, str]:
    d = _json(PARTNERS_URL)
    return {int(r['id']): r['text'] for r in d.get('results', []) if str(r.get('id', '')).lstrip('-').isdigit()}


def _fetch(year: int, flow: str, codes: tuple[str, ...]) -> tuple[list[dict], str]:
    params = dict(reporterCode=842, period=year, cmdCode=','.join(codes), flowCode=flow,
                  motCode=0, customsCode='C00', partner2Code=0)
    url = f'{BASE}?' + urllib.parse.urlencode(params)
    d = _json(url)
    if d.get('error'):
        raise RuntimeError(d['error'])
    if d.get('count', 0) >= 500 and len(codes) > 1:  # preview cap: split the request
        rows = []
        for c in codes:
            rows += _fetch(year, flow, (c,))[0]
        return rows, url
    return d.get('data') or [], url


def main(argv: list[str]) -> int:
    y0 = int(argv[1]) if len(argv) > 1 else 2015
    y1 = int(argv[2]) if len(argv) > 2 else 2025
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    names = _partners()
    out, failures = [], []
    for y in range(y0, y1 + 1):
        for flow in FLOWS:
            for group, codes in GROUPS.items():
                try:
                    rows, url = _fetch(y, flow, codes)
                except Exception as e:  # record, keep going
                    failures.append(f'{y} {flow} {group}: {type(e).__name__}: {str(e)[:80]}')
                    continue
                for r in rows:
                    pc = int(r['partnerCode'])
                    out.append(dict(year=y, flow=flow, hs6=r['cmdCode'], partner_code=pc,
                                    partner='World' if pc == 0 else names.get(pc, str(pc)),
                                    net_kg=r.get('netWgt') if r.get('netWgt') is not None else '',
                                    net_kg_estimated=r.get('isNetWgtEstimated'),
                                    qty=r.get('qty') if r.get('qty') is not None else '',
                                    qty_unit=r.get('qtyUnitAbbr') or r.get('qtyUnitCode') or '',
                                    qty_estimated=r.get('isQtyEstimated'),
                                    value_usd=r.get('primaryValue'), source_url=url, retrieved_at=stamp))
                print(f'{y} {flow:2s} {group}: {len(rows)} rows')
                time.sleep(1.5)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(out)
    print(f'wrote {OUT} ({len(out)} rows)')
    for msg in failures:
        print('FAILED', msg, file=sys.stderr)
    return 2 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
