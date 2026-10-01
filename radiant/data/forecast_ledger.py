from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
import hashlib, json, math

@dataclass(frozen=True)
class RegisteredForecast:
    forecast_id: str
    registered_at: str
    cutoff: date
    target_date: date
    target: str
    kind: str
    prediction: float
    model_spec: dict
    evidence_ids: tuple[str,...]
    artifact_hash: str

@dataclass(frozen=True)
class Resolution:
    forecast_id: str
    resolved_at: str
    actual: float
    score: dict

def _canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),default=str)

def register(cutoff:date,target_date:date,target:str,kind:str,prediction:float,model_spec:dict,evidence_ids:list[str],registered_at:str|None=None):
    if target_date <= cutoff: raise ValueError('target must be after cutoff')
    if kind not in {'binary','positive_continuous'}: raise ValueError('unsupported kind')
    if kind=='binary' and not 0 <= prediction <= 1: raise ValueError('probability outside [0,1]')
    if kind=='positive_continuous' and prediction <= 0: raise ValueError('prediction must be positive')
    reg=registered_at or datetime.now(timezone.utc).isoformat()
    payload={'registered_at':reg,'cutoff':cutoff,'target_date':target_date,'target':target,'kind':kind,
             'prediction':prediction,'model_spec':model_spec,'evidence_ids':sorted(evidence_ids)}
    h=hashlib.sha256(_canonical(payload).encode()).hexdigest()
    return RegisteredForecast(h[:24],reg,cutoff,target_date,target,kind,prediction,model_spec,tuple(sorted(evidence_ids)),h)

def resolve(f:RegisteredForecast,actual:float,resolved_at:str|None=None):
    if f.kind=='binary':
        if actual not in (0,1): raise ValueError('binary actual must be 0/1')
        p=min(max(f.prediction,1e-12),1-1e-12)
        score={'brier':(p-actual)**2,'log_score':-(actual*math.log(p)+(1-actual)*math.log(1-p))}
    else:
        if actual <= 0: raise ValueError('actual must be positive')
        e=math.log(f.prediction/actual)
        score={'log_error':e,'abs_log_error':abs(e),'factor_error':math.exp(abs(e))}
    return Resolution(f.forecast_id,resolved_at or datetime.now(timezone.utc).isoformat(),actual,score)
