import importlib.util
from pathlib import Path
from radiant.hosted_release import validate_completed_run


def _mod():
    spec = importlib.util.spec_from_file_location('rc', Path('scripts/record_completed_ci.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def test_record_built_from_gh_json_passes_release_validator():
    run = {'databaseId': 987654321, 'headSha': 'ABCDEF0123456789abcdef0123456789abcdef01',
           'status': 'completed', 'conclusion': 'success', 'url': 'https://github.com/logan/radiant/actions/runs/987654321'}
    ok, _ = validate_completed_run(_mod().build_record(run, 'logan/radiant'))
    assert ok


def test_failed_run_record_would_not_validate():
    run = {'databaseId': 1, 'headSha': 'a' * 40, 'status': 'completed', 'conclusion': 'failure',
           'url': 'https://github.com/x/y/actions/runs/1'}
    ok, _ = validate_completed_run(_mod().build_record(run, 'x/y'))
    assert not ok
