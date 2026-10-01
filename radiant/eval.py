"""Ship-gate evaluation harness.

The release gate is deliberately stricter than the historical research log.  Run 026
showed that the earlier sequencing "77.5% better" headline depended on an easy
all-history baseline.  Run 027 therefore makes fair-baseline survival part of the
actual CI gate: a system that loses to a predeclared simple baseline cannot pass by
pointing to a weaker comparator.  Run 028 (ADR 006): a result that fails its gate is
WITHDRAWN -- published as a negative result and never asserted -- so it does not
block release, and it can only be re-claimed by passing the same fair gate.

Retrospective datasets remain labeled retrospective.  The strict BLS vintage replay
continues to test information-time integrity and is allowed to preserve a negative
predictive result.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import sys

from radiant.data.backtest import load_series, metrics, rolling_one_step, causal_model_selector
from radiant.data.vintage_eval import evaluate_bls_vintages, information_integrity_benchmark
from radiant.data.baseline_fairness import baseline_fairness_audit
from radiant.data.robustness import paired_improvement_diagnostics
from radiant.data.eval_sensitivity import selector_specification_sensitivity
from radiant.data.online_aggregation import online_aggregation_benchmark


@dataclass(frozen=True)
class EvalResult:
    name: str
    baseline: float
    system: float
    relative_improvement: float
    threshold: float
    passed: bool
    metric: str
    evidence_class: str
    note: str
    claim_status: str = 'claimed'  # 'claimed' | 'integrity' | 'withdrawn'


def _improvement(baseline: float, system: float) -> float:
    return (baseline - system) / baseline if baseline else 0.0


def forecasting_eval(root: str | Path = '.') -> list[EvalResult]:
    root = Path(root)
    seq = load_series(root / 'data/nhgri/sequencing_costs_2001_2014.csv')
    bat = load_series(root / 'data/battery/liion_pack_price_2010_2020.csv',
                      value_col='pack_price_2020_usd_per_kwh')

    seq_fair = baseline_fairness_audit(seq, min_train=8)
    seq_base = seq_fair['strongest_predeclared_baseline_male']
    seq_sys = seq_fair['system_male']

    bat_base = metrics(rolling_one_step(bat, 5, 5))['MALE']
    bat_sys = metrics(causal_model_selector(bat, 5, (None, 5, 3), 2)[0])['MALE']
    bls_path = root / 'data/bls_productivity_vintages.csv'
    bls = evaluate_bls_vintages(bls_path)
    integrity = information_integrity_benchmark(bls_path)

    return [
        EvalResult(
            'bitemporal_information_integrity_vs_latest_revision',
            float(integrity['baseline_future_information_violations']),
            float(integrity['system_future_information_violations']),
            float(integrity['relative_violation_reduction']), 1.0, bool(integrity['passed']),
            'future_information_violations', 'strict_historical_vintage',
            'Explicit baseline comparison: latest-revision reconstruction uses future BLS revisions at historical cutoffs; as-of reconstruction does not. Measures information integrity, not forecast accuracy.',
            'claimed',
        ),
        EvalResult(
            'sequencing_fair_baseline_gate', seq_base, seq_sys,
            _improvement(seq_base, seq_sys), 0.0, bool(seq_fair['fair_gate_passed']),
            'MALE', 'retrospective_real_data',
            'CI gate: the selector must robustly beat every baseline in the predeclared simple panel; '
            f"strongest observed panel baseline is {seq_fair['strongest_predeclared_baseline']}. "
            'Claim WITHDRAWN (ADR 006): reported as a negative result, not asserted.',
            'withdrawn',
        ),
        EvalResult(
            'battery_prequential_selector', bat_base, bat_sys, _improvement(bat_base, bat_sys),
            0.0, bat_sys <= bat_base, 'MALE', 'retrospective_real_data',
            'No-regression check against the predeclared rolling-5 baseline; small n (6) and a bootstrap '
            'interval crossing zero mean no advantage is claimed.',
            'withdrawn',
        ),
        EvalResult(
            'bls_strict_vintage_integrity', bls['baseline_mae'], bls['system_mae'], bls['relative_improvement'],
            -1.0, bls['strict_vintage_integrity'], 'MAE_pct_points', 'strict_historical_vintage',
            'Strict archived-release replay. Predictive correction is allowed to fail; this gate tests no-leak '
            'vintage integrity and preserves the negative result.',
            'integrity',
        ),
    ]


def release_decision(rows) -> dict:
    """ADR 006: a result may be asserted only if its gate passes.

    Rows marked 'claimed' or 'integrity' must pass. Rows marked 'withdrawn' are
    published as negative results and are never asserted, so they cannot block a
    release -- but they also cannot be re-claimed without passing their gate.
    """
    rows = [r if isinstance(r, dict) else asdict(r) for r in rows]
    blocking = [r['name'] for r in rows if r['claim_status'] in ('claimed', 'integrity') and not r['passed']]
    return {'release_ok': not blocking, 'blocking_failed_claims': blocking,
            'asserted': [r['name'] for r in rows if r['claim_status'] in ('claimed', 'integrity') and r['passed']],
            'withdrawn_negative_results': [r['name'] for r in rows if r['claim_status'] == 'withdrawn']}


def run_eval(root: str | Path = '.', output: str | Path | None = None) -> dict:
    root = Path(root)
    rows = forecasting_eval(root)
    seq = load_series(root / 'data/nhgri/sequencing_costs_2001_2014.csv')
    bat = load_series(root / 'data/battery/liion_pack_price_2010_2020.csv',
                      value_col='pack_price_2020_usd_per_kwh')

    seq_selector = causal_model_selector(seq, 8, (None, 8, 4), 2)[0]
    seq_all_history = rolling_one_step(seq, 8, None)
    bat_selector = causal_model_selector(bat, 5, (None, 5, 3), 2)[0]
    bat_roll5 = rolling_one_step(bat, 5, 5)

    seq_robust = paired_improvement_diagnostics(
        [abs(f.log_error) for f in seq_all_history],
        [abs(f.log_error) for f in seq_selector],
    )
    bat_robust = paired_improvement_diagnostics(
        [abs(f.log_error) for f in bat_roll5],
        [abs(f.log_error) for f in bat_selector],
    )
    seq_sensitivity = selector_specification_sensitivity(
        seq, min_train=8, baseline_window=None,
        candidate_window_sets=((None, 8, 4), (None, 10, 5), (None, 6, 3), (None, 12, 6)),
        warmups=(1, 2, 3, 4), headline_threshold=0.50,
    )
    bat_sensitivity = selector_specification_sensitivity(
        bat, min_train=5, baseline_window=5,
        candidate_window_sets=((None, 5, 3), (None, 4, 3), (None, 6, 3)),
        warmups=(1, 2, 3), headline_threshold=0.0,
    )
    fair = baseline_fairness_audit(seq, min_train=8)
    online = online_aggregation_benchmark(seq, min_train=8)

    report = {
        'schema': 'radiant.eval.v2',
        'all_passed': all(r.passed for r in rows),
        'release': release_decision(rows),
        'results': [asdict(r) for r in rows],
        'diagnostics': {
            'legacy_all_history_sequencing_improvement': _improvement(
                metrics(seq_all_history)['MALE'], metrics(seq_selector)['MALE']
            ),
            'legacy_all_history_note': (
                'Retained for historical comparability only; it is not the ship-gate comparator after Run 026.'
            ),
        },
        'robustness': {'sequencing_vs_all_history': seq_robust, 'battery': bat_robust},
        'specification_sensitivity': {'sequencing_vs_all_history': seq_sensitivity, 'battery': bat_sensitivity},
        'baseline_fairness': {'sequencing': fair},
        'online_aggregation': {'sequencing': online},
        'limitations': [
            'The sequencing and battery datasets are retrospective real-data evaluations; the BLS row is a separate strict historical-vintage replay.',
            'The BLS revision-correction model underperforms its no-correction baseline; passing certifies information-time integrity, not predictive superiority.',
            'The 77.5% sequencing number is retained only as a legacy comparison against the all-history baseline. The selector loses to stronger predeclared short-window baselines, so the claim is withdrawn (ADR 006).',
            'Canonical online aggregation (follow-the-leader and exponential weights) improves on the old selector but still does not robustly beat the strongest fixed short-window baseline.',
            'Passing any forecasting diagnostic would not by itself establish causal intervention validity.',
        ],
    }
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    report = run_eval('.', 'artifacts/eval_report.json')
    print(json.dumps(report, indent=2))
    # Report-only is useful for one-command reproduction before the ship gate passes.
    # CI invokes --strict so scientific gate failures make the workflow fail closed.
    strict = '--strict' in sys.argv
    raise SystemExit(1 if strict and not report['release']['release_ok'] else 0)
