"""Uncertainty-aware constraint resolution and measurement prioritization.

Scenario distributions are epistemic inputs, never silently promoted to evidence. The
purpose is to ask which conclusions are robust and which unknown parameter should be
measured next.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from collections import Counter
from typing import Mapping
import numpy as np
from radiant.engines.constraint_resolution import ProductionSystem, maximize_throughput

@dataclass(frozen=True)
class Interval:
    low: float
    high: float
    provenance: str = "scenario"
    def __post_init__(self):
        if self.low < 0 or self.high < self.low: raise ValueError("invalid interval")

@dataclass
class EnsembleResult:
    n: int
    throughput_q05: float
    throughput_median: float
    throughput_q95: float
    top_intervention_probability: dict[str,float]
    positive_gain_probability: dict[str,float]
    expected_gain: dict[str,float]
    measurement_priority: list[dict]


def _draw_system(base: ProductionSystem, cap: Mapping[str,Interval], imp: Mapping[str,Interval], rng):
    ps=[]
    for p in base.processes:
        iv=cap.get(p.id)
        ps.append(replace(p,capacity=float(rng.uniform(iv.low,iv.high))) if iv else p)
    ims=dict(base.import_limits)
    for x,iv in imp.items(): ims[x]=float(rng.uniform(iv.low,iv.high))
    return replace(base,processes=tuple(ps),import_limits=ims)


def _gain(s: ProductionSystem, key: str, fraction: float) -> float:
    b=maximize_throughput(s).throughput
    kind,name=key.split(':',1)
    if kind=='capacity':
        ps=list(s.processes)
        for i,p in enumerate(ps):
            if p.id==name: ps[i]=replace(p,capacity=p.capacity*(1+fraction)); break
        r=maximize_throughput(replace(s,processes=tuple(ps))).throughput
    else:
        im=dict(s.import_limits); im[name]*=(1+fraction)
        r=maximize_throughput(replace(s,import_limits=im)).throughput
    return r-b


def uncertainty_scan(base: ProductionSystem, capacity_intervals: Mapping[str,Interval],
                     import_intervals: Mapping[str,Interval], n: int=1000,
                     fraction: float=.20, seed: int=0) -> EnsembleResult:
    rng=np.random.default_rng(seed)
    keys=[f'capacity:{p.id}' for p in base.processes if p.id in capacity_intervals]
    keys += [f'import:{x}' for x in import_intervals]
    through=[]; gains={k:[] for k in keys}; winners=[]; samples={k:[] for k in list(capacity_intervals)+list(import_intervals)}
    for _ in range(n):
        s=_draw_system(base,capacity_intervals,import_intervals,rng)
        through.append(maximize_throughput(s).throughput)
        for p in s.processes:
            if p.id in capacity_intervals: samples[p.id].append(p.capacity)
        for x in import_intervals: samples[x].append(s.import_limits[x])
        gs={k:_gain(s,k,fraction) for k in keys}
        for k,v in gs.items(): gains[k].append(v)
        m=max(gs.values()) if gs else 0
        if m>1e-12:
            tied=sorted(k for k,v in gs.items() if abs(v-m)<1e-10)
            winners.extend(tied)
    top={k:winners.count(k)/max(1,len(winners)) for k in keys}
    pos={k:float(np.mean(np.asarray(v)>1e-12)) for k,v in gains.items()}
    exp={k:float(np.mean(v)) for k,v in gains.items()}
    # Measurement priority: absolute Spearman-like rank correlation with baseline throughput.
    # High value means uncertainty in this parameter strongly controls the answer.
    y=np.asarray(through); yr=np.argsort(np.argsort(y)).astype(float)
    priority=[]
    for name,vals in samples.items():
        x=np.asarray(vals); xr=np.argsort(np.argsort(x)).astype(float)
        corr=float(np.corrcoef(xr,yr)[0,1]) if np.std(xr)>0 and np.std(yr)>0 else 0.0
        priority.append({'parameter':name,'abs_rank_correlation':abs(corr),'rank_correlation':corr})
    priority.sort(key=lambda z:-z['abs_rank_correlation'])
    q=np.quantile(y,[.05,.5,.95])
    return EnsembleResult(n,float(q[0]),float(q[1]),float(q[2]),top,pos,exp,priority)
