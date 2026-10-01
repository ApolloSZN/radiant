from math import inf
from radiant.engines.partial_identification import Bound, serial_throughput, knockout_bound, capacity_multiplier
from radiant.data.lpt_evidence_network import partial_identification_example, ADDITIONAL_BOUNDED_EVIDENCE

def test_unknown_stage_prevents_false_positive_lower_bound():
    r=serial_throughput({'a':Bound(10,10,'measured'),'b':Bound(0,inf,'unknown')})
    assert r.low == 0 and r.high == 10 and not r.identified

def test_serial_bounds_and_knockout():
    caps={'a':Bound(8,10,'a'),'b':Bound(6,9,'b'),'c':Bound(7,12,'c')}
    r=serial_throughput(caps)
    assert (r.low,r.high)==(6,9)
    ko=knockout_bound(caps,'c')
    assert ko.low == ko.high == 0 and ko.identified

def test_multiplier_propagates_interval_not_midpoint():
    x=capacity_multiplier(Bound(20,30,'base'),Bound(1.5,2.0,'expansion'))
    assert (x.low,x.high)==(30,60)

def test_real_lpt_partial_identification_stays_wide():
    r=partial_identification_example()
    assert r.low == 0 and r.high == 57 and not r.identified
    assert ADDITIONAL_BOUNDED_EVIDENCE['siemens_charlotte_new_lpt_full_capacity_units_per_year']['value']==57
