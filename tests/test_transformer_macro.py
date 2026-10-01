from radiant.data.transformer_macro import LPT2019Macro, domestic_capacity_counterfactual

def test_2019_accounting_identity_and_bound():
    m=LPT2019Macro(); r=domestic_capacity_counterfactual(m)
    assert m.apparent_consumption == 750
    assert .82 < m.import_share < .83
    assert abs(r['implied_nameplate_capacity']-342.5)<1e-9
    assert abs(r['unused_nameplate_capacity']-205.5)<1e-9
    assert abs(r['residual_imports_if_full_utilization']-411.5)<1e-9
