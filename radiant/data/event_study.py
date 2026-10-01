"""Minimal falsifiable event-study primitives for future transformer plant/order panels.

No transformer causal effect is claimed until real outcome panels satisfy these contracts.
The implementation exists now so future evidence is evaluated against predeclared checks
rather than a post-hoc estimator chosen after outcomes are seen.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class EventStudyResult:
    pretrend_slope_gap: float
    pretrend_pass: bool
    did_effect: float
    placebo_effect: float
    placebo_pass: bool
    identified: bool


def _slope(t, y):
    if len(t)<2: return float('nan')
    return float(np.polyfit(np.asarray(t,float),np.asarray(y,float),1)[0])


def evaluate_panel(rows, *, pretrend_tolerance:float, placebo_tolerance:float):
    """rows: dicts with group in {treated,control}, rel_time int, outcome float.

    DID compares mean post (rel_time>=0) vs pre (rel_time<0). Pretrend compares
    group slopes using pre-treatment observations. Placebo uses the last pre period
    as a fake intervention and earlier pre observations as placebo baseline.
    """
    tr=[r for r in rows if r['group']=='treated']; co=[r for r in rows if r['group']=='control']
    if not tr or not co: raise ValueError('need treated and control rows')
    tp=[r for r in tr if r['rel_time']<0]; cp=[r for r in co if r['rel_time']<0]
    if len(tp)<3 or len(cp)<3: raise ValueError('need >=3 pre observations per group')
    gap=_slope([r['rel_time'] for r in tp],[r['outcome'] for r in tp])-_slope([r['rel_time'] for r in cp],[r['outcome'] for r in cp])
    pre_ok=abs(gap)<=pretrend_tolerance
    def mean(xs): return float(np.mean(xs))
    tr_pre=mean([r['outcome'] for r in tp]); co_pre=mean([r['outcome'] for r in cp])
    tr_post=mean([r['outcome'] for r in tr if r['rel_time']>=0]); co_post=mean([r['outcome'] for r in co if r['rel_time']>=0])
    did=(tr_post-tr_pre)-(co_post-co_pre)
    cutoff=max(r['rel_time'] for r in tp)
    te=[r for r in tp if r['rel_time']==cutoff]; ce=[r for r in cp if r['rel_time']==cutoff]
    tb=[r for r in tp if r['rel_time']<cutoff]; cb=[r for r in cp if r['rel_time']<cutoff]
    placebo=(mean([r['outcome'] for r in te])-mean([r['outcome'] for r in tb]))-(mean([r['outcome'] for r in ce])-mean([r['outcome'] for r in cb]))
    pl_ok=abs(placebo)<=placebo_tolerance
    return EventStudyResult(gap,pre_ok,did,placebo,pl_ok,pre_ok and pl_ok)
