from radiant.data.goes_import_floor import (
    all_forms_view, goes_import_floor_result,
    CLIFFS_2025_LAMINATION_IMPORT_UNITS_2024,
    CLIFFS_2025_LAMINATION_IMPORT_UNITS_2025_YTD,
)


def test_all_forms_view_matches_like_for_like_accounting():
    v = all_forms_view()
    assert v['us_goes_use_2019_all_forms_kt'] == 288.0 and v['foreign_goes_2019_all_forms_kt'] == 95.0
    lo, hi = v['foreign_goes_floor_all_forms_kt']
    assert 155 < lo < 156 and 175 < hi < 176
    m_lo, m_hi = v['floor_multiple_of_2019_foreign_all_forms']
    assert 1.6 < m_lo < 1.7 and 1.8 < m_hi < 1.9
    s_lo, s_hi = v['foreign_share_floor']
    assert 0.32 < v['foreign_share_2019'] < 0.34 and 0.40 < s_lo < 0.41 and 0.43 < s_hi < 0.44


def test_sheet_floor_plus_core_imports_equals_all_forms_floor():
    # Same physics, two framings: sheet-channel floor + flat embodied cores = all-forms floor.
    sheet = goes_import_floor_result()['import_floor_kt']
    allf = all_forms_view()['foreign_goes_floor_all_forms_kt']
    assert abs(sheet[0] + 68.0 - allf[0]) < 1e-9 and abs(sheet[1] + 68.0 - allf[1]) < 1e-9


def test_sheet_only_multiple_is_not_the_headline():
    assert all_forms_view()['sheet_only_multiple_withdrawn_as_headline'] is True


def test_2024_2025_lamination_trade_counts_are_context_not_tonnage():
    y2024 = CLIFFS_2025_LAMINATION_IMPORT_UNITS_2024
    y2025 = CLIFFS_2025_LAMINATION_IMPORT_UNITS_2025_YTD
    assert y2024.value == 147_652_598.0 and y2024.unit == 'units'
    assert y2025.value == 25_059_726.0 and y2025.unit == 'units'
    assert '8504.90.9534' in y2024.scope_note and '8504.90.9634' in y2024.scope_note
    # New unit-count evidence must not silently change the mass-based headline.
    assert all_forms_view()['foreign_goes_2019_all_forms_kt'] == 95.0
    sheet = goes_import_floor_result()['import_floor_kt']
    assert all_forms_view()['foreign_goes_floor_all_forms_kt'] == (sheet[0] + 68.0, sheet[1] + 68.0)


def test_run053_all_forms_headline_is_withdrawn_and_superseded():
    v = all_forms_view()
    assert v['status'] == 'withdrawn_run_061' and v['evidence_class'] == 'withdrawn_negative_result'
    assert 'double counts' in v['withdrawal_reason'] and v['superseded_by'] == 'radiant.data.goes_balance.headline'
    assert goes_import_floor_result()['status'] == 'withdrawn_run_061'
