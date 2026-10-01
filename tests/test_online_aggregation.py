from pathlib import Path

from radiant.data.backtest import load_series
from radiant.data.online_aggregation import (
    EXPERT_NAMES,
    exponential_weights,
    follow_the_leader,
    online_aggregation_benchmark,
)


def _seq():
    return load_series(Path('data/nhgri/sequencing_costs_2001_2014.csv'))


def test_online_algorithms_are_deterministic_and_causal_shape():
    obs = _seq()
    f1, f2 = follow_the_leader(obs), follow_the_leader(obs)
    e1, e2 = exponential_weights(obs), exponential_weights(obs)
    assert f1 == f2 and e1 == e2
    assert len(f1) == len(e1) == 39
    assert len(f1[0].weights) == len(EXPERT_NAMES)
    assert abs(sum(f1[0].weights) - 1.0) < 1e-12
    assert abs(sum(e1[-1].weights) - 1.0) < 1e-12


def test_online_aggregation_does_not_rescue_forecasting_headline():
    r = online_aggregation_benchmark(_seq())
    assert r['strongest_fixed_baseline'] == 'rolling_3'
    assert r['any_online_algorithm_robustly_beats_strongest_fixed'] is False
    rows = {x['algorithm']: x for x in r['algorithms']}
    # They improve on the old selector's 0.1762 MALE, but not on rolling-3.
    assert rows['follow_the_leader']['male'] < 0.1762
    assert rows['exponential_weights']['male'] < 0.1762
    assert rows['follow_the_leader']['male'] > r['strongest_fixed_male']
    assert rows['exponential_weights']['male'] > r['strongest_fixed_male']
