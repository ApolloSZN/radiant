import pytest
from radiant.data.lpt_evidence_network import (
    NLR2026_LPT_REFERENCE_MODEL, NLR2026_NATIONAL_SCENARIO,
    nlr2026_material_requirement, charlotte_reference_material_scenarios,
)

def test_nlr_reference_model_reproduces_material_shares():
    r=nlr2026_material_requirement(100)
    assert r['goes'] == pytest.approx(28_800)
    assert r['copper'] == pytest.approx(18_000)
    assert sum(r.values()) == pytest.approx(60_000)
    assert NLR2026_LPT_REFERENCE_MODEL['evidence_class'] == 'published_model_assumption'

def test_reference_model_rejects_out_of_scope_small_transformers():
    with pytest.raises(ValueError):
        nlr2026_material_requirement(99)

def test_charlotte_product_mix_remains_scenario_not_measurement():
    s=charlotte_reference_material_scenarios()
    assert set(s) == {100,300,500,700}
    assert s[700]['goes'] == pytest.approx(11_491_200)
    assert s[100]['goes'] == pytest.approx(1_641_600)

def test_national_scenario_preserves_modeled_evidence_class():
    n=NLR2026_NATIONAL_SCENARIO
    assert n['annual_transformer_units']['AC'] == 1510
    assert n['annual_all_transmission_material_thousand_tons']['goes'] == [94,114]
    assert n['evidence_class'] == 'modeled_national_planning_scenario'
