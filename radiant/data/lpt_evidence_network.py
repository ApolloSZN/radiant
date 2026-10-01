"""Evidence-bounded large-power-transformer production network.

This is deliberately a *qualitative/interval* empirical slice, not a fake calibrated
factory model. Public DOE evidence identifies the production graph and some measured
risk/lead-time facts, but does not publish compatible physical mass coefficients or
per-stage annual capacities. Those unknowns remain explicit.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceNode:
    id: str
    kind: str
    evidence_ids: tuple[str, ...]
    measured: dict

@dataclass(frozen=True)
class EvidenceEdge:
    source: str
    target: str
    evidence_ids: tuple[str, ...]

NODES = (
    EvidenceNode('goes','material',('DOE2024_LPT_RESILIENCE','DOE2022_GRID_DEEP_DIVE'),
                 {'domestic_supply':'majority_not_domestic','cost_share_approx':0.25}),
    EvidenceNode('ctc_copper','material',('DOE2024_LPT_RESILIENCE',),
                 {'cost_share_approx':0.25}),
    EvidenceNode('insulation','material',('DOE2024_LPT_RESILIENCE','DOE2022_GRID_DEEP_DIVE'),{}),
    EvidenceNode('core','component',('DOE2022_GRID_DEEP_DIVE',),{}),
    EvidenceNode('winding','component',('DOE2022_GRID_DEEP_DIVE',),{}),
    EvidenceNode('assembly','stage',('DOE2024_LPT_RESILIENCE',),{}),
    EvidenceNode('testing','stage',('DOE2022_GRID_DEEP_DIVE',),
                 {'test_duration_days_approx':7,'reported_test_beds_range':[1,2]}),
    EvidenceNode('qualified_lpt','output',('DOE2024_LPT_RESILIENCE',),
                 {'current_reported_lead_time_months_upper_or_exceeding':36}),
)
EDGES = (
    EvidenceEdge('goes','core',('DOE2024_LPT_RESILIENCE',)),
    EvidenceEdge('ctc_copper','winding',('DOE2024_LPT_RESILIENCE',)),
    EvidenceEdge('insulation','assembly',('DOE2024_LPT_RESILIENCE',)),
    EvidenceEdge('core','assembly',('DOE2024_LPT_RESILIENCE',)),
    EvidenceEdge('winding','assembly',('DOE2024_LPT_RESILIENCE',)),
    EvidenceEdge('assembly','testing',('DOE2022_GRID_DEEP_DIVE',)),
    EvidenceEdge('testing','qualified_lpt',('DOE2022_GRID_DEEP_DIVE',)),
)

UNKNOWN_NUMERIC_PARAMETERS = (
    'goes_mass_per_lpt','ctc_copper_mass_per_lpt','insulation_mass_per_lpt',
    'core_fabrication_units_per_year','winding_units_per_year',
    'assembly_units_per_year','compatible_test_bed_units_per_year',
)

def evidence_coverage():
    """Return what the public evidence can and cannot identify numerically."""
    return {
        'topology_identified': True,
        'numeric_path_model_identified': False,
        'measured_nodes': {n.id:n.measured for n in NODES if n.measured},
        'unknown_numeric_parameters': list(UNKNOWN_NUMERIC_PARAMETERS),
        'reason': ('DOE identifies material/component/stage topology and selected cost, lead-time, '
                   'testing-duration, and import-dependence facts, but not a mutually compatible set '
                   'of physical coefficients and stage capacities needed for an empirical path LP.'),
    }

def safe_knockout_claims():
    """Structural claims licensed by topology without inventing coefficients."""
    upstream={'goes','ctc_copper','insulation','core','winding','assembly','testing'}
    return {x:'structurally necessary in documented production path; effect size not identified'
            for x in sorted(upstream)}

# Additional primary/public evidence located in Run 021. These observations are kept
# at their native scope; they are NOT combined into a fictitious national factory.
ADDITIONAL_BOUNDED_EVIDENCE = {
    'typical_finished_lpt_weight_tons': {
        'bound': [110, 410],
        'scope': 'illustrative DOE/USITC table across selected 75-750 MVA designs',
        'evidence_id': 'USITC2024_PUB5531_TABLE_I5',
        'use': 'finished-equipment weight envelope only; not GOES/copper mass',
    },
    'siemens_charlotte_new_lpt_full_capacity_units_per_year': {
        'value': 57,
        'evidence_class': 'announced_future_full_capacity_target',
        'scope': 'Siemens Energy Charlotte facility at planned full capacity',
        'evidence_id': 'SIEMENS_ENERGY_CHARLOTTE_EXPANSION',
        'use': 'site-level finished LPT output capacity; not national or stage capacity',
    },
    'hitachi_varennes_capacity_multiplier_post_expansion': {
        'qualitative': 'nearly triple annual production capacity',
        'scope': 'Varennes site; relative expansion statement without a numeric baseline',
        'evidence_id': 'HITACHI_VARennes_2025_09_29',
        'use': 'qualitative relative site evidence only; do not translate nearly triple into a numeric interval',
    },
}

def partial_identification_example():
    """Demonstrate what current real evidence does—and does not—identify.

    The Charlotte finished-output observation is site-specific. Upstream stage
    capacities for that same site are not published in compatible units, so a full
    physical-path throughput remains [0, 57], not 57.
    """
    from radiant.engines.partial_identification import Bound, serial_throughput
    stages={
        'materials': Bound(0, float('inf'), 'unidentified compatible material throughput'),
        'core': Bound(0, float('inf'), 'unidentified Charlotte core capacity'),
        'winding': Bound(0, float('inf'), 'unidentified Charlotte winding capacity'),
        'assembly': Bound(0, float('inf'), 'unidentified Charlotte assembly capacity'),
        'qualified_output': Bound(0,57,'Siemens Charlotte announced future full-capacity target; achieved lower bound unknown'),
    }
    return serial_throughput(stages)

# DOE 2012 gives a physical core-steel coefficient for a bounded transformer class.
# It is not silently applied to Charlotte because the site's product-mix/MVA distribution
# is not established by the evidence currently in this repository.
CORE_STEEL_COEFFICIENT_300_500_MVA_KG = {
    'bound': [80000, 120000],
    'scope': 'power transformers rated 300-500 MVA',
    'evidence_id': 'DOE2012_LPT_STUDY_CORE_STEEL',
    'evidence_class': 'reported_reference_physical_coefficient',
}

def conditional_charlotte_core_steel_requirement():
    """Conditional calculation only: if all 57 annual units were 300-500 MVA.

    The condition is intentionally explicit because Charlotte's future product mix is
    not identified in the current evidence. Result is kg/year, not a claim of actual use.
    """
    from radiant.engines.partial_identification import Bound, coefficient_requirement
    output=Bound(57,57,'Siemens Charlotte announced future full-capacity target')
    coeff=Bound(80000,120000,'DOE 2012 reference for 300-500 MVA transformer core steel kg/unit')
    return coefficient_requirement(output,coeff)

def charlotte_information_requirements():
    """Expose why one more isolated measurement cannot identify Charlotte path throughput."""
    from radiant.engines.partial_identification import Bound, minimal_zero_lifting_measurement_set, measurement_set_analysis
    stages={
        'materials': Bound(0,float('inf'),'unidentified compatible material throughput'),
        'core': Bound(0,float('inf'),'unidentified Charlotte core capacity'),
        'winding': Bound(0,float('inf'),'unidentified Charlotte winding capacity'),
        'assembly': Bound(0,float('inf'),'unidentified Charlotte assembly capacity'),
        'qualified_output': Bound(0,57,'announced future full-capacity output; achieved lower bound unknown'),
    }
    needed=minimal_zero_lifting_measurement_set(stages)
    one=measurement_set_analysis(stages,('qualified_output',))
    return {'zero_lower_bound_stages': needed,
            'count': len(needed),
            'qualified_output_alone_lifts_lower_bound': one.sufficient_to_lift_zero_lower_bound,
            'interpretation': 'Every zero-lower-bound serial stage needs a positive evidence-backed lower bound; isolated output-capacity evidence cannot establish feasible path throughput.'}

# Run 023: a January 2026 DOE-funded NLR report supplies a *reference material
# model* for LPTs. These are explicit analytical assumptions, not measurements of
# Charlotte's future product mix or factory consumption. Keeping that distinction
# prevents a national planning heuristic from becoming a site-level observation.
NLR2026_LPT_REFERENCE_MODEL = {
    'weight_kg_per_mva': 600.0,
    'material_mass_fractions': {
        'steel_non_goes': 0.12,
        'goes': 0.48,
        'copper': 0.30,
        'other': 0.10,
    },
    'scope': 'reference analytical model for LPT material demand, generally >100 MVA',
    'evidence_id': 'NLR2026_TP_6A40_97167_TABLE3',
    'evidence_class': 'published_model_assumption',
}

def nlr2026_material_requirement(mva: float, units: float = 1.0):
    """Material demand implied by NLR's published reference assumptions.

    Returns kg by material. This is a scenario calculation, not a measured BOM.
    """
    if mva < 100:
        raise ValueError('NLR LPT reference model is scoped to transformers >=100 MVA')
    if units < 0:
        raise ValueError('units must be nonnegative')
    total = float(mva) * float(units) * NLR2026_LPT_REFERENCE_MODEL['weight_kg_per_mva']
    return {
        material: total * fraction
        for material, fraction in NLR2026_LPT_REFERENCE_MODEL['material_mass_fractions'].items()
    }

NLR2026_NATIONAL_SCENARIO = {
    'annual_transformer_units': {'AC': 1510, 'MT': 1370},
    'ten_year_transformer_material_thousand_tons': {
        'AC': {'steel_non_goes': 285, 'goes': 1140, 'copper': 710, 'other': 240},
        'MT': {'steel_non_goes': 235, 'goes': 940, 'copper': 590, 'other': 200},
    },
    'annual_all_transmission_material_thousand_tons': {
        'goes': [94, 114], 'copper': [61, 74], 'steel': [595, 693], 'aluminum': [174, 208],
    },
    'goes_share_of_2019_2023_apparent_consumption': 'more_than_45_percent',
    'evidence_id': 'NLR2026_TP_6A40_97167',
    'evidence_class': 'modeled_national_planning_scenario',
}

def charlotte_reference_material_scenarios(mva_values=(100, 300, 500, 700)):
    """Sensitivity envelope for 57 Charlotte units under explicit MVA scenarios.

    This intentionally returns separate scenarios rather than selecting or averaging a
    product mix that Siemens has not publicly identified.
    """
    return {int(mva): nlr2026_material_requirement(mva, 57) for mva in mva_values}

@dataclass(frozen=True)
class SupplyPressureBound:
    """Distribution-free implication of incremental material demand.

    This is deliberately not a shortage forecast.  If a modeled incremental demand D
    is known to exceed fraction f of a historical apparent-consumption baseline C,
    then D/C > f.  Absent displacement, inventory drawdown, recycling changes, or
    supply expansion, total requirements would therefore exceed (1+f)C.  No exact C
    is reverse-engineered from the inequality.
    """
    incremental_demand_thousand_tons: tuple[float, float]
    historical_window: tuple[int, int]
    incremental_share_lower_bound: float
    total_requirement_index_lower_bound: float
    shortage_identified: bool
    evidence_id: str
    interpretation: str


def nlr_goes_supply_pressure() -> SupplyPressureBound:
    """Conservative implication of NLR 2026 GOES demand vs 2019-23 consumption.

    NLR states 94--114 kt/y modeled transmission demand is *more than 45%* of
    average U.S. GOES apparent consumption in 2019--2023.  We preserve the strict
    lower bound rather than manufacturing the underlying consumption series.
    """
    return SupplyPressureBound(
        incremental_demand_thousand_tons=(94.0, 114.0),
        historical_window=(2019, 2023),
        incremental_share_lower_bound=0.45,
        total_requirement_index_lower_bound=1.45,
        shortage_identified=False,
        evidence_id='NLR2026_TP_6A40_97167_FIG10_USITC_APPARENT_CONSUMPTION',
        interpretation=(
            'Modeled transmission expansion adds GOES demand greater than 45% of the '
            '2019-2023 average apparent-consumption baseline. This establishes material '
            'pressure, not a shortage: supply can expand, imports can change, inventories '
            'can move, and other uses can be displaced. An empirical shortage claim '
            'requires vintage-aligned supply, trade, inventory, and competing-use data.'
        ),
    )
