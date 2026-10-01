from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import csv, math
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class Observation:
    date: date
    value: float
    recorded_at: date
    source_tier: str
    source_url: str

@dataclass(frozen=True)
class Forecast:
    cutoff: date
    target_date: date
    predicted: float
    actual: float
    log_error: float
    train_n: int
    window: int | None


def load_series(path: str|Path, value_col='cost_per_genome_usd') -> list[Observation]:
    out=[]
    with open(path,newline='') as f:
        for r in csv.DictReader(f):
            out.append(Observation(date.fromisoformat(r['date']), float(r[value_col]),
                date.fromisoformat(r['recorded_at']), r['source_tier'], r['source_url']))
    return sorted(out,key=lambda x:x.date)

def visible_as_of(obs:list[Observation], cutoff:date)->list[Observation]:
    # Both clocks: world date and when the map learned it.
    return [o for o in obs if o.date <= cutoff and o.recorded_at <= cutoff]

def _year(d:date)->float:
    return d.year + (d.timetuple().tm_yday-1)/365.2425

def fit_log_linear(train:list[Observation], window:int|None=None):
    if window: train=train[-window:]
    if len(train)<3: raise ValueError('need >=3 observations')
    x=np.array([_year(o.date) for o in train]); y=np.log([o.value for o in train])
    x0=x.mean(); slope,intercept=np.polyfit(x-x0,y,1)
    residual=y-(intercept+slope*(x-x0)); sigma=float(np.sqrt(np.sum(residual**2)/max(1,len(y)-2)))
    return float(intercept),float(slope),float(x0),sigma,len(train)

def predict(model,target:date)->float:
    a,b,x0,_,_=model
    return float(math.exp(a+b*(_year(target)-x0)))

def rolling_one_step(obs:list[Observation], min_train=8, window:int|None=None, honest_recorded_at=False):
    out=[]
    for i in range(min_train,len(obs)):
        target=obs[i]
        cutoff=obs[i-1].date
        train=obs[:i]
        if honest_recorded_at:
            train=visible_as_of(train,cutoff)
        if len(train)<3: continue
        m=fit_log_linear(train,window)
        p=predict(m,target.date)
        out.append(Forecast(cutoff,target.date,p,target.value,math.log(p/target.value),m[-1],window))
    return out

def metrics(fs:list[Forecast]):
    e=np.array([f.log_error for f in fs])
    return {'n':len(fs),'MALE':float(np.mean(np.abs(e))), 'RMSE_log':float(np.sqrt(np.mean(e*e))),
            'median_factor_error':float(np.exp(np.median(np.abs(e))))}

def first_crossing(obs:list[Observation], threshold:float):
    return next((o.date for o in obs if o.value<=threshold),None)

def _norm_cdf(z:float)->float:
    return 0.5*(1.0+math.erf(z/math.sqrt(2.0)))

def crossing_forecasts(obs:list[Observation], threshold:float, min_train=8, window=8):
    rows=[]
    for i in range(min_train,len(obs)):
        train=obs[:i]; target=obs[i]; m=fit_log_linear(train,window)
        mu=math.log(predict(m,target.date)); sigma=max(m[3],1e-6)
        p=_norm_cdf((math.log(threshold)-mu)/sigma)
        outcome=1 if target.value<=threshold else 0
        p=min(max(p,1e-12),1-1e-12)
        rows.append({'cutoff':obs[i-1].date,'target':target.date,'p':p,'outcome':outcome,
                     'brier':(p-outcome)**2,'log_score':-(outcome*math.log(p)+(1-outcome)*math.log(1-p))})
    return rows

def score_binary(rows):
    return {'n':len(rows),'brier':float(np.mean([r['brier'] for r in rows])),
            'log_score':float(np.mean([r['log_score'] for r in rows]))}

@dataclass(frozen=True)
class VintageAnchor:
    source_available_at: date
    observation_date: date
    value: float
    relation: str
    source_tier: str
    source_url: str

def load_vintage_anchors(path: str|Path) -> list[VintageAnchor]:
    out=[]
    with open(path,newline='') as f:
        for r in csv.DictReader(f):
            out.append(VintageAnchor(date.fromisoformat(r['source_available_at']), date.fromisoformat(r['observation_date']),
                float(r['value_usd']),r['relation'],r['source_tier'],r['source_url']))
    return sorted(out,key=lambda x:x.source_available_at)

def historical_vintage_as_of(rows:list[VintageAnchor], cutoff:date)->list[VintageAnchor]:
    return [r for r in rows if r.source_available_at <= cutoff and r.observation_date <= cutoff]

def sequential_break_scores(obs:list[Observation], min_train=8, window=8, z_threshold=2.0):
    """No-lookahead innovation detector: score target only against model fit to earlier rows."""
    out=[]
    for i in range(min_train,len(obs)):
        train=obs[:i]
        m=fit_log_linear(train,window)
        pred=predict(m,obs[i].date)
        sigma=max(m[3],1e-6)
        innovation=math.log(obs[i].value/pred)
        z=innovation/sigma
        out.append({'cutoff':obs[i-1].date,'target':obs[i].date,'predicted':pred,'actual':obs[i].value,
                    'innovation_log':innovation,'z':z,'break':abs(z)>=z_threshold})
    return out

def adaptive_one_step(obs:list[Observation], min_train=8, base_window=8, z_threshold=2.0, post_break_window=4):
    """Causal adaptive forecaster: a detected surprise can change only future fits."""
    out=[]; active_window=base_window
    for i in range(min_train,len(obs)):
        train=obs[:i]; m=fit_log_linear(train,active_window); target=obs[i]
        p=predict(m,target.date); err=math.log(p/target.value)
        out.append(Forecast(obs[i-1].date,target.date,p,target.value,err,m[-1],active_window))
        sigma=max(m[3],1e-6)
        if abs(math.log(target.value/p)/sigma)>=z_threshold:
            active_window=post_break_window
        elif active_window==post_break_window and i >= min_train+post_break_window:
            active_window=base_window
    return out

def compare_forecasters(obs:list[Observation], min_train=5, rolling_window=5, z_threshold=2.0, post_break_window=3):
    """Cross-domain benchmark with identical causal forecasting contracts."""
    models={
        'all_history': rolling_one_step(obs,min_train,None),
        f'rolling_{rolling_window}': rolling_one_step(obs,min_train,rolling_window),
        'adaptive': adaptive_one_step(obs,min_train,rolling_window,z_threshold,post_break_window),
    }
    return {k:metrics(v) for k,v in models.items()}

def causal_model_selector(obs:list[Observation], min_train=8, windows=(None,8,4), warmup_predictions=2):
    """Prequential selector: choose next model only from each candidate's errors observed so far.
    No target outcome is used to choose the model that predicts that target.
    """
    history={w:[] for w in windows}; out=[]; choices=[]
    for i in range(min_train,len(obs)):
        target=obs[i]; train=obs[:i]
        eligible=[w for w in windows if w is None or len(train)>=w]
        scored=[]
        for w in eligible:
            prior=history[w]
            score=float(np.mean(np.abs(prior))) if len(prior)>=warmup_predictions else float('inf')
            scored.append((score, 10**9 if w is None else w, w))
        # Before enough evidence, default to all-history; afterwards minimize observed prequential MALE.
        finite=[s for s in scored if math.isfinite(s[0])]
        chosen=(min(finite)[2] if finite else None)
        m=fit_log_linear(train,chosen); p=predict(m,target.date); err=math.log(p/target.value)
        out.append(Forecast(obs[i-1].date,target.date,p,target.value,err,m[-1],chosen)); choices.append(chosen)
        # Outcome is now known; update every candidate for future choices only.
        for w in eligible:
            mm=fit_log_linear(train,w); pp=predict(mm,target.date); history[w].append(math.log(pp/target.value))
    return out,choices

def load_compute_series(path: str|Path) -> list[Observation]:
    out=[]
    with open(path,newline='') as f:
        for r in csv.DictReader(f):
            out.append(Observation(date.fromisoformat(r['date']),float(r['flops_per_2022_usd']),
                date.fromisoformat(r['recorded_at']),r['source_tier'],r['source_url']))
    return sorted(out,key=lambda x:x.date)
