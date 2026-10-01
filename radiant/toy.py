"""Illustrative networks at three scales, for tests and the demo.

EVERY NUMBER AND NETWORK HERE IS ILLUSTRATIVE. None of it is sourced data.
The engines refuse nothing; the ledger is what separates evidence from
examples, and these carry source='ILLUSTRATIVE' so they can never be
mistaken for measurements.
"""
from __future__ import annotations

import math

from radiant.engines.counterfactual import CurveState, Snapshot, Threshold
from radiant.engines.raf import Process
from radiant.kernel import AdaptiveSystem

P = Process.of
ILL = "ILLUSTRATIVE"


def protocell() -> AdaptiveSystem:
    """Abstract autocatalytic chemistry: two food species, mutual catalysis, a membrane."""
    procs = [
        P("r1", ["A", "B"], ["C"], ["D"]),
        P("r2", ["C", "A"], ["D"], ["C"]),
        P("r3", ["D", "B"], ["E"], ["E"]),
        P("r4", ["E", "A"], ["membrane"], ["C"]),
        P("r_dead", ["Z"], ["Y"], ["C"]),          # needs a species the environment never supplies
    ]
    return AdaptiveSystem(
        id="protocell", name="Toy protocell", scale="chemical",
        boundary="membrane-enclosed volume",
        viability={"membrane_integrity": (0.6, 1.0)},
        food={"A", "B"}, processes=procs,
        observes={"membrane_integrity"}, acts_on={"membrane_integrity"},
    )


def lab() -> AdaptiveSystem:
    """A research lab: reagents and funding in, results out, instruments and methods reused."""
    procs = [
        P("run_experiment", ["reagents", "protocol"], ["data"], ["instrument"]),
        P("fit_model", ["data"], ["model"], ["analysis_code"]),
        P("design_protocol", ["model"], ["protocol"], ["model"]),
        P("write_code", ["model", "funding"], ["analysis_code"], ["analysis_code"]),
        P("buy_instrument", ["funding"], ["instrument"], [], requires_catalyst=False),
        P("seed_protocol", ["funding"], ["protocol"], [], requires_catalyst=False),
    ]
    return AdaptiveSystem(
        id="lab", name="Toy research lab", scale="lab",
        boundary="people, instruments and records under one PI",
        viability={"funding_months": (6, 60)},
        food={"reagents", "funding"}, processes=procs,
        observes={"funding_months"}, acts_on={"funding_months"},
    )


def industry_processes() -> list[Process]:
    return [
        P("import_power", ["grid_power"], ["electricity"], [], requires_catalyst=False),
        P("pv_generate", ["sunlight"], ["electricity"], ["pv_panel"]),
        P("refine_si", ["sand", "electricity"], ["silicon"], ["furnace"]),
        P("make_pv", ["silicon", "electricity"], ["pv_panel"], ["fab_tools"]),
        P("smelt", ["ore", "electricity"], ["metal"], ["furnace"]),
        P("make_furnace", ["metal", "electricity"], ["furnace"], ["fab_tools"]),
        P("make_tools", ["metal", "electricity"], ["fab_tools"], ["fab_tools"]),   # machine tools make machine tools
        P("make_electrolyzer", ["metal", "electricity"], ["electrolyzer"], ["fab_tools"]),
        P("electrolysis", ["water", "electricity"], ["hydrogen"], ["electrolyzer"]),
        P("make_reactor", ["metal", "electricity"], ["reactor"], ["fab_tools"]),
        P("haber", ["hydrogen", "air"], ["ammonia"], ["reactor"]),
    ]


INDUSTRY_FOOD = {"sunlight", "sand", "ore", "water", "air", "grid_power"}


def industry() -> AdaptiveSystem:
    return AdaptiveSystem(
        id="toy_region", name="Toy industrial region", scale="region",
        boundary="regional border for goods and power",
        viability={"power_margin": (0.1, 1.0)},
        food=set(INDUSTRY_FOOD), processes=industry_processes(),
        observes={"power_margin"}, acts_on={"power_margin"},
    )


def industry_snapshot() -> Snapshot:
    """Two cost curves gate two processes. Values are illustrative, in ln($/unit)."""
    return Snapshot(
        as_of="ILLUSTRATIVE-T0",
        food=set(INDUSTRY_FOOD),
        processes=industry_processes(),
        curves={
            "pv_module_cost": CurveState("pv_module_cost", math.log(0.30), 0.08, 0.03, ILL),
            "electrolyzer_cost": CurveState("electrolyzer_cost", math.log(1000.0), 0.06, 0.04, ILL),
        },
        thresholds=[
            Threshold("pv_generate", "pv_module_cost", math.log(0.20), ILL),
            Threshold("electrolysis", "electrolyzer_cost", math.log(400.0), ILL),
        ],
    )
