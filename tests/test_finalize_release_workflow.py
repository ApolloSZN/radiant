import importlib.util
from pathlib import Path
import pytest


def _module():
    spec=importlib.util.spec_from_file_location('w',Path('scripts/write_completed_ci_from_env.py'))
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def good():
    return {'RADIANT_REPOSITORY':'owner/radiant','RADIANT_COMMIT_SHA':'a'*40,'RADIANT_RUN_ID':'123',
            'RADIANT_RUN_URL':'https://github.com/owner/radiant/actions/runs/123',
            'RADIANT_RUN_STATUS':'completed','RADIANT_RUN_CONCLUSION':'success'}


def test_completed_receipt_from_workflow_run_is_fail_closed():
    m=_module(); d=m.build_record(good())
    assert d['schema']=='radiant.completed_ci.v1' and d['conclusion']=='success'
    for key,value in [('RADIANT_RUN_CONCLUSION','failure'),('RADIANT_RUN_STATUS','in_progress'),
                      ('RADIANT_RUN_URL','https://github.com/owner/radiant/actions/runs/999'),
                      ('RADIANT_COMMIT_SHA','bad')]:
        e=good(); e[key]=value
        with pytest.raises(RuntimeError): m.build_record(e)


def test_finalize_workflow_binds_and_verifies_exact_upstream_run():
    t=Path('.github/workflows/finalize-release.yml').read_text()
    assert 'workflow_run:' in t and 'workflows: ["ci"]' in t
    assert "conclusion == 'success'" in t
    assert 'github.event.workflow_run.head_sha' in t
    assert 'run-id: ${{ github.event.workflow_run.id }}' in t
    assert 'python scripts/write_completed_ci_from_env.py' in t
    assert 'python -m radiant.release' in t
