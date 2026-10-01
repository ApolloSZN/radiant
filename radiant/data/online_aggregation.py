"""Causal online aggregation benchmark for forecasting experts (Run 027).

This module asks a narrow falsification question: can a generic online learner add
value beyond the strongest simple fixed-window trend baselines on the sequencing
series?  Every forecast at time t is formed only from expert losses observed before
t.  The current target outcome is revealed only after the aggregate forecast is
recorded.

The expert set is predeclared and intentionally includes the strong short-window
baselines that weakened the earlier Radiant headline:
  all-history, rolling 8/6/5/4/3, and no-change.

Two standard online formulations are reported without post-hoc hyperparameter
selection:
  * Follow-the-leader (FTL): after the first forecast, use the expert with the
    lowest mean absolute log loss observed so far. The first forecast is the
    equal-weight geometric mean because no expert has a loss history yet.
  * Exponential weights: mix expert log forecasts with weights proportional to
    exp(-eta_t * cumulative_loss), eta_t = sqrt(8 log(K) / t). This is a
    deterministic time-varying schedule; no eta is selected from the outcome.

These are retrospective benchmarks, not evidence that the algorithms would have
been chosen historically. Their purpose is to see whether "adaptive selection"
itself has demonstrated value on this dataset.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from radiant.data.backtest import Observation, fit_log_linear, predict
from radiant.data.robustness import paired_improvement_diagnostics

EXPERT_WINDOWS: tuple[int | None, ...] = (None, 8, 6, 5, 4, 3)
EXPERT_NAMES: tuple[str, ...] = (
    'all_history', 'rolling_8', 'rolling_6', 'rolling_5', 'rolling_4', 'rolling_3', 'no_change'
)


@dataclass(frozen=True)
class OnlineForecast:
    algorithm: str
    step: int
    predicted_log: float
    actual_log: float
    abs_log_error: float
    selected_expert: str | None
    weights: tuple[float, ...]


def _expert_log_predictions(obs: list[Observation], i: int) -> list[float]:
    train = obs[:i]
    target = obs[i]
    preds = [math.log(predict(fit_log_linear(train, w), target.date)) for w in EXPERT_WINDOWS]
    preds.append(math.log(obs[i - 1].value))
    return preds


def _history_update(histories: list[list[float]], preds: list[float], actual_log: float) -> None:
    for j, p in enumerate(preds):
        histories[j].append(abs(p - actual_log))


def follow_the_leader(obs: list[Observation], *, min_train: int = 8) -> list[OnlineForecast]:
    histories = [[] for _ in EXPERT_NAMES]
    out: list[OnlineForecast] = []
    k = len(EXPERT_NAMES)
    for step, i in enumerate(range(min_train, len(obs)), start=1):
        preds = _expert_log_predictions(obs, i)
        actual = math.log(obs[i].value)
        if step == 1:
            weights = np.ones(k, dtype=float) / k
            pred = float(np.dot(weights, preds))
            selected = None
        else:
            means = np.array([float(np.mean(h)) for h in histories])
            winner = int(np.argmin(means))
            weights = np.zeros(k, dtype=float)
            weights[winner] = 1.0
            pred = preds[winner]
            selected = EXPERT_NAMES[winner]
        out.append(OnlineForecast('follow_the_leader', step, pred, actual, abs(pred - actual), selected,
                                  tuple(float(x) for x in weights)))
        _history_update(histories, preds, actual)
    return out


def exponential_weights(obs: list[Observation], *, min_train: int = 8) -> list[OnlineForecast]:
    histories = [[] for _ in EXPERT_NAMES]
    out: list[OnlineForecast] = []
    k = len(EXPERT_NAMES)
    for step, i in enumerate(range(min_train, len(obs)), start=1):
        preds = _expert_log_predictions(obs, i)
        actual = math.log(obs[i].value)
        if step == 1:
            weights = np.ones(k, dtype=float) / k
        else:
            cumulative = np.array([sum(h) for h in histories], dtype=float)
            eta = math.sqrt(8.0 * math.log(k) / (step - 1))
            logits = -eta * cumulative
            logits -= logits.max()
            weights = np.exp(logits)
            weights /= weights.sum()
        pred = float(np.dot(weights, preds))
        out.append(OnlineForecast('exponential_weights', step, pred, actual, abs(pred - actual), None,
                                  tuple(float(x) for x in weights)))
        _history_update(histories, preds, actual)
    return out


def _fixed_expert_errors(obs: list[Observation], *, min_train: int = 8) -> dict[str, list[float]]:
    errors = {name: [] for name in EXPERT_NAMES}
    for i in range(min_train, len(obs)):
        preds = _expert_log_predictions(obs, i)
        actual = math.log(obs[i].value)
        for name, p in zip(EXPERT_NAMES, preds):
            errors[name].append(abs(p - actual))
    return errors


def online_aggregation_benchmark(obs: list[Observation], *, min_train: int = 8) -> dict:
    """Report the complete causal benchmark, including the negative result.

    The strongest fixed expert is selected only as an evaluation benchmark after
    all forecasts are generated. It is not used to form any FTL or exponential-
    weights forecast.
    """
    fixed = _fixed_expert_errors(obs, min_train=min_train)
    fixed_male = {k: float(np.mean(v)) for k, v in fixed.items()}
    strongest = min(fixed_male, key=fixed_male.get)
    strongest_err = fixed[strongest]

    alg_rows = []
    for name, rows in (
        ('follow_the_leader', follow_the_leader(obs, min_train=min_train)),
        ('exponential_weights', exponential_weights(obs, min_train=min_train)),
    ):
        errs = [r.abs_log_error for r in rows]
        diag = paired_improvement_diagnostics(strongest_err, errs)
        alg_rows.append({
            'algorithm': name,
            'male': float(np.mean(errs)),
            'strongest_fixed_baseline': strongest,
            'strongest_fixed_male': fixed_male[strongest],
            'relative_improvement_vs_strongest_fixed': diag['point_improvement'],
            'bootstrap_ci95': diag['bootstrap_ci95'],
            'robustly_beats_strongest_fixed': bool(diag['bootstrap_ci95'][0] > 0),
        })

    return {
        'schema': 'radiant.online_aggregation.v1',
        'n_paired_forecasts': len(strongest_err),
        'experts': list(EXPERT_NAMES),
        'fixed_expert_male': fixed_male,
        'strongest_fixed_baseline': strongest,
        'strongest_fixed_male': fixed_male[strongest],
        'algorithms': alg_rows,
        'any_online_algorithm_robustly_beats_strongest_fixed': any(
            r['robustly_beats_strongest_fixed'] for r in alg_rows
        ),
        'interpretation': (
            'Canonical causal online aggregation improves on the original Radiant selector, '
            'but does not establish an edge over the strongest predeclared short-window baseline. '
            'This is retained as a negative result rather than choosing a winning formulation after seeing outcomes.'
        ),
    }
