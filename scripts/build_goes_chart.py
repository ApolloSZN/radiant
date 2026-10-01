#!/usr/bin/env python3
"""Render docs/figures/goes_foreign_share.svg from radiant.data.goes_balance (no plotting libraries).

One y-axis: foreign share of U.S. GOES use, all forms (sheet + cores + finished transformers), 2015-2035.
History is a range band (model years lighter, identified years 2017/2019 as whiskers); projections are
scenario bands. Palette: dataviz reference slots 1-3, validated light and dark (all-pairs).
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from radiant.data import goes_balance as b  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / 'docs/figures/goes_foreign_share.svg'
W, H = 760, 470
L, R, T, B = 64, 190, 70, 86
X0, X1 = 2015, 2035


def x(year: float) -> float:
    return L + (year - X0) / (X1 - X0) * (W - L - R)


def y(share: float) -> float:
    return T + (1 - share) * (H - T - B)


def band(points: list[tuple[int, float, float]], cls: str) -> str:
    top = ' '.join(f'{x(t):.1f},{y(hi):.1f}' for t, lo, hi in points)
    bot = ' '.join(f'{x(t):.1f},{y(lo):.1f}' for t, lo, hi in reversed(points))
    edge_hi = ' '.join(f'{x(t):.1f},{y(hi):.1f}' for t, lo, hi in points)
    edge_lo = ' '.join(f'{x(t):.1f},{y(lo):.1f}' for t, lo, hi in points)
    return (f'<polygon class="{cls} fill" points="{top} {bot}"/>'
            f'<polyline class="{cls} edge" points="{edge_hi}"/><polyline class="{cls} edge" points="{edge_lo}"/>')


def main() -> int:
    rows = {r['year']: r for r in b.balance_sheet()}
    hist = [(yr, *rows[yr]['foreign_share_all_forms'][0]) for yr in sorted(rows)]
    o = b.outlook()
    yrs = sorted(o)
    anchor = rows[2025]['foreign_share_all_forms'][0]
    cur = [(2025, *anchor)] + [(yr, *o[yr]['current']['foreign_share']) for yr in yrs]
    best = [(2025, *anchor)] + [(yr, *o[yr]['diversion']['foreign_share']) for yr in yrs]
    p = []
    p.append('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 470" role="img" aria-labelledby="t d" font-family="system-ui,-apple-system,Segoe UI,sans-serif">
<title id="t">Foreign share of U.S. GOES use, all forms, 2015-2035</title>
<desc id="d">Range bands. History 2015-2025 (identified years 2017 and 2019 shown as whiskers, other years are model ranges); projections to 2035 for no change and best case. The withdrawn Run 053 figure of 33 percent is shown dashed.</desc>
<style>
svg{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--grid:#e4e3df;--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a}
@media (prefers-color-scheme: dark){svg{--surface:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#8f8e86;--grid:#33332f;--s1:#3987e5;--s2:#d95926;--s3:#199e70}}
.bg{fill:var(--surface)} text{fill:var(--ink2);font-size:12px} .title{fill:var(--ink);font-size:15px;font-weight:600}
.grid{stroke:var(--grid);stroke-width:1} .fill{stroke:none} .edge{fill:none;stroke-width:2}
.hist.fill{fill:var(--s1);opacity:.18} .hist.edge{stroke:var(--s1)} .cur.fill{fill:var(--s2);opacity:.18} .cur.edge{stroke:var(--s2)}
.best.fill{fill:var(--s3);opacity:.18} .best.edge{stroke:var(--s3)} .wh{stroke:var(--s1);stroke-width:2} .dot{fill:var(--s1);stroke:var(--surface);stroke-width:2}
.old{stroke:var(--muted);stroke-width:2;stroke-dasharray:5 4} .lab{fill:var(--ink);font-size:12px} .sw1{fill:var(--s1)} .sw2{fill:var(--s2)} .sw3{fill:var(--s3)}
</style>
<rect class="bg" width="760" height="470"/>
<text class="title" x="64" y="26">Foreign share of U.S. GOES use, all forms, 2015–2035</text>
<text x="64" y="44">Sheet + GOES inside imported cores and finished transformers. Bands are ranges, not confidence intervals.</text>''')
    for s in (0, .25, .5, .75, 1.0):
        p.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(s):.1f}" y2="{y(s):.1f}"/>'
                 f'<text x="{L - 8}" y="{y(s) + 4:.1f}" text-anchor="end">{s:.0%}</text>')
    for yr in (2015, 2019, 2025, 2030, 2035):
        p.append(f'<text x="{x(yr):.1f}" y="{H - B + 18}" text-anchor="middle">{yr}</text>')
    p.append(f'<line class="grid" x1="{x(2025):.1f}" x2="{x(2025):.1f}" y1="{T}" y2="{H - B}"/>'
             f'<text x="{x(2025) + 6:.1f}" y="{T + 12}">projection →</text>')
    p.append(band(hist, 'hist'))
    p.append(band(cur, 'cur'))
    p.append(band(best, 'best'))
    for yr in (2017, 2019):  # identified years: whisker + marker
        lo, hi = rows[yr]['foreign_share_all_forms'][0]
        p.append(f'<line class="wh" x1="{x(yr):.1f}" x2="{x(yr):.1f}" y1="{y(hi):.1f}" y2="{y(lo):.1f}"/>'
                 f'<circle class="dot" cx="{x(yr):.1f}" cy="{y((lo + hi) / 2):.1f}" r="5"/>')
    lo19, hi19 = rows[2019]['foreign_share_all_forms'][0]
    p.append(f'<text class="lab" x="{x(2019):.1f}" y="{y(.92):.1f}" text-anchor="middle">2019 (identified): {lo19:.0%}–{hi19:.0%}</text>')
    p.append(f'<line class="old" x1="{x(2015):.1f}" x2="{x(2025):.1f}" y1="{y(.33):.1f}" y2="{y(.33):.1f}"/>'
             f'<text x="{x(2015) + 4:.1f}" y="{y(.33) + 16:.1f}">Withdrawn Run 053: 33%</text>')
    for pts, cls, name in ((cur, 'cur', 'No change'), (best, 'best', 'Best case*')):
        lo, hi = pts[-1][1:]
        p.append(f'<text class="lab" x="{x(2035) + 8:.1f}" y="{y((lo + hi) / 2) + 4:.1f}">{name} {lo:.0%}–{hi:.0%}</text>')
    lx = L
    for i, name in ((1, 'History'), (2, 'No change'), (3, 'Best case*')):
        p.append(f'<rect class="sw{i}" x="{lx}" y="{H - 50}" width="12" height="12" rx="2"/><text x="{lx + 18}" y="{H - 40}">{name}</text>')
        lx += 120
    p.append(f'<text x="{L}" y="{H - 16}">*Butler +25% by 2028, no GOES exported. Whiskers = identified years. Source: radiant.data.goes_balance</text>')
    p.append('</svg>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(p) + '\n')
    print(f'wrote {OUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
