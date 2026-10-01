"""Counterfactual engine: the atomic Radiant operation.

  measured snapshot -> intervention -> propagate curves -> threshold crossings
  -> feasible processes -> self-sustaining core (RAF) -> adjacency
  -> distribution + causal trace

Baseline and intervention runs share the same random draws (common random
numbers), so every difference in the output is caused by the intervention,
not by sampling noise. Same snapshot + interventions + seed => identical
result hash on any machine.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field

import numpy as np

from radiant.engines.raf import Process, closure, max_raf

MODEL_VERSION = "counterfactual-0.2.0"


@dataclass(frozen=True)
class CurveState:
    metric: str
    log_now: float        # ln(cost) at the snapshot date
    rate: float           # progress rate per year (positive = falling cost)
    rate_se: float        # uncertainty of the rate
    source: str           # evidence pointer (observation ids, dataset, or 'ILLUSTRATIVE')


@dataclass(frozen=True)
class Threshold:
    process: str          # process that becomes feasible once the metric is low enough
    metric: str
    log_value: float
    source: str


@dataclass(frozen=True)
class Intervention:
    kind: str             # 'scale_cost' | 'set_rate' | 'cut_supply' | 'remove_process' | 'add_supply'
    target: str
    value: float | None = None


@dataclass
class Snapshot:
    as_of: str
    food: set[str]
    processes: list[Process]
    curves: dict[str, CurveState]
    thresholds: list[Threshold] = field(default_factory=list)


def _round(x):
    if isinstance(x, float):
        return None if not np.isfinite(x) else round(x, 10)
    if isinstance(x, dict):
        return {k: _round(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_round(v) for v in x]
    return x


def _structural(snapshot: Snapshot, interventions: list[Intervention]):
    food = set(snapshot.food)
    procs = list(snapshot.processes)
    for iv in interventions:
        if iv.kind == "cut_supply":
            food.discard(iv.target)
        elif iv.kind == "add_supply":
            food.add(iv.target)
        elif iv.kind == "remove_process":
            procs = [p for p in procs if p.id != iv.target]
    return food, procs


def _curve_params(snapshot: Snapshot, interventions: list[Intervention]):
    log_now = {m: c.log_now for m, c in snapshot.curves.items()}
    rate = {m: c.rate for m, c in snapshot.curves.items()}
    for iv in interventions:
        if iv.kind == "scale_cost":
            log_now[iv.target] += float(np.log(iv.value))
        elif iv.kind == "set_rate":
            rate[iv.target] = float(iv.value)
    return log_now, rate


def _evaluate(snapshot, food, procs, log_cost):
    by_proc: dict[str, list[Threshold]] = {}
    for th in snapshot.thresholds:
        by_proc.setdefault(th.process, []).append(th)
    feasible = [p for p in procs
                if all(log_cost[th.metric] <= th.log_value for th in by_proc.get(p.id, []))]
    res = max_raf(food, feasible)
    reach = closure(food, feasible)
    adjacency = sum(1 for p in feasible if p.inputs <= reach)
    return {p.id for p in feasible}, res, adjacency


def run(snapshot: Snapshot, interventions: list[Intervention], horizon_years: float,
        n: int = 2000, seed: int = 0, change_threshold: float = 0.05) -> dict:
    rng = np.random.default_rng(seed)
    metrics = sorted(snapshot.curves)
    z = rng.standard_normal((n, len(metrics)))

    worlds = {"baseline": [], "intervention": list(interventions)}
    stats = {}
    for name, ivs in worlds.items():
        food, procs = _structural(snapshot, ivs)
        log_now, rate = _curve_params(snapshot, ivs)
        in_core = {p.id: 0 for p in snapshot.processes}
        adj, core_size = np.empty(n), np.empty(n)
        crossings = {th: np.empty(n) for th in range(len(snapshot.thresholds))}
        for i in range(n):
            r = {m: rate[m] + snapshot.curves[m].rate_se * z[i, j] for j, m in enumerate(metrics)}
            log_cost = {m: log_now[m] - r[m] * horizon_years for m in metrics}
            _, res, a = _evaluate(snapshot, food, procs, log_cost)
            for pid in res.core:
                in_core[pid] += 1
            adj[i], core_size[i] = a, len(res.core)
            for k, th in enumerate(snapshot.thresholds):
                gap = log_now[th.metric] - th.log_value
                crossings[k][i] = 0.0 if gap <= 0 else (gap / r[th.metric] if r[th.metric] > 0 else np.inf)
        # deterministic mean-parameter run for the causal trace
        log_cost_mean = {m: log_now[m] - rate[m] * horizon_years for m in metrics}
        feas_mean, res_mean, _ = _evaluate(snapshot, food, procs, log_cost_mean)
        stats[name] = {
            "p_core": {k: v / n for k, v in in_core.items()},
            "adjacency": adj, "core_size": core_size, "crossings": crossings,
            "feasible_mean": feas_mean, "removal_log_mean": res_mean.removal_log,
            "food": food, "proc_ids": {p.id for p in procs},
        }

    b, v = stats["baseline"], stats["intervention"]
    delta_adj = v["adjacency"] - b["adjacency"]
    procs_by_id = {p.id: p for p in snapshot.processes}
    trace = {}
    for pid in sorted(procs_by_id):
        pb, pv = b["p_core"][pid], v["p_core"][pid]
        if abs(pv - pb) < change_threshold:
            continue
        p = procs_by_id[pid]
        th_rows = []
        for k, th in enumerate(snapshot.thresholds):
            if th.process == pid:
                th_rows.append({
                    "metric": th.metric, "source": th.source,
                    "crossing_years_median_baseline": float(np.median(b["crossings"][k])),
                    "crossing_years_median_intervention": float(np.median(v["crossings"][k])),
                })
        trace[pid] = {
            "p_core_baseline": pb, "p_core_intervention": pv,
            "process_removed_by_intervention": pid not in v["proc_ids"],
            "feasible_at_mean": {"baseline": pid in b["feasible_mean"], "intervention": pid in v["feasible_mean"]},
            "thresholds": th_rows,
            "raf_pruning_at_mean": v["removal_log_mean"].get(pid) or b["removal_log_mean"].get(pid),
            "inputs": sorted(p.inputs), "catalysts": sorted(p.catalysts),
            "supply_cut": sorted(set(snapshot.food) - v["food"]),
        }

    def q(a):
        return {"p10": float(np.percentile(a, 10)), "p50": float(np.percentile(a, 50)),
                "p90": float(np.percentile(a, 90)), "mean": float(a.mean())}

    result = {
        "model_version": MODEL_VERSION,
        "assumptions": {
            "snapshot_as_of": snapshot.as_of, "horizon_years": horizon_years, "draws": n, "seed": seed,
            "interventions": [asdict(iv) for iv in interventions],
            "curve_sources": {m: c.source for m, c in snapshot.curves.items()},
        },
        "adjacency": {"baseline": q(b["adjacency"]), "intervention": q(v["adjacency"]), "delta": q(delta_adj)},
        "core_size": {"baseline": q(b["core_size"]), "intervention": q(v["core_size"])},
        "p_core": {"baseline": b["p_core"], "intervention": v["p_core"]},
        "trace": trace,
    }
    result = _round(result)
    result["result_hash"] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    return result
