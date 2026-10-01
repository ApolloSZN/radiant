from radiant.data.robustness import paired_improvement_diagnostics

def test_paired_diagnostics_are_deterministic_and_detect_clear_gain():
    r1=paired_improvement_diagnostics([2,2,2,2],[1,1,1,1],draws=500,seed=7)
    r2=paired_improvement_diagnostics([2,2,2,2],[1,1,1,1],draws=500,seed=7)
    assert r1==r2
    assert r1['bootstrap_ci95']==[0.5,0.5]
    assert r1['leave_one_out_min_improvement']==0.5

def test_diagnostics_reject_unpaired_inputs():
    try:
        paired_improvement_diagnostics([1,2,3],[1,2])
    except ValueError:
        pass
    else:
        raise AssertionError('expected ValueError')
