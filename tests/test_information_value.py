from radiant.engines.partial_identification import Bound, minimal_zero_lifting_measurement_set, measurement_set_analysis, coefficient_requirement
from radiant.data.lpt_evidence_network import conditional_charlotte_core_steel_requirement, charlotte_information_requirements

def test_zero_lifting_set_requires_every_zero_lower_stage():
    s={'a':Bound(0,10),'b':Bound(2,8),'c':Bound(0,7)}
    assert minimal_zero_lifting_measurement_set(s)==('a','c')

def test_single_measurement_does_not_fake_identification():
    s={'a':Bound(0,10),'b':Bound(0,8),'out':Bound(0,7)}
    r=measurement_set_analysis(s,('out',))
    assert r.lower_bound_if_upper_realized == 0
    assert not r.sufficient_to_lift_zero_lower_bound

def test_physical_coefficient_interval_propagates_without_midpoint():
    r=coefficient_requirement(Bound(57,57),Bound(80000,120000))
    assert r.low == 4_560_000
    assert r.high == 6_840_000

def test_charlotte_core_steel_is_explicitly_conditional():
    r=conditional_charlotte_core_steel_requirement()
    assert (r.low,r.high)==(4_560_000,6_840_000)
    info=charlotte_information_requirements()
    assert info['count']==5
    assert not info['qualified_output_alone_lifts_lower_bound']
