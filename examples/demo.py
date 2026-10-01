"""End-to-end demo on ILLUSTRATIVE networks.  Run:  python -m examples.demo"""
import json

from radiant import toy
from radiant.engines.counterfactual import Intervention, run
from radiant.engines.raf import criticality_ranking, knockout


def show(title, obj):
    print(f"\n=== {title} ===")
    print(json.dumps(obj, indent=2) if not isinstance(obj, str) else obj)


# 1. One kernel, three scales: does each system produce its own catalysts?
for s in (toy.protocell(), toy.lab(), toy.industry()):
    v = s.self_producing()
    show(f"{s.name} [{s.scale}] self-producing", {"pass": v["pass"], "core": v["core"],
                                                   "coverage": round(v["coverage"], 2)})

# 2. What holds the industrial core up?
show("Criticality ranking (processes lost if removed)",
     criticality_ranking(toy.INDUSTRY_FOOD, toy.industry_processes())[:6])

# 3. Exact knockout with root causes
ko = knockout(toy.INDUSTRY_FOOD, toy.industry_processes(), remove_items=["ore"])
show("Knockout: cut ore imports", {"dropped": ko["dropped"],
     "root_causes": sorted({c for r in ko["trace"].values() for c in r["root_causes"]})})

# 4. Counterfactual: cut grid power, 5-year horizon, uncertain PV cost curve
snap = toy.industry_snapshot()
res = run(snap, [Intervention("cut_supply", "grid_power")], horizon_years=5, n=2000, seed=42)
show("Counterfactual: cut grid power, 5 years", {
    "core_size": res["core_size"], "adjacency_delta": res["adjacency"]["delta"],
    "trace_sample": {k: res["trace"][k] for k in list(res["trace"])[:2]},
    "result_hash": res["result_hash"]})

# 5. Counterfactual: halve electrolyzer cost now
res2 = run(snap, [Intervention("scale_cost", "electrolyzer_cost", 0.5)], horizon_years=5, n=2000, seed=42)
show("Counterfactual: halve electrolyzer cost", {
    "p_core_haber": {"baseline": res2["p_core"]["baseline"]["haber"],
                     "intervention": res2["p_core"]["intervention"]["haber"]},
    "trace": res2["trace"]})
