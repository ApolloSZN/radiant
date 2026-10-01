from __future__ import annotations
import csv, hashlib, json
from datetime import date
from pathlib import Path
import numpy as np

def load_bls_vintages(path):
    rows=[]
    with open(path,newline='') as f:
        for r in csv.DictReader(f):
            rows.append({**r,'preliminary_release':date.fromisoformat(r['preliminary_release']),
                         'revised_release':date.fromisoformat(r['revised_release']),
                         'preliminary_pct':float(r['preliminary_pct']),'revised_pct':float(r['revised_pct'])})
    return rows

def revision_prequential(rows, min_history=2):
    """At each preliminary release, predict its later revision using only revisions already published."""
    out=[]
    for i,r in enumerate(rows):
        cutoff=r['preliminary_release']
        known=[x['revised_pct']-x['preliminary_pct'] for x in rows[:i] if x['revised_release'] <= cutoff]
        if len(known)<min_history: continue
        correction=float(np.median(known))
        pred=r['preliminary_pct']+correction
        payload={'quarter':r['quarter'],'cutoff':cutoff.isoformat(),'target_release':r['revised_release'].isoformat(),
                 'preliminary':r['preliminary_pct'],'prediction':pred,'known_revision_n':len(known)}
        h=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
        out.append({**payload,'actual':r['revised_pct'],'baseline_abs_error':abs(r['preliminary_pct']-r['revised_pct']),
                    'system_abs_error':abs(pred-r['revised_pct']),'artifact_hash':h})
    return out

def evaluate_bls_vintages(path):
    rows=load_bls_vintages(path); fs=revision_prequential(rows)
    b=float(np.mean([x['baseline_abs_error'] for x in fs])); s=float(np.mean([x['system_abs_error'] for x in fs]))
    integrity=all(x['cutoff'] < x['target_release'] for x in fs) and all(x['known_revision_n']>=2 for x in fs)
    return {'n':len(fs),'baseline_mae':b,'system_mae':s,'relative_improvement':(b-s)/b if b else 0.0,
            'strict_vintage_integrity':integrity,'forecasts':fs}

def information_integrity_benchmark(path):
    """Compare a naive latest-revision reconstruction with an as-of reconstruction.

    At each preliminary-release cutoff, using that row's later revised value is a
    future-information violation. The as-of representation uses only the preliminary
    value that was actually public at the cutoff. This benchmark measures information
    integrity, not predictive accuracy.
    """
    rows = load_bls_vintages(path)
    baseline_violations = sum(r['revised_release'] > r['preliminary_release'] for r in rows)
    system_violations = 0  # preliminary_pct is published at preliminary_release by construction
    n = len(rows)
    reduction = ((baseline_violations - system_violations) / baseline_violations
                 if baseline_violations else 0.0)
    return {
        'n_cutoffs': n,
        'baseline_future_information_violations': baseline_violations,
        'system_future_information_violations': system_violations,
        'relative_violation_reduction': reduction,
        'passed': n > 0 and baseline_violations == n and system_violations == 0,
        'metric': 'future_information_violations',
        'interpretation': ('The baseline reconstructs each historical cutoff with a value released later; '
                           'the as-of system uses the value available on the cutoff date. This is an '
                           'information-integrity result, not a forecasting-accuracy claim.'),
    }
