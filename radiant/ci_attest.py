"""Generate a hosted-CI attestation from GitHub Actions environment variables.

This is deliberately unavailable in ordinary local runs. It is not a cryptographic
signature; the trustworthy copy is the artifact attached to the corresponding
GitHub Actions run. The release verifier validates its shape and commit binding.
"""
from __future__ import annotations
import json, os, re
from pathlib import Path

REQUIRED=("GITHUB_ACTIONS","GITHUB_SHA","GITHUB_RUN_ID","GITHUB_REPOSITORY","GITHUB_SERVER_URL")

def build_attestation(env=None):
    e=dict(os.environ if env is None else env)
    if e.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("hosted CI attestation may only be generated in GitHub Actions")
    missing=[k for k in REQUIRED if not e.get(k)]
    if missing: raise RuntimeError(f"missing GitHub Actions environment: {', '.join(missing)}")
    sha=e["GITHUB_SHA"]
    if not re.fullmatch(r"[0-9a-fA-F]{40}",sha): raise RuntimeError("GITHUB_SHA must be a 40-hex commit SHA")
    if not str(e["GITHUB_RUN_ID"]).isdigit(): raise RuntimeError("GITHUB_RUN_ID must be numeric")
    run_url=f'{e["GITHUB_SERVER_URL"].rstrip("/")}/{e["GITHUB_REPOSITORY"]}/actions/runs/{e["GITHUB_RUN_ID"]}'
    return {"schema":"radiant.hosted_ci.v1","provider":"github_actions","repository":e["GITHUB_REPOSITORY"],
            "commit_sha":sha.lower(),"run_id":str(e["GITHUB_RUN_ID"]),"run_url":run_url,
            "workflow_ref":e.get("GITHUB_WORKFLOW_REF","")}

def write(path="artifacts/hosted_ci_attestation.json", env=None):
    data=build_attestation(env)
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2)+"\n")
    return data

if __name__=="__main__": print(json.dumps(write(),indent=2))
