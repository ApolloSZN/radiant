"""Specification-sensitivity diagnostics for retrospective forecast claims.

These diagnostics do not search for a winning specification. They evaluate a
predeclared grid of plausible selector hyperparameters against the same baseline
and report how often the headline direction survives. This is a robustness audit,
not an evidence-class upgrade.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from itertools import product
import math
import numpy as np

from radiant.data.backtest import Observation, causal_model_selector, metrics, rolling_one_step

@dataclass(frozen=True)
class SensitivityRow:
    windows: tuple[int|None, ...]
    warmup_predictions: int
    system_male: float
    relative_improvement: float


def selector_specification_sensitivity(
    obs: list[Observation],
    *,
    min_train: int,
    baseline_window: int|None,
    candidate_window_sets: tuple[tuple[int|None, ...], ...],
    warmups: tuple[int, ...]=(1,2,3,4),
    headline_threshold: float=0.0,
) -> dict:
    base_fs=rolling_one_step(obs,min_train,baseline_window)
    baseline=metrics(base_fs)['MALE']
    rows=[]
    for windows,warmup in product(candidate_window_sets,warmups):
        fs,_=causal_model_selector(obs,min_train,windows,warmup)
        sys=metrics(fs)['MALE']
        imp=(baseline-sys)/baseline if baseline else 0.0
        rows.append(SensitivityRow(tuple(windows),warmup,sys,imp))
    vals=np.array([r.relative_improvement for r in rows],dtype=float)
    return {
        'n_specifications':len(rows),
        'baseline_male':baseline,
        'min_relative_improvement':float(vals.min()),
        'median_relative_improvement':float(np.median(vals)),
        'max_relative_improvement':float(vals.max()),
        'fraction_improving':float(np.mean(vals>0)),
        'fraction_meeting_headline_threshold':float(np.mean(vals>=headline_threshold)),
        'headline_threshold':headline_threshold,
        'rows':[asdict(r) for r in rows],
        'interpretation':'Predeclared specification-sensitivity audit only; does not upgrade retrospective evidence or justify selecting the best row after seeing outcomes.'
    }
