import pytest
from radiant.data import goes_research as g


def test_every_fact_is_typed_and_sourced():
    for f in g.PHASE0_FACTS:
        assert f.evidence_type in g.EVIDENCE_TYPES, f.fact_id
        assert f.source.startswith('http') and f.note, f.fact_id


def test_core_coalition_figures_are_flagged_as_interested_secondhand():
    for f in (g.COMMERCE_2019_CONSUMPTION_CORE_COALITION, g.COMMERCE_2019_EMBODIED_CORES, g.COMMERCE_2020_EMBODIED_CORES):
        assert f.evidence_type == 'secondhand' and 'Core Coalition' in f.interested_party


def test_comtrade_matches_census_panel_2019_2024():
    # Two independent pulls of the same U.S. series must agree (Census API vs UN Comtrade).
    census_imports = {2019: 26.8, 2020: 26.2, 2021: 41.8, 2022: 20.0, 2023: 31.4, 2024: 35.2}
    census_exports = {2019: 45.7, 2020: 30.6, 2021: 47.7, 2022: 71.9, 2023: 45.8, 2024: 37.5}
    for y in census_imports:
        assert g.comtrade_world_kt(y, 'M') == pytest.approx(census_imports[y], rel=0.05)  # general vs consumption
        assert g.comtrade_world_kt(y, 'X') == pytest.approx(census_exports[y], rel=0.01)
        assert g.comtrade_world_kt(y, 'DX') + g.comtrade_world_kt(y, 'RX') == pytest.approx(g.comtrade_world_kt(y, 'X'), rel=0.01)


def test_phase0_220kt_is_all_forms_and_288kt_double_counts_cores():
    r = g.phase0_reconciliation()
    lo, hi = r['sheet_consumption_2019_kt']
    assert 145 < lo < hi <= 150
    assert r['core_coalition_220kt_matches_all_forms'] is True
    assert r['double_count_in_288kt_kt'] == pytest.approx(72.1, abs=0.5)


def test_phase0_implied_production_fits_under_capacity_and_matches_2017():
    r = g.phase0_reconciliation()
    plo, phi = r['implied_production_2019_kt']
    assert 160 < plo < phi < 170
    assert r['production_within_all_electrical_capacity'] is True
    assert phi < g.AK_2014_GOES_CAPACITY.value  # AK's stated 2014 GOES capacity is ~258 kt
    assert r['implied_production_2017_kt'] == pytest.approx(162, abs=3)  # independent year, same answer


def test_phase0_re_exports_are_a_minority_of_2019_exports():
    r = g.phase0_reconciliation()
    e = r['exports_2019_kt']
    assert e['re_exports'] / e['total'] == pytest.approx(0.24, abs=0.01)
    assert r['foreign_sheet_retained_2019_kt'] == pytest.approx(17.0, abs=0.2)
