"""Catalytic closure engine (RAF theory).

The same algorithm detects a self-sustaining core in a chemical reaction
network and in an industrial production network. That shared math is the
formal bridge from "inception of life" to technology and civilization.

Definitions (Hordijk & Steel):
  A set of processes R' is a RAF relative to food set F if
    RA: every process in R' is catalyzed by an item produced within
        cl(F, R') (or in F), and
    F : every input of every process in R' lies in cl(F, R'),
  where cl(F, R') is everything reachable from F using processes in R'.

The maximal RAF is unique (the union of RAFs is a RAF) and is found in
polynomial time by repeated pruning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Process:
    """A catalyzed transformation: inputs -> outputs, enabled by any catalyst.

    Chemistry: reactants -> products, catalyzed by a molecule.
    Industry:  materials -> goods, enabled by a tool, machine or skill that
               is required but not consumed.
    """
    id: str
    inputs: frozenset[str]
    outputs: frozenset[str]
    catalysts: frozenset[str] = frozenset()
    requires_catalyst: bool = True

    @staticmethod
    def of(id: str, inputs: Iterable[str], outputs: Iterable[str],
           catalysts: Iterable[str] = (), requires_catalyst: bool = True) -> "Process":
        return Process(id, frozenset(inputs), frozenset(outputs),
                       frozenset(catalysts), requires_catalyst)


def closure(food: Iterable[str], processes: Iterable[Process]) -> set[str]:
    """Everything producible from food using the given processes (catalysis ignored)."""
    avail = set(food)
    procs = list(processes)
    changed = True
    while changed:
        changed = False
        for p in procs:
            if p.inputs <= avail and not p.outputs <= avail:
                avail |= p.outputs
                changed = True
    return avail


@dataclass
class RAFResult:
    core: set[str]                              # process ids in the maximal RAF
    produced: set[str]                          # items reachable inside the core
    removal_log: dict[str, dict] = field(default_factory=dict)  # why each pruned process fell out

    @property
    def self_sustaining(self) -> bool:
        return bool(self.core)


def max_raf(food: Iterable[str], processes: Iterable[Process]) -> RAFResult:
    """Maximal RAF with a causal log of every pruning step."""
    food = set(food)
    current = {p.id: p for p in processes}
    log: dict[str, dict] = {}
    round_ = 0
    while True:
        cl = closure(food, current.values())
        drop = {}
        for pid, p in current.items():
            missing_inputs = sorted(p.inputs - cl)
            catalyst_ok = (not p.requires_catalyst) or bool(p.catalysts & cl)
            if missing_inputs or not catalyst_ok:
                drop[pid] = {
                    "round": round_,
                    "missing_inputs": missing_inputs,
                    "missing_catalyst": [] if catalyst_ok else sorted(p.catalysts),
                }
        if not drop:
            return RAFResult(core=set(current), produced=cl, removal_log=log)
        log.update(drop)
        for pid in drop:
            del current[pid]
        round_ += 1


def knockout(food: Iterable[str], processes: list[Process],
             remove_items: Iterable[str] = (), remove_processes: Iterable[str] = ()) -> dict:
    """Exact counterfactual: what leaves the self-sustaining core if we remove things?

    Returns the dropped processes, each with the pruning reason and round, so the
    cascade can be read as a causal trace (round 0 = direct hit, later rounds = knock-on).
    """
    food = set(food)
    base = max_raf(food, processes)
    remove_items = set(remove_items)
    remove_processes = set(remove_processes)
    food_after = food - remove_items
    # Removing an item cuts its external supply only; internal production of it survives.
    procs_after = [p for p in processes if p.id not in remove_processes]
    after = max_raf(food_after, procs_after)
    dropped = sorted(base.core - after.core)
    producers: dict[str, list[Process]] = {}
    for p in processes:
        for o in p.outputs:
            producers.setdefault(o, []).append(p)

    def roots(item: str, seen: set[str]) -> set[str]:
        if item in seen:
            return set()
        seen.add(item)
        if item in remove_items:
            return {f"supply_cut:{item}"}
        if item not in producers and item not in food:
            return {f"never_supplied:{item}"}
        out: set[str] = set()
        for q in producers.get(item, []):
            if q.id in remove_processes:
                out.add(f"process_removed:{q.id}")
            elif q.id in after.removal_log:
                why = after.removal_log[q.id]
                for x in why["missing_inputs"] + why["missing_catalyst"]:
                    out |= roots(x, seen)
        return out

    trace = {}
    for pid in dropped:
        if pid in remove_processes:
            trace[pid] = {"removed_directly": True, "root_causes": [f"process_removed:{pid}"]}
            continue
        why = dict(after.removal_log[pid])
        rc: set[str] = set()
        for x in why["missing_inputs"] + why["missing_catalyst"]:
            rc |= roots(x, set())
        why["root_causes"] = sorted(rc)
        trace[pid] = why
    return {
        "core_before": sorted(base.core),
        "core_after": sorted(after.core),
        "dropped": dropped,
        "trace": trace,
        "criticality": len(dropped),
    }


def criticality_ranking(food: Iterable[str], processes: list[Process]) -> list[tuple[str, int]]:
    """Rank every food item and every core process by how much of the core it holds up."""
    food = set(food)
    base = max_raf(food, processes)
    scores = []
    for item in sorted(food):
        scores.append((f"food:{item}", knockout(food, processes, remove_items=[item])["criticality"]))
    for pid in sorted(base.core):
        scores.append((f"process:{pid}", knockout(food, processes, remove_processes=[pid])["criticality"]))
    return sorted(scores, key=lambda s: (-s[1], s[0]))


def topological_closure_time(food: Iterable[str], processes_by_time: dict[float, list[Process]]) -> float | None:
    """First time a non-empty RAF exists. This is NOT sufficient for material self-maintenance or life."""
    for t in sorted(processes_by_time):
        if max_raf(food, processes_by_time[t]).self_sustaining:
            return t
    return None


# Backward-compatible name; semantically this is only topological closure.
inception_time = topological_closure_time

def recursive_knockout_trace(food: Iterable[str], processes: list[Process],
                             remove_items: Iterable[str]=(), remove_processes: Iterable[str]=()) -> dict:
    """Explain a knockout as a process-level DAG from intervention roots to dropped processes.
    Unlike the compact root-cause labels in knockout(), this preserves intermediate producers.
    """
    base=max_raf(food,processes); food_after=set(food)-set(remove_items); removed=set(remove_processes)
    after=max_raf(food_after,[p for p in processes if p.id not in removed])
    by_id={p.id:p for p in processes}; producers={}
    for p in processes:
        for o in p.outputs: producers.setdefault(o,[]).append(p.id)
    nodes={}; edges=set()
    for item in remove_items: nodes[f'supply:{item}']={'type':'intervention','item':item}
    for pid in removed: nodes[f'process:{pid}']={'type':'intervention_process','process':pid}
    dropped=sorted(base.core-after.core)
    for pid in dropped:
        key=f'process:{pid}'; nodes.setdefault(key,{'type':'dropped_process','process':pid})
        if pid in removed: continue
        why=after.removal_log.get(pid,{})
        for item in why.get('missing_inputs',[])+why.get('missing_catalyst',[]):
            ik=f'item:{item}'; nodes.setdefault(ik,{'type':'unavailable_item','item':item}); edges.add((ik,key))
            if item in set(remove_items): edges.add((f'supply:{item}',ik))
            for qid in producers.get(item,[]):
                if qid in dropped or qid in removed:
                    qk=f'process:{qid}'; nodes.setdefault(qk,{'type':'dropped_process','process':qid}); edges.add((qk,ik))
    return {'dropped':dropped,'nodes':nodes,'edges':[{'from':a,'to':b} for a,b in sorted(edges)]}
