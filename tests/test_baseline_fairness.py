from radiant.data.backtest import load_series
from radiant.data.baseline_fairness import baseline_fairness_audit
from radiant.eval import run_eval


def _seq():
    return load_series('data/nhgri/sequencing_costs_2001_2014.csv')


def test_fairness_audit_is_deterministic_and_reports_full_panel():
    a = baseline_fairness_audit(_seq()); b = baseline_fairness_audit(_seq())
    assert a == b
    names = [r['baseline'] for r in a['rows']]
    assert names == ['all_history', 'rolling_8', 'rolling_6', 'rolling_5', 'rolling_4', 'rolling_3', 'no_change']
    assert a['n_paired_forecasts'] == 39


def test_headline_does_not_survive_fair_baselines_and_negative_result_is_preserved():
    r = baseline_fairness_audit(_seq())
    rows = {x['baseline']: x for x in r['rows']}
    # The published headline is real against the weak baseline...
    assert rows['all_history']['robust_win'] and rows['all_history']['point_improvement'] > 0.75
    # ...but not against a simple 5-point rolling fit, and it loses to shorter windows.
    assert not rows['rolling_5']['robust_win']
    assert rows['rolling_4']['selector_loses'] and rows['rolling_3']['selector_loses']
    assert r['headline_survives_all_simple_baselines'] is False


def test_eval_report_carries_fairness_audit(tmp_path):
    rep = run_eval('.', tmp_path / 'eval.json')
    assert rep['baseline_fairness']['sequencing']['headline_survives_all_simple_baselines'] is False
    assert any('all-history baseline' in x for x in rep['limitations'])
