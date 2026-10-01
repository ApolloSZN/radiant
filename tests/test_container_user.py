from pathlib import Path


def test_container_runs_as_host_user_so_ci_can_overwrite_receipts():
    s = Path('scripts/reproduce_container.sh').read_text()
    assert '--user "$(id -u):$(id -g)"' in s
    assert 'PYTEST_ADDOPTS="-p no:cacheprovider"' in s  # /app is read-only for a non-root user
