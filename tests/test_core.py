import math
import random

import numpy as np
import pytest

from radiant.engines import dynamics as D
from radiant.engines.counterfactual import Intervention, run
from radiant.engines.raf import Process, closure, knockout, max_raf, criticality_ranking
from radiant import toy

P = Process.of


# ------------------------------------------------------------ R1 Sahal / Wright -> Moore
def test_r1_wright_with_exponential_production_is_moore():
    w, g = 0.32, 0.25
    t = np.arange(0, 20.0)
    log_x = math.log(10) + g * t
    log_c = math.log(100) - w * log_x
    fit = D.fit_moore(t, log_c)
    assert fit.rate == pytest.approx(D.sahal_rate(w, g), rel=1e-9)
    assert D.fit_wright(log_x, log_c).rate == pytest.approx(w, rel=1e-9)


# ------------------------------------------------------------ R2 composite slowdown
C0, RATES = [5.0, 3.0, 2.0], [0.30, 0.10, 0.02]

def test_r2_drift_equals_minus_variance():
    for t in [0.0, 5.0, 20.0, 60.0]:
        h = 1e-5
        numeric = (D.composite_rate(C0, RATES, t + h) - D.composite_rate(C0, RATES, t - h)) / (2 * h)
        assert numeric == pytest.approx(D.composite_rate_drift(C0, RATES, t), rel=1e-5, abs=1e-12)
        assert D.composite_rate_drift(C0, RATES, t) <= 0

def test_r2_rate_converges_to_slowest_and_share_concentrates():
    assert D.composite_rate(C0, RATES, 800.0) == pytest.approx(min(RATES), abs=1e-6)
    assert D.shares(C0, RATES, 800.0)[2] == pytest.approx(1.0, abs=1e-6)

def test_r2_leverage_points_at_slow_components():
    lev = D.bottleneck_leverage(C0, RATES, 10.0)
    assert int(np.argmax(lev)) == 2 and lev[0] < 0

def test_r2_multiplicative_law_has_no_single_bottleneck():
    assert D.composite_rate(C0, RATES, 50.0, law="multiplicative") == pytest.approx(sum(RATES))


# ------------------------------------------------------------ R3 Amdahl
def test_r3_amdahl_ceiling():
    loop = D.LoopState(read=1, write=6, model=1, verify=2)
    assert loop.bottleneck() == "write"
    assert loop.amdahl("model", 1e9) == pytest.approx(loop.amdahl_ceiling("model"), rel=1e-6)
    assert loop.amdahl_ceiling("model") == pytest.approx(10 / 9)
    assert loop.closure_index() == pytest.approx(1 / 6)


# ------------------------------------------------------------ RAF engine
def test_raf_mutual_catalysis():
    procs = [P("r1", ["a", "b"], ["ab"], ["abb"]), P("r2", ["ab", "b"], ["abb"], ["ab"])]
    assert max_raf({"a", "b"}, procs).core == {"r1", "r2"}

def test_raf_empty_without_internal_catalyst():
    procs = [P("r1", ["a"], ["x"], ["q"])]
    res = max_raf({"a"}, procs)
    assert res.core == set() and res.removal_log["r1"]["missing_catalyst"] == ["q"]

def _random_network(rng, n_items=12, n_procs=18):
    items = [f"m{i}" for i in range(n_items)]
    procs = []
    for k in range(n_procs):
        ins = rng.sample(items, rng.randint(1, 2))
        outs = rng.sample(items, 1)
        cats = rng.sample(items, rng.randint(1, 2))
        procs.append(P(f"p{k}", ins, outs, cats))
    food = set(rng.sample(items, 3))
    return food, procs

def _is_raf(food, procs, core_ids):
    core = [p for p in procs if p.id in core_ids]
    cl = closure(food, core)
    return all(p.inputs <= cl and p.catalysts & cl for p in core)

def test_raf_result_is_a_raf_and_monotone():
    rng = random.Random(7)
    for _ in range(300):
        food, procs = _random_network(rng)
        core = max_raf(food, procs).core
        assert _is_raf(food, procs, core)
        extra = P("extra", [rng.choice(sorted(food))], ["m0"], [rng.choice(sorted(food))])
        assert core <= max_raf(food, procs + [extra]).core          # adding a process never shrinks the core
        assert max_raf(food, procs).core <= max_raf(food | {"m11"}, procs).core  # adding food never shrinks it

def test_knockout_trace_cascade():
    ko = knockout(toy.INDUSTRY_FOOD, toy.industry_processes(), remove_items=["ore"])
    assert "smelt" in ko["dropped"] and "haber" in ko["dropped"]
    assert "ore" in ko["trace"]["smelt"]["missing_inputs"]
    for pid, row in ko["trace"].items():                  # every dropped process traces back to the cut
        assert row["root_causes"] == ["supply_cut:ore"], (pid, row)
    assert "import_power" in ko["core_after"]

def test_criticality_ranks_ore_above_air():
    rank = dict(criticality_ranking(toy.INDUSTRY_FOOD, toy.industry_processes()))
    assert rank["food:ore"] > rank["food:air"]


# ------------------------------------------------------------ kernel, gate 3: cross-scale grammar
def test_same_kernel_describes_three_scales():
    for system in (toy.protocell(), toy.lab(), toy.industry()):
        v = system.self_producing()
        assert v["pass"], system.id
    assert "r_dead" not in toy.protocell().self_producing()["core"]

def test_autonomy_requires_all_three_closures():
    rng = np.random.default_rng(0)
    dev = rng.normal(0, 1, 200)
    resp = -0.5 * dev + rng.normal(0, 0.2, 200)
    ev = {"perturbations": [{"var": "membrane_integrity", "recovered": True}] * 5, "feedback": (dev, resp)}
    assert toy.protocell().profile(ev)["verdicts"]["autonomous"]
    thermostat = toy.protocell()
    thermostat.processes = []
    prof = thermostat.profile(ev)["verdicts"]
    assert prof["regulated"] and not prof["autonomous"]

def test_beta_detects_superexponential_and_rejects_linear():
    a = [1.0]
    for _ in range(40):
        a.append(a[-1] + 0.05 * a[-1] ** 1.3)
    sys = toy.lab()
    assert sys.self_improving(a)["beta"] == pytest.approx(0.3, abs=0.05)
    assert sys.self_improving(a)["pass"]
    assert not sys.self_improving([1 + 0.5 * t for t in range(40)])["pass"]

def test_learning_detects_falling_error():
    assert toy.lab().learning([1 / (1 + 0.3 * k) for k in range(20)])["pass"]


# ------------------------------------------------------------ gate 4: counterfactual reproducibility
def test_counterfactual_reproducible_and_null_intervention_is_zero():
    snap = toy.industry_snapshot()
    a = run(snap, [Intervention("cut_supply", "grid_power")], horizon_years=5, n=400, seed=11)
    b = run(snap, [Intervention("cut_supply", "grid_power")], horizon_years=5, n=400, seed=11)
    assert a["result_hash"] == b["result_hash"]
    null = run(snap, [], horizon_years=5, n=400, seed=11)
    assert null["adjacency"]["delta"]["mean"] == 0 and null["trace"] == {}

def test_counterfactual_trace_is_complete():
    snap = toy.industry_snapshot()
    res = run(snap, [Intervention("cut_supply", "grid_power")], horizon_years=5, n=400, seed=3)
    assert res["trace"], "cutting grid power must change something"
    for pid, row in res["trace"].items():
        explained = row["thresholds"] or row["raf_pruning_at_mean"] or row["supply_cut"]
        assert explained, pid

def test_recursive_knockout_trace_preserves_intermediate_cascade():
    from radiant.engines.raf import recursive_knockout_trace
    from radiant.toy import INDUSTRY_FOOD,industry_processes
    r=recursive_knockout_trace(INDUSTRY_FOOD,industry_processes(),remove_items=['ore'])
    assert r['dropped']
    assert any(e['from']=='supply:ore' for e in r['edges'])
    assert any(n.startswith('process:') for n in r['nodes'])
