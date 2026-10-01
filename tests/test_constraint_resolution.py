from dataclasses import replace
from radiant.engines.constraint_resolution import maximize_throughput, intervention_scan
from radiant.data.transformer_case import lpt_scenario

def test_throughput_is_bottlenecked_by_test_capacity_in_scenario():
    s=lpt_scenario(); r=maximize_throughput(s)
    assert r.feasible and abs(r.throughput-.72)<1e-8

def test_scan_finds_only_relaxations_that_can_move_current_bottleneck():
    rows=intervention_scan(lpt_scenario(),.20)
    assert rows[0]['intervention']=='capacity:test_and_qualification'
    assert rows[0]['gain'] > 0
    assert next(x for x in rows if x['intervention']=='import:goes')['gain']==0

def test_bottleneck_migrates_after_relaxation():
    s=lpt_scenario(); ps=list(s.processes)
    p=ps[-1]; ps[-1]=replace(p,capacity=1.0)
    r=maximize_throughput(replace(s,processes=tuple(ps)))
    assert abs(r.throughput-.78)<1e-8

def test_evidence_binding_is_explicit_not_numeric_fabrication():
    s=lpt_scenario(); rows=intervention_scan(s)
    q=next(x for x in rows if x['intervention']=='capacity:test_and_qualification')
    assert 'DOE2014_CUSTOM' in q['evidence_ids']
