from pathlib import Path


def test_ci_executes_clean_container_reproduction_and_uploads_receipt():
    t=Path('.github/workflows/ci.yml').read_text()
    assert 'bash scripts/reproduce_container.sh' in t
    assert 'artifacts/container_reproduction_report.json' in t


def test_container_wrapper_fails_closed_and_writes_receipt_after_docker_only():
    t=Path('scripts/reproduce_container.sh').read_text()
    assert 'set -euo pipefail' in t
    build=t.index('docker build')
    run=t.index('docker run')
    receipt=t.index('container_reproduction_report.json')
    assert build < run < receipt
    assert "'schema':'radiant.container_reproduction.v1'" in t


def test_docker_context_excludes_generated_and_git_state():
    ignored=set(Path('.dockerignore').read_text().splitlines())
    assert '.git' in ignored
    assert 'artifacts' in ignored
    assert '**/__pycache__' in ignored
