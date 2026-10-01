from pathlib import Path
import json
from radiant.release import verify
from radiant.source_fingerprint import fingerprint

def test_release_fails_closed_without_strict_vintage(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'retrospective_real_data'}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','README.md','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(('word '*600) if p=='README.md' else 'x')
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    r=verify(tmp_path)
    assert not r['passed']
    assert not next(g for g in r['gates'] if g['name']=='strict_no_leak_headline_evidence')['passed']

def test_release_accepts_strict_vintage_when_other_gates_present(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/hosted_ci_attestation.json').write_text(json.dumps({'schema':'radiant.hosted_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':'a'*40,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123'}))
    (tmp_path/'artifacts/completed_ci_run.json').write_text(json.dumps({'schema':'radiant.completed_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':'a'*40,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123','status':'completed','conclusion':'success'}))
    assert verify(tmp_path, candidate_sha='a'*40)['passed']

def test_ci_mode_does_not_claim_final_completion(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/hosted_ci_attestation.json').write_text(json.dumps({'schema':'radiant.hosted_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':'a'*40,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123'}))
    r=verify(tmp_path, ci_mode=True, candidate_sha='a'*40)
    assert r['passed'] and r['mode']=='ci'
    assert not next(g for g in r['gates'] if g['name']=='hosted_ci_completed_green')['passed']
    assert not verify(tmp_path, candidate_sha='a'*40)['passed']


def test_release_rejects_hosted_evidence_from_different_candidate(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    old='a'*40; current='b'*40
    (tmp_path/'artifacts/hosted_ci_attestation.json').write_text(json.dumps({'schema':'radiant.hosted_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':old,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123'}))
    (tmp_path/'artifacts/completed_ci_run.json').write_text(json.dumps({'schema':'radiant.completed_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':old,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123','status':'completed','conclusion':'success'}))
    r=verify(tmp_path, candidate_sha=current)
    assert not r['passed']
    assert not next(g for g in r['gates'] if g['name']=='hosted_ci_execution')['passed']
    assert not next(g for g in r['gates'] if g['name']=='hosted_ci_completed_green')['passed']

def test_release_rejects_mixed_hosted_runs(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fingerprint(tmp_path)}))
    sha='a'*40
    (tmp_path/'artifacts/hosted_ci_attestation.json').write_text(json.dumps({'schema':'radiant.hosted_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':sha,'run_id':'123','run_url':'https://github.com/owner/radiant/actions/runs/123'}))
    (tmp_path/'artifacts/completed_ci_run.json').write_text(json.dumps({'schema':'radiant.completed_ci.v1','provider':'github_actions','repository':'owner/radiant','commit_sha':sha,'run_id':'999','run_url':'https://github.com/owner/radiant/actions/runs/999','status':'completed','conclusion':'success'}))
    r=verify(tmp_path, candidate_sha=sha)
    assert not r['passed']
    assert not next(g for g in r['gates'] if g['name']=='hosted_ci_completed_green')['passed']


def test_release_rejects_stale_or_failed_execution_artifacts(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':1,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':False,'source_fingerprint':fingerprint(tmp_path)}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':False,'source_fingerprint':fingerprint(tmp_path)}))
    r=verify(tmp_path, candidate_sha='a'*40)
    assert not next(g for g in r['gates'] if g['name']=='tests_ci_green')['passed']
    assert not next(g for g in r['gates'] if g['name']=='one_command_reproduction')['passed']
    assert not next(g for g in r['gates'] if g['name']=='working_demo')['passed']

def test_release_rejects_receipts_after_executable_source_changes(tmp_path):
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir(); (tmp_path/'radiant').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'release':{'release_ok':True},'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for p in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py','radiant/model.py']:
        q=tmp_path/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('original')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    fp=fingerprint(tmp_path)
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fp}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fp}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fp}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fp}))
    (tmp_path/'radiant/model.py').write_text('changed after receipts')
    r=verify(tmp_path, candidate_sha='a'*40)
    assert not next(g for g in r['gates'] if g['name']=='tests_ci_green')['passed']
    assert not next(g for g in r['gates'] if g['name']=='one_command_reproduction')['passed']
    assert not next(g for g in r['gates'] if g['name']=='working_demo')['passed']


def test_release_run_preserves_source_bound_test_receipt(tmp_path, monkeypatch):
    """--run must not destroy the v2 receipt needed by final hosted verification."""
    (tmp_path/'artifacts').mkdir(); (tmp_path/'.github/workflows').mkdir(parents=True); (tmp_path/'scripts').mkdir(); (tmp_path/'docs/adr').mkdir(parents=True); (tmp_path/'examples').mkdir(); (tmp_path/'radiant').mkdir()
    (tmp_path/'artifacts/eval_report.json').write_text(json.dumps({'all_passed':True,'release':{'release_ok':True},'results':[{'passed':True,'evidence_class':'strict_historical_vintage','claim_status':'claimed','relative_improvement':1.0}]}))
    for qname in ['.github/workflows/ci.yml','scripts/reproduce.sh','scripts/reproduce_container.sh','Dockerfile','docs/limitations.md','examples/demo.py','radiant/model.py']:
        q=tmp_path/qname; q.parent.mkdir(parents=True,exist_ok=True); q.write_text('x')
    (tmp_path/'README.md').write_text('word '*600); (tmp_path/'docs/technical_writeup.md').write_text('word '*1600)
    for i in range(3): (tmp_path/f'docs/adr/{i}.md').write_text('x')
    fp=fingerprint(tmp_path)
    (tmp_path/'artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':fp}))
    (tmp_path/'artifacts/reproduction_report.json').write_text(json.dumps({'schema':'radiant.reproduction.v2','passed':True,'source_fingerprint':fp}))
    (tmp_path/'artifacts/container_reproduction_report.json').write_text(json.dumps({'schema':'radiant.container_reproduction.v1','passed':True,'source_fingerprint':fp}))
    (tmp_path/'artifacts/demo_report.json').write_text(json.dumps({'schema':'radiant.demo.v2','passed':True,'source_fingerprint':fp}))
    # Stub only the pytest subprocess: this test is about the persisted receipt contract,
    # not recursively running pytest from inside pytest.
    class CP:
        returncode=0; stdout='1 passed'; stderr=''
    monkeypatch.setattr('radiant.release.subprocess.run', lambda *a, **k: CP())
    verify(tmp_path, run_commands=True, candidate_sha='a'*40)
    receipt=json.loads((tmp_path/'artifacts/test_report.json').read_text())
    assert receipt['schema']=='radiant.tests.v2'
    assert receipt['returncode']==0
    assert receipt['source_fingerprint']==fingerprint(tmp_path)
