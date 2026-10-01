#!/usr/bin/env python3
"""After the GitHub `ci` run finishes green, record it and verify the release.

    python scripts/record_completed_ci.py            # latest `ci` run
    python scripts/record_completed_ci.py 1234567890 # a specific run id

Requires the GitHub CLI (`gh`) logged in. Downloads the run's evidence artifact
(hosted attestation), writes artifacts/completed_ci_run.json, then runs the final
release verifier. Refuses to write anything for a run that is not completed+success.
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path


def build_record(run: dict, repository: str) -> dict:
    return {'schema': 'radiant.completed_ci.v1', 'provider': 'github_actions', 'repository': repository,
            'commit_sha': str(run['headSha']).lower(), 'run_id': str(run['databaseId']), 'run_url': run['url'],
            'status': run['status'], 'conclusion': run['conclusion']}


def _gh(*args: str) -> str:
    return subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        run_id = argv[1]
    else:
        runs = json.loads(_gh('run', 'list', '--workflow', 'ci', '--limit', '1', '--json', 'databaseId'))
        if not runs:
            print('no ci runs found'); return 1
        run_id = str(runs[0]['databaseId'])
    run = json.loads(_gh('run', 'view', run_id, '--json', 'databaseId,headSha,status,conclusion,url'))
    if not (run['status'] == 'completed' and run['conclusion'] == 'success'):
        print(f"run {run_id} is {run['status']}/{run['conclusion']} - nothing recorded. Fix CI first."); return 1
    repo = json.loads(_gh('repo', 'view', '--json', 'nameWithOwner'))['nameWithOwner']
    dl = Path('artifacts/ci_download')
    shutil.rmtree(dl, ignore_errors=True)
    _gh('run', 'download', run_id, '-n', 'radiant-release-evidence', '-D', str(dl))
    att = next(dl.rglob('hosted_ci_attestation.json'))
    shutil.copy(att, 'artifacts/hosted_ci_attestation.json')
    Path('artifacts/completed_ci_run.json').write_text(json.dumps(build_record(run, repo), indent=2) + '\n')
    shutil.rmtree(dl, ignore_errors=True)
    print('recorded', run['url'])
    return subprocess.call([sys.executable, '-m', 'radiant.release'])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
