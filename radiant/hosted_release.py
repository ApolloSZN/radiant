"""Verify *completed* hosted CI evidence for the final v1.0 ship decision.

A workflow cannot truthfully attest its own successful completion while it is still
running.  `radiant.ci_attest` therefore proves only that the release verifier ran
inside GitHub Actions.  Final shipment requires a separate completed-run record
captured after GitHub reports conclusion=success.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json, re
from pathlib import Path

@dataclass(frozen=True)
class HostedRun:
    repository: str
    commit_sha: str
    run_id: str
    run_url: str
    status: str
    conclusion: str


def validate_completed_run(data: dict, expected_sha: str | None = None) -> tuple[bool, str]:
    sha=str(data.get('commit_sha','')).lower()
    ok=(data.get('schema')=='radiant.completed_ci.v1'
        and data.get('provider')=='github_actions'
        and bool(data.get('repository'))
        and bool(re.fullmatch(r'[0-9a-f]{40}',sha))
        and str(data.get('run_id','')).isdigit()
        and str(data.get('run_url','')).startswith('https://github.com/')
        and data.get('status')=='completed'
        and data.get('conclusion')=='success')
    if expected_sha is not None:
        ok = ok and sha == expected_sha.lower()
    return ok, (data.get('run_url','invalid completed-run evidence') if ok else 'invalid or non-successful completed hosted run')


def load(path: str|Path='artifacts/completed_ci_run.json', expected_sha: str|None=None):
    p=Path(path)
    if not p.exists(): return False, f'missing {p}'
    try: data=json.loads(p.read_text())
    except Exception as exc: return False, f'invalid completed CI record: {exc}'
    return validate_completed_run(data, expected_sha)
