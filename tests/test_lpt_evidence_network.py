from radiant.data.lpt_evidence_network import evidence_coverage, safe_knockout_claims, UNKNOWN_NUMERIC_PARAMETERS

def test_real_lpt_slice_refuses_fake_numeric_parameterization():
    c=evidence_coverage()
    assert c['topology_identified'] is True
    assert c['numeric_path_model_identified'] is False
    assert 'goes_mass_per_lpt' in c['unknown_numeric_parameters']
    assert len(UNKNOWN_NUMERIC_PARAMETERS) >= 7

def test_structural_knockouts_are_not_effect_sizes():
    claims=safe_knockout_claims()
    assert 'goes' in claims and 'testing' in claims
    assert all('effect size not identified' in x for x in claims.values())
