import pytest
from radiant.data.goes_import_floor import (goes_import_floor_result, import_floor,
    CLIFFS_ELECTRICAL_STEEL_CAPACITY, CLIFFS_HOT_MILL_EXPANSION_2026,
    COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS, COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS,
    DOE_2021_STACKED_CORE_IMPORT_UNITS, JFE_JSW_INDIA_GOES_JV_INVESTMENT, JFE_JSW_INDIA_GOES_CAPACITY_2030,
    THYSSENKRUPP_ISBERGUES_2026_CURTAILMENT, COMMERCE_2019_NA_TRANSFORMER_COMPONENT_US_DESTINATION,
    US_2026_GOES_SECTION232_TARIFF, USITC_2026_GOES_COLUMN1_RATE, DOE_2020_DIRECT_GOES_IMPORT_VALUE,
    EU_2026_TRANSFORMER_CORE_SAFEGUARD_DUTY, COMMERCE_2026_EU_GOES_SAFEGUARD_SCOPE, IEA_2023_GLOBAL_GOES_CAPACITY, JFE_2024_US_EATON_GOES_ORDER, DOE_2024_DISTRIBUTION_TRANSFORMER_CORE_STEEL_DEMAND, MTC_2024_DISTRIBUTION_TRANSFORMER_GOES_CONSUMPTION, COMMERCE_2014_US_GOES_HTS10_SCOPE)


def test_floor_is_positive_and_about_three_to_four_times_2019_imports():
    r = goes_import_floor_result()
    lo, hi = r['import_floor_kt']
    assert 87 < lo < 88 and 107 < hi < 108
    m_lo, m_hi = r['import_floor_multiple_of_2019_imports']
    assert 3.2 < m_lo < 3.3 and 3.9 < m_hi < 4.0
    assert r['identified'] and r['evidence_class'] == 'identified_conditional_bound'


def test_breakeven_requires_large_baseline_decline():
    r = goes_import_floor_result()
    d_hi_inc, d_lo_inc = r['baseline_decline_needed_for_zero_floor']
    assert d_lo_inc > 0.39 and d_hi_inc > 0.48


def test_capacity_is_an_upper_bound_so_more_capacity_never_raises_floor():
    assert import_floor(220, 94, 300) <= import_floor(220, 94, 226.8)
    assert import_floor(100, 94, 226.8) == 0.0
    with pytest.raises(ValueError):
        import_floor(-1, 94, 226.8)


def test_hot_mill_expansion_is_not_converted_into_goes_capacity():
    assert CLIFFS_HOT_MILL_EXPANSION_2026.evidence_class == 'qualitative_relative_statement_not_convertible'
    r = goes_import_floor_result()
    assert r['domestic_capacity_upper_bound_kt'] == CLIFFS_ELECTRICAL_STEEL_CAPACITY.value
    s = r['scenario_capacity_expansion']
    assert s['evidence_class'] == 'scenario_assumption'
    assert s['import_floor_kt'][0] > 0  # even the generous scenario leaves a positive floor


def test_no_shortage_claim():
    r = goes_import_floor_result()
    assert any('shortage' in x for x in r['not_claimed'])


def test_embodied_goes_import_evidence_is_typed_and_does_not_change_floor():
    r = goes_import_floor_result()
    context = r['context_evidence']

    assert COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.value == 68.0
    assert COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.unit == 'kt GOES-equivalent'
    assert COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.evidence_class == 'federal_report_estimate_from_industry_weight_estimate'
    assert COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS.value == 96.0
    assert COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS.evidence_class == 'industry_estimate_reported_by_federal_agency'
    assert context['embodied_core_to_direct_goes_import_ratio_2019'] == pytest.approx(68.0 / 27.0)

    # These describe already-imported derivative products; they are context, not a new term in the future import-floor equation.
    assert r['import_floor_kt'][0] == pytest.approx(220 + 94 - CLIFFS_ELECTRICAL_STEEL_CAPACITY.value)
    assert r['import_floor_kt'][1] == pytest.approx(220 + 114 - CLIFFS_ELECTRICAL_STEEL_CAPACITY.value)
    assert COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.evidence_id not in r['evidence_ids']
    assert COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS.evidence_id not in r['evidence_ids']


def test_stacked_core_unit_count_is_not_silently_converted_to_goes_mass():
    r = goes_import_floor_result()
    evidence = r['context_evidence']['stacked_core_import_units_2021_ytd_oct']
    assert DOE_2021_STACKED_CORE_IMPORT_UNITS.value == 842_929.0
    assert evidence['unit'] == 'units'
    assert '8504.90.9638' in evidence['scope_note']
    assert 'cannot be converted to GOES mass' in evidence['scope_note']
    assert DOE_2021_STACKED_CORE_IMPORT_UNITS.evidence_id not in r['evidence_ids']


def test_foreign_goes_supply_evidence_is_typed_but_not_inserted_into_us_floor():
    r = goes_import_floor_result()
    jfe = r['context_evidence']['foreign_goes_project_jfe_jsw_india']
    tkes = r['context_evidence']['foreign_goes_curtailment_thyssenkrupp_isbergues_2026']
    assert JFE_JSW_INDIA_GOES_JV_INVESTMENT.value == 670.0
    assert jfe['unit'] == 'USD million planned investment'
    assert 'No tonnage capacity is stated' in jfe['scope_note']
    assert THYSSENKRUPP_ISBERGUES_2026_CURTAILMENT.value == 0.50
    assert 'June-September 2026' in tkes['period']
    assert JFE_JSW_INDIA_GOES_JV_INVESTMENT.evidence_id not in r['evidence_ids']
    assert THYSSENKRUPP_ISBERGUES_2026_CURTAILMENT.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'][0] == pytest.approx(87.203815)


def test_jfe_jsw_announced_goes_capacity_is_quantified_but_not_us_available_supply():
    r = goes_import_floor_result()
    e = r['context_evidence']['foreign_goes_capacity_jfe_jsw_india_2030']
    assert JFE_JSW_INDIA_GOES_CAPACITY_2030.value == 350.0
    assert e['unit'] == 'kt GOES/year planned capacity'
    assert '100,000 tpy at Vijayanagar' in e['scope_note']
    assert '250,000 tpy at Nashik' in e['scope_note']
    assert 'current capacity is 50,000 tpy' in e['scope_note']
    assert JFE_JSW_INDIA_GOES_CAPACITY_2030.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_2026_goes_tariff_is_typed_policy_context_not_quantity_effect():
    r = goes_import_floor_result()
    sec232 = r['context_evidence']['us_goes_section232_tariff_2026']
    base = r['context_evidence']['us_goes_column1_rate_2026']
    assert US_2026_GOES_SECTION232_TARIFF.value == 0.50
    assert sec232['unit'] == 'additional ad valorem share of full customs value'
    assert '7225 and 7226' in sec232['scope_note']
    assert USITC_2026_GOES_COLUMN1_RATE.value == 0.0
    assert base['unit'] == 'Column 1 general ad valorem rate'
    assert 'distinct from additional' in base['scope_note']
    assert US_2026_GOES_SECTION232_TARIFF.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_north_american_component_routing_is_typed_dependence_context_not_goes_mass():
    r = goes_import_floor_result()
    e = r['context_evidence']['na_transformer_component_us_destination_2019']
    assert COMMERCE_2019_NA_TRANSFORMER_COMPONENT_US_DESTINATION.value == 0.90
    assert e['evidence_class'] == 'federal_report_trade_share_lower_bound'
    assert 'more than 99%' in e['scope_note']
    assert 'not GOES mass' in e['scope_note']
    assert COMMERCE_2019_NA_TRANSFORMER_COMPONENT_US_DESTINATION.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_2020_direct_goes_import_value_adds_source_concentration_without_fake_tonnage():
    r = goes_import_floor_result()
    e = r['context_evidence']['direct_goes_import_value_2020']
    assert DOE_2020_DIRECT_GOES_IMPORT_VALUE.value == 29.0
    assert e['unit'] == 'USD million imports'
    assert 'HS 722511' in e['scope_note']
    assert '85%' in e['scope_note'] and 'South Korea' in e['scope_note']
    assert 'not tonnes' in e['scope_note']
    assert DOE_2020_DIRECT_GOES_IMPORT_VALUE.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_eu_2026_core_safeguard_is_current_foreign_policy_context_not_us_supply():
    r = goes_import_floor_result()
    e = r['context_evidence']['eu_transformer_core_safeguard_duty_2026']
    assert EU_2026_TRANSFORMER_CORE_SAFEGUARD_DUTY.value == 1140.0
    assert e['unit'] == 'EUR per tonne of core'
    assert 'incorporated in transformers' in e['scope_note']
    assert 'not a U.S.-available supply quantity' in e['scope_note']
    assert EU_2026_TRANSFORMER_CORE_SAFEGUARD_DUTY.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_iea_global_capacity_is_context_not_us_available_supply():
    r = goes_import_floor_result()
    e = r['context_evidence']['global_goes_capacity_iea_2023']
    assert IEA_2023_GLOBAL_GOES_CAPACITY.value == 3.8
    assert e['unit'] == 'million tonnes GOES/year global production capacity'
    assert 'almost 85%' in e['scope_note']
    assert '6 Mt/year' in e['scope_note']
    assert 'scenario' in e['scope_note']
    assert IEA_2023_GLOBAL_GOES_CAPACITY.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_jfe_eaton_order_proves_real_us_foreign_goes_route_without_inventing_mass():
    r = goes_import_floor_result()
    e = r['context_evidence']['documented_us_foreign_goes_order_jfe_eaton_2024']
    assert JFE_2024_US_EATON_GOES_ORDER.value == 1.0
    assert e['evidence_class'] == 'producer_primary_documented_us_supply_route'
    assert 'Eaton Corporation' in e['scope_note']
    assert 'no order mass' in e['scope_note']
    assert JFE_2024_US_EATON_GOES_ORDER.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_commerce_scope_mapping_separates_direct_goes_from_embodied_components():
    r = goes_import_floor_result()
    e = r['context_evidence']['official_goes_vs_core_scope_mapping_2026']
    assert COMMERCE_2026_EU_GOES_SAFEGUARD_SCOPE.value == 3.0
    assert '7225.11.00' in e['scope_note'] and '7226.11.00' in e['scope_note']
    assert '8504.90.13' in e['scope_note']
    assert 'not U.S. trade tonnage' in e['scope_note']
    assert COMMERCE_2026_EU_GOES_SAFEGUARD_SCOPE.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_2024_distribution_transformer_material_demand_keeps_scope_and_provenance_separate():
    r = goes_import_floor_result()
    total = r['context_evidence']['distribution_transformer_core_steel_demand_2024']
    goes = r['context_evidence']['distribution_transformer_goes_consumption_mtc_2024']
    assert total['value'] == 225.0
    assert total['evidence_class'] == 'federal_final_rule_demand_estimate'
    assert 'not GOES alone' in total['scope_note']
    assert goes['value'] == 175.0
    assert goes['evidence_class'] == 'stakeholder_estimate_reported_in_federal_final_rule'
    assert 'not a DOE-measured customs series' in goes['scope_note']
    assert DOE_2024_DISTRIBUTION_TRANSFORMER_CORE_STEEL_DEMAND.evidence_id not in r['evidence_ids']
    assert MTC_2024_DISTRIBUTION_TRANSFORMER_GOES_CONSUMPTION.evidence_id not in r['evidence_ids']
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))


def test_commerce_goes_hts10_scope_resolves_fetch_coverage_without_inventing_recent_tonnage():
    r = goes_import_floor_result()
    e = r['context_evidence']['us_goes_hts10_scope_commerce_2014']
    codes = ('7225.11.0000', '7226.11.1000', '7226.11.9030', '7226.11.9060')
    assert e['value'] == 4.0
    assert e['evidence_class'] == 'federal_goes_product_scope_mapping'
    assert all(c in e['scope_note'] for c in codes)
    assert 'does not supply' in e['scope_note']
    assert COMMERCE_2014_US_GOES_HTS10_SCOPE.evidence_id not in r['evidence_ids']
    assert r['recent_imports_comparison']['status'] == 'not_ingested'
    assert r['import_floor_kt'] == pytest.approx((87.203815, 107.203815))
