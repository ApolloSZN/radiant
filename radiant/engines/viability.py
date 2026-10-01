"""Quantitative stock/flow and maintenance closure.

Topological RAF and material viability are deliberately separate.  A RAF can exist
while failing material balance, capacity, energy, or replacement constraints.

This module uses explicit mass/resource balance: *every consumed item* must be
produced internally or supplied through an explicitly bounded external inflow.
Earlier Radiant versions constrained only maintained items, which could accidentally
make raw inputs free.  That failure mode is now impossible.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Iterable
import numpy as np
from scipy.optimize import linprog
from radiant.engines.raf import Process, max_raf

@dataclass(frozen=True)
class FlowProcess:
    id: str
    inputs: Mapping[str, float]
    outputs: Mapping[str, float]
    capacity: float = float("inf")
    energy_per_flux: float = 0.0

    def net(self, item: str) -> float:
        return float(self.outputs.get(item, 0.0) - self.inputs.get(item, 0.0))

@dataclass
class ViabilityResult:
    feasible: bool
    fluxes: dict[str, float] = field(default_factory=dict)
    imports: dict[str, float] = field(default_factory=dict)
    energy_used: float = 0.0
    maintenance_slack: dict[str, float] = field(default_factory=dict)
    balance_slack: dict[str, float] = field(default_factory=dict)
    status: str = ""
    objective: float | None = None


def material_viability(processes: Iterable[FlowProcess], maintenance: Mapping[str, float],
                       import_limits: Mapping[str, float] | None = None,
                       energy_budget: float = float("inf"),
                       import_penalty: float = 1.0, flux_penalty: float = 1e-6) -> ViabilityResult:
    """Minimum-external-input steady-flow feasibility LP.

    For every item appearing anywhere in the network::

        sum_j net[i,j] * flux_j + external_i >= maintenance_i

    External inflow exists only for items explicitly listed in ``import_limits``.
    Thus a process cannot consume an unproduced resource for free. ``maintenance``
    is a replacement/depreciation drain on top of ordinary process consumption.
    """
    ps = list(processes); imports = dict(import_limits or {})
    items = sorted(set(maintenance) | set(imports) |
                   {x for p in ps for x in (*p.inputs.keys(), *p.outputs.keys())})
    imp_items = sorted(imports)
    n, k = len(ps), len(imp_items)
    c = np.r_[np.full(n, flux_penalty), np.full(k, import_penalty)]
    A=[]; b=[]
    for item in items:
        need=float(maintenance.get(item, 0.0))
        row=[-p.net(item) for p in ps] + [(-1.0 if x == item else 0.0) for x in imp_items]
        A.append(row); b.append(-need)
    if np.isfinite(energy_budget):
        A.append([p.energy_per_flux for p in ps] + [0.0]*k); b.append(float(energy_budget))
    bounds=[(0, None if not np.isfinite(p.capacity) else p.capacity) for p in ps]
    bounds += [(0, float(imports[x])) for x in imp_items]
    res=linprog(c, A_ub=np.asarray(A) if A else None, b_ub=np.asarray(b) if b else None,
                bounds=bounds, method="highs")
    if not res.success:
        return ViabilityResult(False, status=res.message)
    v=res.x[:n]; u=res.x[n:]
    flux={p.id: float(v[j]) for j,p in enumerate(ps) if v[j] > 1e-10}
    imp={x: float(u[j]) for j,x in enumerate(imp_items) if u[j] > 1e-10}
    balance={}
    for item in items:
        supplied=sum(p.net(item)*v[j] for j,p in enumerate(ps)) + imp.get(item,0.0)
        balance[item]=float(supplied-maintenance.get(item,0.0))
    maint={i: balance[i] for i in maintenance}
    return ViabilityResult(True, flux, imp,
                           float(sum(p.energy_per_flux*v[j] for j,p in enumerate(ps))),
                           maint, balance, res.message, float(res.fun))


def finite_horizon_viability(processes: Iterable[FlowProcess], initial_stocks: Mapping[str,float],
                             maintenance_rates: Mapping[str,float], horizon: float,
                             import_limits: Mapping[str,float] | None=None,
                             energy_budget: float=float("inf"),
                             require_non_depletion: bool=True) -> ViabilityResult:
    """Finite-horizon stock-flow feasibility under constant process rates.

    Maintenance rates are per unit time. External limits and process capacities are
    rates. Initial stocks may bridge temporary deficits. If ``require_non_depletion``
    is true, terminal enabling stocks must be at least their initial level, so drawing
    down inherited capital cannot masquerade as self-maintenance. If false, the test
    answers only whether stocks remain nonnegative over the chosen horizon.
    """
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    ps=list(processes); imports=dict(import_limits or {})
    items=sorted(set(initial_stocks)|set(maintenance_rates)|set(imports)|
                 {x for p in ps for x in (*p.inputs.keys(), *p.outputs.keys())})
    # Constant-rate dynamics are linear. Terminal stock constraint:
    # s0 + H*(N v + u - m) >= target, where target=s0 for non-depletion else 0.
    n,k=len(ps),len(imports); imp_items=sorted(imports)
    c=np.r_[np.full(n,1e-6),np.ones(k)]
    A=[]; b=[]
    for item in items:
        s0=float(initial_stocks.get(item,0.0)); m=float(maintenance_rates.get(item,0.0))
        target=s0 if require_non_depletion else 0.0
        # -H*(Nv+u) <= s0-target-H*m
        A.append([-horizon*p.net(item) for p in ps] +
                 [(-horizon if x==item else 0.0) for x in imp_items])
        b.append(s0-target-horizon*m)
    if np.isfinite(energy_budget):
        A.append([horizon*p.energy_per_flux for p in ps]+[0.0]*k); b.append(float(energy_budget))
    bounds=[(0,None if not np.isfinite(p.capacity) else p.capacity) for p in ps]
    bounds += [(0,float(imports[x])) for x in imp_items]
    if n + k == 0:
        # scipy.linprog rejects a zero-variable LP; feasibility is purely whether
        # inherited stocks cover cumulative maintenance over the horizon.
        feasible=all(rhs >= -1e-12 for rhs in b)
        if not feasible:
            return ViabilityResult(False,status='inherited stocks cannot satisfy horizon constraints')
        bal={}
        for item in items:
            terminal=float(initial_stocks.get(item,0.0))-horizon*maintenance_rates.get(item,0.0)
            target=float(initial_stocks.get(item,0.0)) if require_non_depletion else 0.0
            bal[item]=terminal-target
        return ViabilityResult(True,balance_slack=bal,maintenance_slack={i:bal[i] for i in maintenance_rates},status='analytic zero-variable feasibility',objective=0.0)
    res=linprog(c,A_ub=np.asarray(A),b_ub=np.asarray(b),bounds=bounds,method='highs')
    if not res.success:
        return ViabilityResult(False,status=res.message)
    v=res.x[:n];u=res.x[n:]
    flux={p.id:float(v[j]) for j,p in enumerate(ps) if v[j]>1e-10}
    imp={x:float(u[j]) for j,x in enumerate(imp_items) if u[j]>1e-10}
    bal={}
    for item in items:
        terminal=float(initial_stocks.get(item,0.0))+horizon*(sum(p.net(item)*v[j] for j,p in enumerate(ps))+imp.get(item,0)-maintenance_rates.get(item,0))
        target=float(initial_stocks.get(item,0.0)) if require_non_depletion else 0.0
        bal[item]=terminal-target
    return ViabilityResult(True,flux,imp,float(horizon*sum(p.energy_per_flux*v[j] for j,p in enumerate(ps))),
                           {i:bal[i] for i in maintenance_rates},bal,res.message,float(res.fun))


def quantitative_closure(food: Iterable[str], raf_processes: Iterable[Process],
                         flow_processes: Iterable[FlowProcess], maintenance: Mapping[str,float],
                         import_limits: Mapping[str,float] | None=None,
                         energy_budget: float=float("inf")) -> dict:
    """Two-gate closure: topological maxRAF first, then quantitative viability."""
    rp=list(raf_processes); fp=list(flow_processes)
    raf=max_raf(food, rp)
    if not raf.self_sustaining:
        return {"topological_closure": False, "material_viability": False,
                "self_maintaining": False, "raf_core": [], "viability": None}
    core_fp=[p for p in fp if p.id in raf.core]
    vr=material_viability(core_fp, maintenance, import_limits, energy_budget)
    return {"topological_closure": True, "material_viability": vr.feasible,
            "self_maintaining": bool(vr.feasible), "raf_core": sorted(raf.core), "viability": vr}

@dataclass
class TrajectoryViabilityResult(ViabilityResult):
    """Finite-horizon result with period-resolved rates and stocks."""
    flux_trajectory: list[dict[str, float]] = field(default_factory=list)
    import_trajectory: list[dict[str, float]] = field(default_factory=list)
    stock_trajectory: list[dict[str, float]] = field(default_factory=list)


def path_viability(processes: Iterable[FlowProcess], initial_stocks: Mapping[str, float],
                   maintenance_rates: Mapping[str, float], periods: int, dt: float = 1.0,
                   import_limits: Mapping[str, float] | None = None,
                   capacity_schedule: Mapping[str, Iterable[float]] | None = None,
                   import_schedule: Mapping[str, Iterable[float]] | None = None,
                   energy_budget: float = float("inf"),
                   terminal_floor: Mapping[str, float] | None = None,
                   require_non_depletion: bool = True) -> TrajectoryViabilityResult:
    """Period-resolved stock-flow viability LP.

    Unlike :func:`finite_horizon_viability`, process/import rates may vary by period
    and stock non-negativity is enforced at *every* boundary. This prevents an
    aggregate terminal balance from borrowing a resource from future production.

    ``capacity_schedule[p]`` and ``import_schedule[item]`` are per-period rate
    ceilings. Missing schedules fall back to process capacity / ``import_limits``.
    ``terminal_floor`` can encode a desired final reserve; otherwise enabling stocks
    are restored to initial levels when ``require_non_depletion`` is true, and zero
    is the terminal floor for survival-only analysis.
    """
    if periods <= 0 or dt <= 0:
        raise ValueError("periods and dt must be positive")
    ps = list(processes); imports = dict(import_limits or {})
    cap_sched = {k: list(v) for k, v in (capacity_schedule or {}).items()}
    imp_sched = {k: list(v) for k, v in (import_schedule or {}).items()}
    for name, seq in {**cap_sched, **imp_sched}.items():
        if len(seq) != periods:
            raise ValueError(f"schedule {name!r} must have exactly {periods} periods")
        if any(float(x) < 0 for x in seq):
            raise ValueError(f"schedule {name!r} contains a negative limit")
    items = sorted(set(initial_stocks)|set(maintenance_rates)|set(imports)|set(imp_sched)|
                   set(terminal_floor or {})|
                   {x for p in ps for x in (*p.inputs.keys(), *p.outputs.keys())})
    imp_items = sorted(set(imports)|set(imp_sched))
    n, k, m = len(ps), len(imp_items), len(items)
    # x = [v(t,p), u(t,i), s(t=1..T,item)]. s0 is fixed input.
    nv, nu = periods*n, periods*k
    ns = periods*m
    total = nv+nu+ns
    if total == 0:
        return TrajectoryViabilityResult(True, status="empty path", objective=0.0,
                                         stock_trajectory=[dict(initial_stocks)])
    c = np.zeros(total); c[:nv] = 1e-6; c[nv:nv+nu] = 1.0
    bounds=[]
    for t in range(periods):
        for p in ps:
            seq=cap_sched.get(p.id)
            lim=float(seq[t]) if seq is not None else p.capacity
            bounds.append((0, None if not np.isfinite(lim) else lim))
    for t in range(periods):
        for item in imp_items:
            seq=imp_sched.get(item)
            lim=float(seq[t]) if seq is not None else float(imports.get(item,0.0))
            bounds.append((0,lim))
    bounds += [(0,None)]*ns
    Aeq=[]; beq=[]
    def sidx(t1,j): return nv+nu+(t1-1)*m+j
    for t in range(periods):
        for j,item in enumerate(items):
            row=np.zeros(total)
            row[sidx(t+1,j)] = 1.0
            if t > 0: row[sidx(t,j)] = -1.0
            for q,p in enumerate(ps): row[t*n+q] -= dt*p.net(item)
            for q,x in enumerate(imp_items):
                if x==item: row[nv+t*k+q] -= dt
            rhs=(float(initial_stocks.get(item,0.0)) if t==0 else 0.0) - dt*float(maintenance_rates.get(item,0.0))
            Aeq.append(row); beq.append(rhs)
    Aub=[]; bub=[]
    if np.isfinite(energy_budget):
        row=np.zeros(total)
        for t in range(periods):
            for q,p in enumerate(ps): row[t*n+q]=dt*p.energy_per_flux
        Aub.append(row); bub.append(float(energy_budget))
    floors=dict(terminal_floor or {})
    for j,item in enumerate(items):
        floor=float(floors.get(item, initial_stocks.get(item,0.0) if require_non_depletion else 0.0))
        row=np.zeros(total); row[sidx(periods,j)] = -1.0
        Aub.append(row); bub.append(-floor)
    res=linprog(c,A_ub=np.asarray(Aub) if Aub else None,b_ub=np.asarray(bub) if bub else None,
                A_eq=np.asarray(Aeq),b_eq=np.asarray(beq),bounds=bounds,method="highs")
    if not res.success:
        return TrajectoryViabilityResult(False,status=res.message)
    x=res.x
    flux_tr=[]; imp_tr=[]
    for t in range(periods):
        flux_tr.append({p.id:float(x[t*n+q]) for q,p in enumerate(ps) if x[t*n+q]>1e-10})
        imp_tr.append({item:float(x[nv+t*k+q]) for q,item in enumerate(imp_items) if x[nv+t*k+q]>1e-10})
    stock_tr=[{item:float(initial_stocks.get(item,0.0)) for item in items}]
    for t in range(1,periods+1):
        stock_tr.append({item:float(x[sidx(t,j)]) for j,item in enumerate(items)})
    energy=dt*sum(p.energy_per_flux*x[t*n+q] for t in range(periods) for q,p in enumerate(ps))
    final=stock_tr[-1]
    slack={item: final[item]-float(floors.get(item,initial_stocks.get(item,0.0) if require_non_depletion else 0.0)) for item in items}
    return TrajectoryViabilityResult(True,
        fluxes={p.id:sum(d.get(p.id,0.0)*dt for d in flux_tr) for p in ps},
        imports={i:sum(d.get(i,0.0)*dt for d in imp_tr) for i in imp_items},
        energy_used=float(energy),maintenance_slack={i:slack[i] for i in maintenance_rates},
        balance_slack=slack,status=res.message,objective=float(res.fun),
        flux_trajectory=flux_tr,import_trajectory=imp_tr,stock_trajectory=stock_tr)
