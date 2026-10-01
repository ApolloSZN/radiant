"""Partial identification for constraint-resolution claims.

A conclusion is certified only when it survives every admissible parameter scenario
provided by the caller. This is deliberately stronger than Monte Carlo frequency:
no probability distribution is invented when only bounds are evidence-backed.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from itertools import product
from typing import Mapping
from radiant.engines.constraint_resolution import ProductionSystem, maximize_throughput
from radiant.engines.uncertain_constraints import Interval, _gain

@dataclass(frozen=True)
class RobustInterventionResult:
    intervention: str
    min_gain: float
    max_gain: float
    robust_positive: bool
    robust_best: bool

@dataclass(frozen=True)
class PartialIdentificationResult:
    scenarios: int
    throughput_low: float
    throughput_high: float
    interventions: tuple[RobustInterventionResult, ...]
    identified_best: str | None


def _corner_systems(base: ProductionSystem, caps: Mapping[str, Interval], imports: Mapping[str, Interval]):
    names=[('capacity',k) for k in sorted(caps)] + [('import',k) for k in sorted(imports)]
    if len(names)>16:
        raise ValueError('corner enumeration capped at 16 uncertain parameters')
    for bits in product((0,1), repeat=len(names)):
        ps=list(base.processes); im=dict(base.import_limits)
        for bit,(kind,name) in zip(bits,names):
            iv=caps[name] if kind=='capacity' else imports[name]
            val=iv.high if bit else iv.low
            if kind=='capacity':
                for i,p in enumerate(ps):
                    if p.id==name: ps[i]=replace(p,capacity=val); break
            else: im[name]=val
        yield replace(base,processes=tuple(ps),import_limits=im)


def partial_identification(base: ProductionSystem, caps: Mapping[str, Interval], imports: Mapping[str, Interval], fraction=.20):
    keys=[f'capacity:{k}' for k in sorted(caps)] + [f'import:{k}' for k in sorted(imports)]
    mins={k:float('inf') for k in keys}; maxs={k:float('-inf') for k in keys}; always_best={k:True for k in keys}
    tlo=float('inf'); thi=float('-inf'); n=0
    for s in _corner_systems(base,caps,imports):
        n+=1; t=maximize_throughput(s).throughput; tlo=min(tlo,t); thi=max(thi,t)
        gs={k:_gain(s,k,fraction) for k in keys}; best=max(gs.values()) if gs else 0.0
        for k,g in gs.items():
            mins[k]=min(mins[k],g); maxs[k]=max(maxs[k],g)
            if g < best-1e-10: always_best[k]=False
    rows=tuple(RobustInterventionResult(k,mins[k],maxs[k],mins[k]>1e-12,always_best[k]) for k in keys)
    rb=[r.intervention for r in rows if r.robust_best]
    return PartialIdentificationResult(n,tlo,thi,rows,rb[0] if len(rb)==1 else None)

# Generic evidence-bound propagation. These bounds are epistemic, not distributions.
from math import inf, isfinite
@dataclass(frozen=True)
class Bound:
    low: float = 0.0
    high: float = inf
    evidence: str = 'unknown'
    def __post_init__(self):
        if self.low < 0 or self.high < self.low: raise ValueError('invalid nonnegative bound')
    @property
    def point_identified(self): return self.low == self.high and isfinite(self.high)

@dataclass(frozen=True)
class ThroughputBound:
    low: float; high: float; binding_low: tuple[str,...]; binding_high: tuple[str,...]; identified: bool

def serial_throughput(stage_capacities: Mapping[str, Bound]) -> ThroughputBound:
    if not stage_capacities: return ThroughputBound(0.0,inf,(),(),False)
    lo=min(b.low for b in stage_capacities.values()); hi=min(b.high for b in stage_capacities.values())
    return ThroughputBound(lo,hi,tuple(sorted(k for k,b in stage_capacities.items() if b.low==lo)),
                           tuple(sorted(k for k,b in stage_capacities.items() if b.high==hi)),
                           lo==hi and isfinite(hi))

def knockout_bound(stage_capacities: Mapping[str, Bound], stage: str) -> ThroughputBound:
    if stage not in stage_capacities: raise KeyError(stage)
    x=dict(stage_capacities); x[stage]=Bound(0,0,f'knockout:{stage}')
    return serial_throughput(x)

def capacity_multiplier(base: Bound, multiplier: Bound) -> Bound:
    return Bound(base.low*multiplier.low,base.high*multiplier.high,f'({base.evidence})*({multiplier.evidence})')


@dataclass(frozen=True)
class MeasurementSetResult:
    measurements: tuple[str, ...]
    residual_width_if_upper_realized: float
    lower_bound_if_upper_realized: float
    sufficient_to_lift_zero_lower_bound: bool

def measurement_set_analysis(stage_capacities: Mapping[str, Bound], measurements: tuple[str, ...]) -> MeasurementSetResult:
    """Analyze an explicitly optimistic measurement scenario without inventing a distribution.

    Each named stage is hypothetically resolved at its *existing evidence-backed upper bound*.
    This is not expected VOI. It answers a narrower falsifiable question: even if these
    measurements came back as favorably as current evidence permits, would they shrink
    the throughput interval / lift its lower bound?
    """
    unknown=set(measurements)-set(stage_capacities)
    if unknown: raise KeyError(sorted(unknown)[0])
    x=dict(stage_capacities)
    for k in measurements:
        b=x[k]
        if not isfinite(b.high):
            # An unbounded quantity cannot be optimistically point-resolved without a value.
            continue
        x[k]=Bound(b.high,b.high,f'hypothetical perfect measurement at existing upper bound: {b.evidence}')
    r=serial_throughput(x)
    width=r.high-r.low if isfinite(r.high) else inf
    return MeasurementSetResult(tuple(sorted(measurements)),width,r.low,r.low>0)

def minimal_zero_lifting_measurement_set(stage_capacities: Mapping[str, Bound]) -> tuple[str, ...]:
    """Return stages that all must acquire positive lower bounds before serial throughput's lower bound can exceed zero.

    This is a structural information requirement, not a probabilistic VOI ranking.
    """
    return tuple(sorted(k for k,b in stage_capacities.items() if b.low == 0))

def coefficient_requirement(output: Bound, coefficient: Bound) -> Bound:
    """Propagate a nonnegative per-output physical coefficient without midpoint substitution."""
    return Bound(output.low*coefficient.low, output.high*coefficient.high,
                 f'output({output.evidence}) * coefficient({coefficient.evidence})')
