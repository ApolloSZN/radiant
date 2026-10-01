from radiant.data.vintage_eval import load_bls_vintages, revision_prequential, evaluate_bls_vintages

def test_strict_vintage_forecasts_use_only_prior_revisions():
    rows=load_bls_vintages('data/bls_productivity_vintages.csv')
    fs=revision_prequential(rows)
    assert fs and all(f['cutoff'] < f['target_release'] for f in fs)
    assert all(f['known_revision_n'] >= 2 for f in fs)

def test_strict_vintage_negative_result_is_preserved():
    r=evaluate_bls_vintages('data/bls_productivity_vintages.csv')
    assert r['strict_vintage_integrity']
    assert r['n'] >= 5
    assert r['system_mae'] >= 0

def test_information_integrity_benchmark_eliminates_future_revision_leakage():
    from radiant.data.vintage_eval import information_integrity_benchmark
    r = information_integrity_benchmark('data/bls_productivity_vintages.csv')
    assert r['n_cutoffs'] == 9
    assert r['baseline_future_information_violations'] == 9
    assert r['system_future_information_violations'] == 0
    assert r['relative_violation_reduction'] == 1.0
    assert r['passed'] is True
