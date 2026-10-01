from datetime import date
from pathlib import Path
from radiant.data.backtest import *
P=Path('data/nhgri/sequencing_costs_2001_2014.csv')
def test_ingest_and_provenance():
    x=load_series(P); assert len(x)==47; assert all(o.value>0 for o in x); assert all(o.source_tier=='T0' for o in x)
def test_bitemporal_visibility_blocks_future_recording():
    x=load_series(P); assert visible_as_of(x,date(2010,1,1))==[]  # transcription recorded 2014, cannot leak into 2010 replay
    assert len(visible_as_of(x,date(2014,4,30)))==47
def test_backtest_runs_and_regime_shift_hurts_global_fit():
    x=load_series(P); g=metrics(rolling_one_step(x,8,None)); r=metrics(rolling_one_step(x,8,8))
    assert g['n']==39 and r['n']==39
    assert r['MALE'] < g['MALE']
def test_known_threshold_crossings():
    x=load_series(P)
    assert first_crossing(x,100000)==date(2009,10,1)
    assert first_crossing(x,10000)==date(2011,10,1)
def test_probabilistic_crossing_scoring_is_finite():
    x=load_series(P); rows=crossing_forecasts(x,100000,8,8); s=score_binary(rows)
    assert s['n']==39 and 0 <= s['brier'] <= 1 and s['log_score'] >= 0

def test_historical_vintage_anchors_are_causal():
    a=load_vintage_anchors('data/nhgri/historical_vintage_anchors.csv')
    assert len(a)==5
    assert len(historical_vintage_as_of(a,date(2009,12,31)))==1
    assert len(historical_vintage_as_of(a,date(2011,1,1)))==3
    assert all(r.source_available_at <= date(2011,1,1) for r in historical_vintage_as_of(a,date(2011,1,1)))

def test_break_detector_has_no_lookahead_and_fires_in_ngs_transition():
    x=load_series(P); s=sequential_break_scores(x,8,8,2.0)
    assert len(s)==39
    transition=[r for r in s if date(2008,1,1)<=r['target']<=date(2010,12,31) and r['break']]
    assert transition
    assert all(r['cutoff'] < r['target'] for r in s)

def test_adaptive_forecaster_is_reproducible_and_finite():
    x=load_series(P); a=adaptive_one_step(x,8,8,2.0,4); b=adaptive_one_step(x,8,8,2.0,4)
    assert a==b and len(a)==39
    assert metrics(a)['MALE'] >= 0

BAT=Path('data/battery/liion_pack_price_2010_2020.csv')
def test_second_domain_battery_ingests_with_explicit_retrospective_vintage():
    x=load_series(BAT,value_col='pack_price_2020_usd_per_kwh')
    assert len(x)==11 and x[0].value==1191 and x[-1].value==137
    assert visible_as_of(x,date(2020,12,31))==[]
    assert len(visible_as_of(x,date(2021,4,1)))==11

def test_same_forecasting_contract_runs_on_battery_without_domain_changes():
    x=load_series(BAT,value_col='pack_price_2020_usd_per_kwh')
    m=compare_forecasters(x,min_train=5,rolling_window=5,z_threshold=2.0,post_break_window=3)
    assert set(m)=={'all_history','rolling_5','adaptive'}
    assert all(v['n']==6 and v['MALE']>=0 for v in m.values())

def test_causal_model_selector_is_reproducible_and_never_uses_current_outcome_for_choice():
    x=load_series(P); a,ca=causal_model_selector(x,8,(None,8,4),2); b,cb=causal_model_selector(x,8,(None,8,4),2)
    assert a==b and ca==cb and len(a)==39
    # Altering final outcome cannot alter the model choice made before that outcome is observed.
    from dataclasses import replace
    y=x[:-1]+[replace(x[-1],value=x[-1].value*100)]
    _,cy=causal_model_selector(y,8,(None,8,4),2)
    assert ca[-1]==cy[-1]

def test_compute_domain_is_real_but_retrospective_and_cannot_fake_vintage_replay():
    x=load_compute_series('data/compute/leading_ai_gpu_price_performance.csv')
    assert len(x)==4 and x[0].value==1.3e9 and x[-1].value==2.2e10
    assert visible_as_of(x,date(2022,12,31))==[]
    assert len(visible_as_of(x,date(2024,10,23)))==4
