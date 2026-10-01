"""Evidence-bound constraint resolution for real production systems.

This layer does not infer causality from prose. It consumes an explicitly encoded
production model whose parameters are bound to evidence records, then asks which
capacity/input relaxations have the largest marginal effect on a declared objective.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Mapping, Iterable
import numpy as np
from scipy.optimize import linprog
from radiant.engines.viability import FlowProcess

@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    source_url: str
    published: str
    tier: str = "T0"
    note: str = ""

@dataclass(frozen=True)
class ProductionSystem:
    processes: tuple[FlowProcess, ...]
    import_limits: Mapping[str, float]
    objective_item: str
    evidence: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

@dataclass
class ThroughputResult:
    feasible: bool
    throughput: float
    fluxes: dict[str,float]
    imports: dict[str,float]
    status: str


def maximize_throughput(system: ProductionSystem, energy_budget: float=float("inf")) -> ThroughputResult:
    ps=list(system.processes); imp_items=sorted(system.import_limits)
    n=len(ps); k=len(imp_items)
    items=sorted({x for p in ps for x in (*p.inputs.keys(),*p.outputs.keys())} | set(imp_items))
    # maximize net production of objective => minimize negative net production
    c=np.r_[[-p.net(system.objective_item) for p in ps], np.zeros(k)]
    A=[]; b=[]
    # Every non-objective intermediate must have non-negative net balance.
    for item in items:
        if item == system.objective_item: continue
        A.append([-p.net(item) for p in ps] + [(-1.0 if x==item else 0.0) for x in imp_items]); b.append(0.0)
    if np.isfinite(energy_budget):
        A.append([p.energy_per_flux for p in ps]+[0.0]*k); b.append(float(energy_budget))
    bounds=[(0,None if not np.isfinite(p.capacity) else p.capacity) for p in ps]
    bounds += [(0,float(system.import_limits[x])) for x in imp_items]
    res=linprog(c,A_ub=np.asarray(A) if A else None,b_ub=np.asarray(b) if b else None,bounds=bounds,method="highs")
    if not res.success: return ThroughputResult(False,0.0,{}, {},res.message)
    v=res.x[:n]; u=res.x[n:]
    throughput=sum(p.net(system.objective_item)*v[j] for j,p in enumerate(ps))
    return ThroughputResult(True,float(throughput),{p.id:float(v[j]) for j,p in enumerate(ps) if v[j]>1e-9},
                            {x:float(u[j]) for j,x in enumerate(imp_items) if u[j]>1e-9},res.message)


def intervention_scan(system: ProductionSystem, fraction: float=.20) -> list[dict]:
    """One-at-a-time +fraction capacity/input relaxations, ranked by objective gain."""
    base=maximize_throughput(system); out=[]
    for i,p in enumerate(system.processes):
        if not np.isfinite(p.capacity) or p.capacity <= 0: continue
        ps=list(system.processes); ps[i]=replace(p,capacity=p.capacity*(1+fraction))
        r=maximize_throughput(replace(system,processes=tuple(ps)))
        out.append({'intervention':f'capacity:{p.id}','baseline':base.throughput,'throughput':r.throughput,
                    'gain':r.throughput-base.throughput,'gain_pct':100*(r.throughput/base.throughput-1) if base.throughput else None,
                    'evidence_ids':list(system.evidence.get(f'capacity:{p.id}',()))})
    for item,lim in system.import_limits.items():
        imports=dict(system.import_limits); imports[item]=lim*(1+fraction)
        r=maximize_throughput(replace(system,import_limits=imports))
        out.append({'intervention':f'import:{item}','baseline':base.throughput,'throughput':r.throughput,
                    'gain':r.throughput-base.throughput,'gain_pct':100*(r.throughput/base.throughput-1) if base.throughput else None,
                    'evidence_ids':list(system.evidence.get(f'import:{item}',()))})
    return sorted(out,key=lambda x:(-x['gain'],x['intervention']))
