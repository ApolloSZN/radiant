from radiant.data.backtest import load_series
from radiant.data.eval_sensitivity import selector_specification_sensitivity


def test_selector_sensitivity_is_deterministic_and_complete():
    obs=load_series('data/nhgri/sequencing_costs_2001_2014.csv')
    kw=dict(min_train=8,baseline_window=None,candidate_window_sets=((None,8,4),(None,10,5)),warmups=(1,2),headline_threshold=.5)
    a=selector_specification_sensitivity(obs,**kw)
    b=selector_specification_sensitivity(obs,**kw)
    assert a==b
    assert a['n_specifications']==4
    assert len(a['rows'])==4
    assert 0 <= a['fraction_meeting_headline_threshold'] <= 1


def test_sensitivity_does_not_hide_losing_specifications():
    obs=load_series('data/battery/liion_pack_price_2010_2020.csv',value_col='pack_price_2020_usd_per_kwh')
    r=selector_specification_sensitivity(obs,min_train=5,baseline_window=5,
        candidate_window_sets=((None,5,3),(None,4,3),(None,6,3)),warmups=(1,2,3),headline_threshold=0.0)
    assert r['n_specifications']==9
    assert r['min_relative_improvement'] <= r['max_relative_improvement']
