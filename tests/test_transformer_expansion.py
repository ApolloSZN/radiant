from radiant.data.transformer_expansion import *

def test_siemens_disclosed_addition_does_not_close_2019_scale_gap_under_optimistic_bound():
    s=CapacityAddition('Siemens Charlotte full rate',57,2027,'SIEMENS2024_CHARLOTTE','LPT')
    r=optimistic_capacity_sufficiency(year=2027,demand_units=750,legacy_nameplate_units=342.5,
        additions=[s],definition_compatible=True)
    assert r.optimistic_domestic_capacity == 399.5
    assert r.residual_external_supply_required == 350.5
    assert round(r.domestic_capacity_share_upper_bound,4)==0.5327

def test_2027_doe_demand_cross_definition_is_scenario_not_identified_claim():
    s=CapacityAddition('Siemens Charlotte full rate',57,2027,'SIEMENS2024_CHARLOTTE','LPT')
    r=optimistic_capacity_sufficiency(year=2027,demand_units=900,legacy_nameplate_units=342.5,
        additions=[s],definition_compatible=False)
    assert r.residual_external_supply_required == 500.5
    assert not r.definition_compatible
    assert 'Scenario only' in r.interpretation

def test_minimum_incremental_capacity_bound():
    assert minimum_additional_capacity_required(demand_units=750,legacy_nameplate_units=342.5,known_additions_units=57)==350.5
