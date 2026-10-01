"""Evidence-bounded LPT capacity-expansion arithmetic.

This module deliberately answers a narrower question than the factory-stage LP:
can disclosed additions to domestic *unit* capacity, even under optimistic utilization,
close a stated demand requirement?  It never infers the internal factory bottleneck.

All calculations require an explicit compatibility flag because public sources use
non-identical product definitions (>60 MVA, >100 MVA, 'large power transformer').
"""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class CapacityAddition:
    name: str
    units_per_year: float
    available_year: int
    evidence_id: str
    product_definition: str
    evidence_level: str = "reported"

@dataclass(frozen=True)
class CapacitySufficiencyResult:
    year: int
    demand_units: float
    legacy_nameplate_units: float
    disclosed_additions_units: float
    optimistic_domestic_capacity: float
    residual_external_supply_required: float
    domestic_capacity_share_upper_bound: float
    definition_compatible: bool
    interpretation: str


def optimistic_capacity_sufficiency(*, year:int, demand_units:float,
    legacy_nameplate_units:float, additions:Iterable[CapacityAddition],
    definition_compatible:bool) -> CapacitySufficiencyResult:
    if demand_units <= 0 or legacy_nameplate_units < 0:
        raise ValueError("demand must be positive and capacity nonnegative")
    additions = tuple(additions)
    added = sum(a.units_per_year for a in additions if a.available_year <= year)
    total = legacy_nameplate_units + added
    residual = max(0.0, demand_units-total)
    share = min(1.0, total/demand_units)
    if definition_compatible:
        interp = ("Even at 100% utilization of legacy nameplate and all disclosed compatible "
                  "additions available by the target year, external supply remains necessary."
                  if residual > 0 else
                  "Disclosed compatible nameplate is arithmetically sufficient, but feasibility is not established.")
    else:
        interp = ("Scenario only: source product definitions are not identical, so the arithmetic "
                  "cannot be promoted to an identified empirical capacity gap.")
    return CapacitySufficiencyResult(year,demand_units,legacy_nameplate_units,added,total,
        residual,share,definition_compatible,interp)


def minimum_additional_capacity_required(*, demand_units:float, legacy_nameplate_units:float,
                                         known_additions_units:float=0.0) -> float:
    """Pure accounting lower bound under 100% utilization; ignores reserves/product mix."""
    return max(0.0, demand_units-legacy_nameplate_units-known_additions_units)
