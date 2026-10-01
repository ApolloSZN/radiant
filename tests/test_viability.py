from radiant.engines.raf import Process
from radiant.engines.viability import FlowProcess, material_viability, quantitative_closure


def cycle_raf():
    return [
      Process.of('make_tool',['ore'],['tool'],['tool']),
      Process.of('make_part',['ore'],['part'],['tool']),
    ]


def test_raf_can_exist_while_materially_nonviable():
    # Topology closes, but tool production capacity cannot cover tool depreciation.
    fp=[FlowProcess('make_tool',{'ore':1},{'tool':1},capacity=.4),
        FlowProcess('make_part',{'ore':1},{'part':1},capacity=10)]
    q=quantitative_closure({'ore'}, cycle_raf(), fp, {'tool':1}, {'ore':100})
    assert q['topological_closure'] is True
    assert q['material_viability'] is False
    assert q['self_maintaining'] is False


def test_quantitative_closure_passes_when_replacement_rate_is_sufficient():
    fp=[FlowProcess('make_tool',{'ore':1},{'tool':1},capacity=2,energy_per_flux=2),
        FlowProcess('make_part',{'ore':1},{'part':1},capacity=10)]
    q=quantitative_closure({'ore'}, cycle_raf(), fp, {'tool':1}, {'ore':100}, energy_budget=3)
    assert q['self_maintaining'] is True
    assert abs(q['viability'].fluxes['make_tool']-1) < 1e-7
    assert q['viability'].energy_used <= 3


def test_energy_budget_can_break_otherwise_viable_network():
    fp=[FlowProcess('make_tool',{'ore':1},{'tool':1},capacity=2,energy_per_flux=2)]
    r=material_viability(fp, {'tool':1}, {'ore':100}, energy_budget=1.9)
    assert r.feasible is False


def test_external_import_can_cover_maintenance_but_is_visible():
    r=material_viability([], {'tool':1}, {'tool':1})
    assert r.feasible
    assert r.imports['tool'] == 1


def test_unproduced_raw_input_is_not_free():
    # Regression: before rc6, balance constraints were emitted only for maintained
    # items, so this process could consume ore even with no ore supply.
    fp=[FlowProcess('make_tool',{'ore':1},{'tool':1},capacity=2)]
    r=material_viability(fp, {'tool':1}, {})
    assert r.feasible is False


def test_raw_input_limit_is_physically_binding():
    fp=[FlowProcess('make_tool',{'ore':2},{'tool':1},capacity=2)]
    assert material_viability(fp, {'tool':1}, {'ore':1.9}).feasible is False
    r=material_viability(fp, {'tool':1}, {'ore':2.0})
    assert r.feasible is True
    assert abs(r.imports['ore']-2.0) < 1e-7


def test_inherited_stock_can_enable_survival_but_not_self_maintenance():
    from radiant.engines.viability import finite_horizon_viability
    # No process replaces tool depreciation. A stock of 10 survives 5 time units
    # at decay 1/time, but terminal stock is depleted and hence not self-maintaining.
    survival=finite_horizon_viability([], {'tool':10}, {'tool':1}, 5,
                                     require_non_depletion=False)
    closure=finite_horizon_viability([], {'tool':10}, {'tool':1}, 5,
                                    require_non_depletion=True)
    assert survival.feasible is True
    assert closure.feasible is False


def test_finite_horizon_replacement_preserves_enabling_stock():
    from radiant.engines.viability import finite_horizon_viability
    fp=[FlowProcess('replace_tool',{'ore':1},{'tool':1},capacity=2,energy_per_flux=1)]
    r=finite_horizon_viability(fp, {'tool':10}, {'tool':1}, 5,
                               {'ore':2}, energy_budget=5,
                               require_non_depletion=True)
    assert r.feasible is True
    assert abs(r.fluxes['replace_tool']-1.0) < 1e-7
    assert r.balance_slack['tool'] >= -1e-8


def test_path_viability_cannot_borrow_raw_material_from_future():
    from radiant.engines.viability import path_viability
    # Tool maintenance is due every period. Ore arrives only in period 2. An
    # aggregate horizon balance would say 2 ore is enough, but period 1 stock hits
    # zero before the future ore exists, so path feasibility must fail.
    fp=[FlowProcess('replace_tool',{'ore':1},{'tool':1},capacity=1)]
    r=path_viability(fp, {'tool':0,'ore':0}, {'tool':1}, periods=2,
                     import_schedule={'ore':[0,2]}, require_non_depletion=False)
    assert r.feasible is False


def test_path_viability_tracks_time_varying_capacity_and_stocks():
    from radiant.engines.viability import path_viability
    fp=[FlowProcess('replace_tool',{'ore':1},{'tool':1},capacity=2)]
    r=path_viability(fp, {'tool':2,'ore':0}, {'tool':1}, periods=3,
                     import_schedule={'ore':[1,1,1]},
                     capacity_schedule={'replace_tool':[0,2,2]},
                     require_non_depletion=False)
    assert r.feasible
    assert len(r.stock_trajectory)==4
    assert r.stock_trajectory[1]['tool'] >= -1e-9
    assert r.flux_trajectory[0].get('replace_tool',0)==0


def test_path_non_depletion_requires_terminal_replacement():
    from radiant.engines.viability import path_viability
    fp=[FlowProcess('replace_tool',{'ore':1},{'tool':1},capacity=1)]
    survival=path_viability(fp, {'tool':3}, {'tool':1}, periods=2,
                            require_non_depletion=False)
    closure=path_viability(fp, {'tool':3}, {'tool':1}, periods=2,
                           require_non_depletion=True)
    assert survival.feasible
    assert closure.feasible is False  # no explicit ore supply
