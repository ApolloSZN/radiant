import json, pytest
from radiant.ci_attest import build_attestation, write

ENV={"GITHUB_ACTIONS":"true","GITHUB_SHA":"a"*40,"GITHUB_RUN_ID":"12345","GITHUB_REPOSITORY":"owner/radiant","GITHUB_SERVER_URL":"https://github.com","GITHUB_WORKFLOW_REF":"owner/radiant/.github/workflows/ci.yml@refs/heads/main"}

def test_attestation_rejects_local_environment():
    with pytest.raises(RuntimeError): build_attestation({})

def test_attestation_is_commit_bound(tmp_path):
    d=build_attestation(ENV)
    assert d["commit_sha"]=="a"*40
    assert d["run_url"]=="https://github.com/owner/radiant/actions/runs/12345"
    p=tmp_path/'att.json'; write(p,ENV)
    assert json.loads(p.read_text())["schema"]=="radiant.hosted_ci.v1"
