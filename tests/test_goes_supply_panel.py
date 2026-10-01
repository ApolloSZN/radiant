import pytest

from radiant.data.goes_supply_panel import (
    CURRENT_EXPORT_SCHEDULE_B,
    CURRENT_IMPORT_HTS,
    validate_trade_code_coverage,
    aggregate_trade_quantity,
    historical_import_share_2019,
    adequacy_identification_status,
    COMMERCE_2019,
)


def test_goes_trade_requires_both_hs6_width_headings():
    partial = validate_trade_code_coverage(['7225.11'])
    assert partial.complete_for_goes_flat_products is False
    assert partial.missing_codes == ('7226.11',)
    full = validate_trade_code_coverage(['7225.11', '7226.11'])
    assert full.complete_for_goes_flat_products is True
    assert full.missing_codes == ()


def test_current_import_extraction_requires_all_four_10_digit_hts_codes():
    partial = validate_trade_code_coverage(['7225110000', '7226111000'], code_set=CURRENT_IMPORT_HTS)
    assert partial.complete_for_goes_flat_products is False
    assert set(partial.missing_codes) == {'7226119030', '7226119060'}
    full = validate_trade_code_coverage(CURRENT_IMPORT_HTS.codes, code_set=CURRENT_IMPORT_HTS)
    assert full.complete_for_goes_flat_products is True
    assert full.classification == 'HTSUSA-10'
    assert full.direction == 'import'


def test_current_export_concordance_is_direction_specific_and_coarser():
    full = validate_trade_code_coverage(['7225110000', '7226110000'], code_set=CURRENT_EXPORT_SCHEDULE_B)
    assert full.complete_for_goes_flat_products
    assert CURRENT_EXPORT_SCHEDULE_B.codes != CURRENT_IMPORT_HTS.codes


def test_aggregate_trade_quantity_fails_closed_on_missing_code_not_silent_zero():
    rows = [
        {'code': '7225110000', 'quantity_kg': 10},
        {'code': '7226111000', 'quantity_kg': 5},
        {'code': '7226119030', 'quantity_kg': 2},
    ]
    with pytest.raises(ValueError, match='incomplete import GOES code coverage'):
        aggregate_trade_quantity(rows, code_set=CURRENT_IMPORT_HTS)
    rows.append({'code': '7226119060', 'quantity_kg': 3})
    assert aggregate_trade_quantity(rows, code_set=CURRENT_IMPORT_HTS) == 20


def test_historical_import_share_is_descriptive_not_future_capacity():
    assert abs(historical_import_share_2019() - 27_000 / 220_000) < 1e-12
    s = adequacy_identification_status()
    assert s['adequacy_identified'] is False
    assert 'domestic_production_or_capacity' in s['missing_supply_response_metrics']
    assert 'competing_consumption' in s['missing_supply_response_metrics']


def test_vintage_metadata_is_explicit():
    assert all(o.period == '2019' and o.published_year == 2021 for o in COMMERCE_2019)
