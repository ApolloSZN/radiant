from radiant.data.event_study import evaluate_panel

def _panel(diverging=False, placebo=False):
    rows=[]
    for t in [-3,-2,-1,0,1,2]:
        control=10+t
        treated=12+t
        if diverging and t<0: treated=12+2*t
        if placebo and t==-1: treated+=4
        if t>=0: treated+=5
        rows += [dict(group='control',rel_time=t,outcome=control),dict(group='treated',rel_time=t,outcome=treated)]
    return rows

def test_clean_parallel_panel_identifies_known_effect():
    r=evaluate_panel(_panel(),pretrend_tolerance=.01,placebo_tolerance=1.0)
    assert r.identified and abs(r.did_effect-5)<1e-9

def test_pretrend_failure_blocks_identification():
    r=evaluate_panel(_panel(diverging=True),pretrend_tolerance=.1,placebo_tolerance=2)
    assert not r.pretrend_pass and not r.identified

def test_placebo_failure_blocks_identification():
    r=evaluate_panel(_panel(placebo=True),pretrend_tolerance=2,placebo_tolerance=.5)
    assert not r.placebo_pass and not r.identified
