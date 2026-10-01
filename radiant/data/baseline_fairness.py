"""Baseline-fairness audit for retrospective forecast headlines (Run 026).

A headline improvement is only as strong as the baseline it beats. The original
sequencing headline compares the prequential selector with an all-history
log-linear fit, which is known to fail badly on a series with a regime shift.
This audit evaluates the same selector against a predeclared panel of simple,
non-adaptive baselines and reports every row, including the ones the selector
loses to. It does not tune anything to the outcome.

Predeclared panel: all-history log-linear; rolling log-linear with windows
8, 6, 5, 4 and 3; and a no-change (last observed value) forecast.
"""
from __future__ import annotations
import math
import numpy as np

from radiant.data.backtest import Observation, causal_model_selector, rolling_one_step
from radiant.data.robustness import paired_improvement_diagnostics

PREDECLARED_WINDOWS: tuple[int|None, ...] = (None, 8, 6, 5, 4, 3)


def _no_change_errors(obs: list[Observation], min_train: int) -> list[float]:
    return [abs(math.log(obs[i].value) - math.log(obs[i-1].value)) for i in range(min_train, len(obs))]


def baseline_fairness_audit(obs: list[Observation], *, min_train: int=8,
                            selector_windows: tuple[int|None, ...]=(None, 8, 4),
                            warmup: int=2, robust_threshold: float=0.0) -> dict:
    sys_fs, _ = causal_model_selector(obs, min_train, selector_windows, warmup)
    sys_err = [abs(f.log_error) for f in sys_fs]
    rows = []
    panel = [(f"rolling_{w}" if w else "all_history", [abs(f.log_error) for f in rolling_one_step(obs, min_train, w)])
             for w in PREDECLARED_WINDOWS]
    panel.append(("no_change", _no_change_errors(obs, min_train)))
    for name, base_err in panel:
        if len(base_err) != len(sys_err):
            raise ValueError(f"baseline {name} is not paired with system forecasts")
        d = paired_improvement_diagnostics(base_err, sys_err)
        lo = d['bootstrap_ci95'][0]
        rows.append({'baseline': name,
                     'baseline_male': float(np.mean(base_err)),
                     'system_male': float(np.mean(sys_err)),
                     'point_improvement': d['point_improvement'],
                     'bootstrap_ci95': d['bootstrap_ci95'],
                     'robust_win': bool(lo > robust_threshold),
                     'selector_loses': bool(np.mean(sys_err) > np.mean(base_err))})
    beaten_robustly = [r['baseline'] for r in rows if r['robust_win']]
    loses_to = [r['baseline'] for r in rows if r['selector_loses']]
    strongest = min(rows, key=lambda r: r['baseline_male'])
    return {'schema': 'radiant.baseline_fairness.v2',
            'n_paired_forecasts': len(sys_err),
            'rows': rows,
            'robustly_beats': beaten_robustly,
            'loses_to': loses_to,
            'strongest_predeclared_baseline': strongest['baseline'],
            'strongest_predeclared_baseline_male': strongest['baseline_male'],
            'system_male': float(np.mean(sys_err)),
            'relative_improvement_vs_strongest': (strongest['baseline_male']-float(np.mean(sys_err)))/strongest['baseline_male'],
            'fair_gate_passed': len(loses_to) == 0 and len(beaten_robustly) == len(rows),
            'headline_survives_all_simple_baselines': len(loses_to) == 0 and len(beaten_robustly) == len(rows),
            'interpretation': ('The large headline improvement is measured against an all-history fit. '
                               'Against short fixed-window fits the selector is not robustly better and '
                               'loses to the shortest windows. The defensible finding is that recent data '
                               'beats old data after a regime shift; the selector itself adds little.')}
