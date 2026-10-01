from radiant.data.lpt_evidence_network import nlr_goes_supply_pressure


def test_nlr_goes_pressure_preserves_only_source_identified_lower_bound():
    r = nlr_goes_supply_pressure()
    assert r.incremental_demand_thousand_tons == (94.0, 114.0)
    assert r.historical_window == (2019, 2023)
    assert r.incremental_share_lower_bound == 0.45
    assert r.total_requirement_index_lower_bound == 1.45
    assert r.shortage_identified is False


def test_pressure_result_does_not_claim_shortage_or_reconstruct_consumption():
    r = nlr_goes_supply_pressure()
    text = r.interpretation.lower()
    assert 'not a shortage' in text
    assert 'supply can expand' in text
