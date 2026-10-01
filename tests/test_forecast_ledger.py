from datetime import date
from radiant.data.forecast_ledger import register,resolve

def test_registration_is_reproducible_and_evidence_order_invariant():
    kw=dict(cutoff=date(2025,1,1),target_date=date(2026,1,1),target='x',kind='binary',prediction=.7,
            model_spec={'m':'v1'},registered_at='2025-01-01T00:00:00+00:00')
    a=register(**kw,evidence_ids=['b','a']); b=register(**kw,evidence_ids=['a','b'])
    assert a.artifact_hash==b.artifact_hash and a.forecast_id==b.forecast_id

def test_binary_and_continuous_resolution_scores():
    b=register(date(2025,1,1),date(2026,1,1),'event','binary',.8,{},[],registered_at='2025-01-01T00:00:00+00:00')
    rb=resolve(b,1,resolved_at='2026-01-02T00:00:00+00:00'); assert abs(rb.score['brier']-.04)<1e-12
    c=register(date(2025,1,1),date(2026,1,1),'cost','positive_continuous',100,{},[],registered_at='2025-01-01T00:00:00+00:00')
    rc=resolve(c,50,resolved_at='2026-01-02T00:00:00+00:00'); assert abs(rc.score['factor_error']-2)<1e-12

def test_invalid_forecasts_rejected():
    import pytest
    with pytest.raises(ValueError): register(date(2025,1,1),date(2024,1,1),'x','binary',.5,{},[])
    with pytest.raises(ValueError): register(date(2025,1,1),date(2026,1,1),'x','binary',1.2,{},[])
