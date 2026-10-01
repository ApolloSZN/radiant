"""Deterministic robustness diagnostics for paired forecast comparisons.

These diagnostics quantify sampling fragility without changing evidence class.
A bootstrap over retrospective errors remains retrospective evidence.
"""
from __future__ import annotations
import numpy as np


def paired_improvement_diagnostics(baseline_errors, system_errors, *, draws=10000, seed=20260929):
    b=np.asarray(baseline_errors,dtype=float); s=np.asarray(system_errors,dtype=float)
    if b.shape != s.shape or b.ndim != 1 or len(b)<3:
        raise ValueError('paired one-dimensional errors with n>=3 required')
    if np.any(b<0) or np.any(s<0):
        raise ValueError('errors must be nonnegative')
    def imp(bb,ss):
        mb=float(np.mean(bb)); ms=float(np.mean(ss))
        return (mb-ms)/mb if mb else 0.0
    point=imp(b,s)
    rng=np.random.default_rng(seed)
    samples=np.empty(draws)
    for j in range(draws):
        idx=rng.integers(0,len(b),len(b))
        samples[j]=imp(b[idx],s[idx])
    loo=[]
    for i in range(len(b)):
        keep=np.arange(len(b))!=i
        loo.append(imp(b[keep],s[keep]))
    return {
        'n':int(len(b)), 'point_improvement':point,
        'paired_bootstrap_draws':int(draws), 'seed':int(seed),
        'bootstrap_ci95':[float(x) for x in np.quantile(samples,[0.025,0.975])],
        'p_improvement_gt_0':float(np.mean(samples>0)),
        'p_improvement_ge_50pct':float(np.mean(samples>=0.5)),
        'leave_one_out_min_improvement':float(min(loo)),
        'leave_one_out_max_improvement':float(max(loo)),
        'interpretation':'Sampling robustness diagnostic only; does not upgrade retrospective evidence to historical-vintage evidence.'
    }
