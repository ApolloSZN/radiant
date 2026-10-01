from radiant.data.transformer_case import lpt_scenario
from radiant.engines.uncertain_constraints import Interval, uncertainty_scan

def test_uncertainty_scan_is_reproducible_and_bounded():
    s=lpt_scenario(); caps={p.id:Interval(.5,1.2) for p in s.processes}; imps={x:Interval(.7,1.5) for x in s.import_limits}
    a=uncertainty_scan(s,caps,imps,n=80,seed=7); b=uncertainty_scan(s,caps,imps,n=80,seed=7)
    assert a.throughput_median==b.throughput_median
    assert a.throughput_q05 <= a.throughput_median <= a.throughput_q95
    assert abs(sum(a.top_intervention_probability.values())-1)<1e-9

def test_narrow_known_bottleneck_yields_robust_intervention():
    s=lpt_scenario()
    caps={'core_fabrication':Interval(1,1.1),'winding':Interval(.9,1.0),'insulation_prep':Interval(1,1.1),'assembly':Interval(.8,.9),'test_and_qualification':Interval(.55,.60)}
    imps={x:Interval(1.1,1.4) for x in s.import_limits}
    r=uncertainty_scan(s,caps,imps,n=60,seed=2)
    assert r.top_intervention_probability['capacity:test_and_qualification'] > .95
    assert r.positive_gain_probability['import:goes']==0

def test_measurement_priority_finds_uncertain_binding_stage():
    s=lpt_scenario()
    caps={'core_fabrication':Interval(1,1.01),'winding':Interval(1,1.01),'insulation_prep':Interval(1,1.01),'assembly':Interval(1,1.01),'test_and_qualification':Interval(.3,1.0)}
    r=uncertainty_scan(s,caps,{},n=120,seed=4)
    assert r.measurement_priority[0]['parameter']=='test_and_qualification'


def test_partial_identification_refuses_fake_unique_bottleneck():
    from radiant.engines.partial_identification import partial_identification
    from radiant.engines.viability import FlowProcess
    from radiant.engines.constraint_resolution import ProductionSystem
    ps=(FlowProcess('a',{'ore':1},{'mid':1},capacity=1),FlowProcess('b',{'mid':1},{'out':1},capacity=1))
    s=ProductionSystem(ps,{'ore':1},'out')
    iv={'a':Interval(.5,1.5),'b':Interval(.5,1.5)}
    r=partial_identification(s,iv,{'ore':Interval(.5,1.5)})
    assert r.identified_best is None
    assert r.throughput_low == .5 and r.throughput_high == 1.5


def test_partial_identification_can_certify_bottleneck():
    from radiant.engines.partial_identification import partial_identification
    from radiant.engines.viability import FlowProcess
    from radiant.engines.constraint_resolution import ProductionSystem
    ps=(FlowProcess('a',{'ore':1},{'mid':1},capacity=1),FlowProcess('b',{'mid':1},{'out':1},capacity=1))
    s=ProductionSystem(ps,{'ore':10},'out')
    r=partial_identification(s,{'a':Interval(.5,.6),'b':Interval(2,3)}, {})
    assert r.identified_best == 'capacity:a'
    row=next(x for x in r.interventions if x.intervention=='capacity:a')
    assert row.robust_positive
