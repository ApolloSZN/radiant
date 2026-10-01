from radiant.hosted_release import validate_completed_run

BASE={"schema":"radiant.completed_ci.v1","provider":"github_actions","repository":"owner/radiant",
      "commit_sha":"a"*40,"run_id":"123","run_url":"https://github.com/owner/radiant/actions/runs/123",
      "status":"completed","conclusion":"success"}

def test_completed_success_is_required():
    ok,_=validate_completed_run(BASE, 'a'*40)
    assert ok
    for field,value in [('status','in_progress'),('conclusion','failure')]:
        d={**BASE,field:value}
        assert not validate_completed_run(d,'a'*40)[0]

def test_commit_binding():
    assert not validate_completed_run(BASE,'b'*40)[0]
