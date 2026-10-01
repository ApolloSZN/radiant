from pathlib import Path

from radiant.eval import run_eval, release_decision


def test_fair_gate_still_fails_but_claim_is_withdrawn_not_asserted(tmp_path):
    r = run_eval('.', tmp_path / 'eval.json')
    assert r['all_passed'] is False  # the raw scientific result is unchanged
    seq = next(x for x in r['results'] if x['name'] == 'sequencing_fair_baseline_gate')
    assert seq['passed'] is False and seq['claim_status'] == 'withdrawn'
    assert seq['relative_improvement'] < 0
    assert r['baseline_fairness']['sequencing']['strongest_predeclared_baseline'] == 'rolling_3'
    assert r['online_aggregation']['sequencing']['any_online_algorithm_robustly_beats_strongest_fixed'] is False
    assert r['release']['release_ok'] is True
    assert 'sequencing_fair_baseline_gate' in r['release']['withdrawn_negative_results']
    assert 'sequencing_fair_baseline_gate' not in r['release']['asserted']


def test_reclaiming_a_failed_result_blocks_release():
    rows = [{'name': 'x', 'passed': False, 'claim_status': 'claimed'},
            {'name': 'y', 'passed': True, 'claim_status': 'integrity'}]
    d = release_decision(rows)
    assert d['release_ok'] is False and d['blocking_failed_claims'] == ['x']
    rows[1]['passed'] = False
    assert release_decision(rows)['blocking_failed_claims'] == ['x', 'y']


def test_withdrawn_forecasting_claim_is_disclaimed_in_readme():
    assert 'Not a proven forecasting advantage' in Path('README.md').read_text()


def test_ci_enforces_strict_eval_mode():
    ci = Path('.github/workflows/ci.yml').read_text()
    assert 'bash scripts/reproduce.sh' in ci
    assert 'python -m radiant.eval --strict' in Path('scripts/reproduce.sh').read_text()
