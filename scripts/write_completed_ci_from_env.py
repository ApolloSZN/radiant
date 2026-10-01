#!/usr/bin/env python3
"""Write a completed GitHub Actions CI receipt from a workflow_run environment.

This deliberately fails closed unless the upstream run is completed+success and
all identity fields are well formed. The final release verifier independently
cross-checks this receipt against the attestation produced inside the upstream
CI run and the checked-out commit SHA.
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path


def build_record(env=None):
    e=dict(os.environ if env is None else env)
    required=['RADIANT_REPOSITORY','RADIANT_COMMIT_SHA','RADIANT_RUN_ID','RADIANT_RUN_URL','RADIANT_RUN_STATUS','RADIANT_RUN_CONCLUSION']
    missing=[k for k in required if not e.get(k)]
    if missing: raise RuntimeError('missing workflow_run environment: '+', '.join(missing))
    sha=e['RADIANT_COMMIT_SHA'].lower(); run_id=str(e['RADIANT_RUN_ID'])
    repo=e['RADIANT_REPOSITORY']; url=e['RADIANT_RUN_URL']
    if not re.fullmatch(r'[0-9a-f]{40}',sha): raise RuntimeError('commit SHA must be 40 hex')
    if not run_id.isdigit(): raise RuntimeError('run id must be numeric')
    if not re.fullmatch(r'[^/\s]+/[^/\s]+',repo): raise RuntimeError('repository must be owner/name')
    expected=f'https://github.com/{repo}/actions/runs/{run_id}'
    if url != expected: raise RuntimeError('run URL does not match repository/run id')
    if e['RADIANT_RUN_STATUS']!='completed' or e['RADIANT_RUN_CONCLUSION']!='success':
        raise RuntimeError('upstream CI is not completed+success')
    return {'schema':'radiant.completed_ci.v1','provider':'github_actions','repository':repo,
            'commit_sha':sha,'run_id':run_id,'run_url':url,'status':'completed','conclusion':'success'}


def main():
    try: d=build_record()
    except Exception as exc:
        print(str(exc),file=sys.stderr); return 2
    p=Path('artifacts/completed_ci_run.json'); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,indent=2)+'\n'); print(json.dumps(d,indent=2)); return 0

if __name__=='__main__': raise SystemExit(main())
