"""GOES import floor under grid expansion (Run 028).

Question: can domestic production cover U.S. grain-oriented electrical steel (GOES)
demand once modeled transmission expansion is added?

Identified quantity: a lower bound on the annual volume that must come from imports
(or from non-recurring stock drawdown), obtained from

    import_floor = baseline_use + grid_increment - domestic_capacity_upper_bound

where every term is either sourced or an explicit, separately reported condition.
The domestic term is an *upper* bound: Cleveland-Cliffs (sole U.S./North American
GOES producer) states capacity for all electrical steel, which includes
non-oriented grades, so GOES capacity cannot exceed it. Using an upper bound on
supply makes the floor conservative.

Refused conversions:
- the 2026 "25% growth" Butler hot-mill expansion is not converted into GOES
  finishing capacity (hot-mill throughput is not GOES output, and no absolute
  GOES figure was stated). It is reported only as a labeled scenario.
- baseline use is not reconstructed from NLR's ">45% of 2019-2023 consumption"
  inequality; the 2019 Commerce value is used as an explicit condition and the
  break-even baseline is reported so the reader can see how far it must fall.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict

SHORT_TON_T = 0.90718474


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    value: float
    unit: str
    period: str
    published: str
    evidence_class: str
    source: str
    scope_note: str


CLIFFS_ELECTRICAL_STEEL_CAPACITY = Evidence(
    'CLIFFS2020_GOES_232_RELEASE', 250_000 * SHORT_TON_T / 1000, 'kt/year', 'stated 2020', '2020-11-02',
    'company_stated_capacity_upper_bound',
    'https://www.clevelandcliffs.com/news/news-releases/detail/10/cleveland-cliffs-applauds-president-trumps-actions-to',
    'Up to 250,000 net tons/year of ALL electrical steel (GOES + non-oriented) at Butler and Zanesville; '
    'GOES capacity is at most this. Sole GOES producer in the U.S. and North America.')

CLIFFS_HOT_MILL_EXPANSION_2026 = Evidence(
    'BUTLEREAGLE_2026-08-08_CLIFFS_CEO', 0.25, 'relative (qualitative)', 'completion expected 2028', '2026-08-08',
    'qualitative_relative_statement_not_convertible',
    'https://www.butlereagle.com/20260807/cliffs-ceo-says-grain-oriented-steel-essential-as-dept-of-energy-mulls-2024-transformer-ruling/',
    '$195M Butler Works hot mill expansion described by the CEO as "25% growth"; baseline and GOES '
    'finishing impact not stated. Not converted into GOES capacity.')

DLA_GOES_STOCKPILE_CONTRACT = Evidence(
    'DLA_SP8000-25-D-0008_GOES', 53_000 * SHORT_TON_T / 1000 / 5, 'kt/year (ceiling, averaged)', 'FY2025-FY2029, ends 2030-09-08',
    '2026-07-01', 'contract_ceiling_reported',
    'https://www.steelmarketupdate.com/2026/07/06/cliffs-awarded-400m-goes-contract-from-department-of-war/',
    'Defense Logistics Agency sole-source IDIQ, up to $400M; volume "up to 53,000 short tons" stated by the '
    'Cliffs CEO (Q3 2025 call) and reported by multiple trade outlets; DoD announced the award 2026-07-01. '
    'Material is stockpiled, so it is domestic output unavailable to the grid. Ceiling, not a delivery schedule.')


CLIFFS_2025_STAINLESS_ELECTRICAL_SHIPMENTS = Evidence(
    'CLIFFS2025_10K_STAINLESS_ELECTRICAL_SHIPMENTS', 575.0, 'thousand net tons/year', 'FY2025', '2026-02-09',
    'company_sec_filing_measured_aggregate',
    'https://www.clevelandcliffs.com/investors/sec-filings/all-sec-filings/content/0000764065-26-000025/0000764065-26-000025.pdf',
    'Cleveland-Cliffs FY2025 Form 10-K reports 575 thousand net tons of combined stainless AND electrical-steel shipments. '
    'This is measured company output but is not GOES-specific, so it cannot replace the GOES capacity upper bound.')

DOE_2024_DISTRIBUTION_TRANSFORMER_FINAL_RULE = Evidence(
    'DOE2024_DISTRIBUTION_TRANSFORMER_FINAL_RULE', 0.75, 'share of market able to comply using GOES (approx.)',
    'standards compliance from 2029-04-23', '2024-04-04', 'federal_final_rule_policy_parameter',
    'https://www.energy.gov/articles/doe-finalizes-energy-efficiency-standards-distribution-transformers-protect-domestic',
    'DOE says about 75% of the distribution-transformer market can meet the final standards with GOES; the initial proposal '
    'would likely have shifted about 95% of the market to amorphous alloy. This is a technology-mix constraint, not tonnage.')

DOE_2024_DISTRIBUTION_TRANSFORMER_CORE_STEEL_DEMAND = Evidence(
    'DOE2024_DT_CORE_STEEL_DEMAND', 225.0, 'kt/year electrical steel for U.S. distribution transformers',
    'current demand estimate in 2024 final rule', '2024-04-22', 'federal_final_rule_demand_estimate',
    'https://www.energy.gov/sites/default/files/2024-04/dt_ecs_fr.pdf',
    'DOE final rule estimates current domestic demand for electrical steel used in distribution transformers at approximately '
    '225,000 metric tons. This covers transformer core electrical steel, not GOES alone, so it cannot replace the 2019 all-use '
    'GOES baseline or be added to it without double counting. The same rule separately reports an MTC stakeholder estimate of '
    'about 175,000 metric tons of GOES consumption for distribution transformers.')

MTC_2024_DISTRIBUTION_TRANSFORMER_GOES_CONSUMPTION = Evidence(
    'MTC2024_DT_GOES_CONSUMPTION_REPORTED_BY_DOE', 175.0, 'kt/year GOES for U.S. distribution transformers',
    'stakeholder current-consumption estimate entered in 2024 DOE rulemaking', '2024-04-22',
    'stakeholder_estimate_reported_in_federal_final_rule',
    'https://public-inspection.federalregister.gov/2024-07480.pdf',
    'DOE final rule records MTC comment that U.S. consumption of GOES for distribution transformers is approximately 175K MT. '
    'This is a stakeholder estimate preserved with its provenance, not a DOE-measured customs series and not an all-use GOES '
    'total. It is therefore context evidence only and is not inserted into the import-floor equation.')

DOE_2026_DISTRIBUTION_TRANSFORMER_RFI = Evidence(
    'DOE2026_DISTRIBUTION_TRANSFORMER_RFI', 2029.0, 'compliance year', 'RFI issued 2026-06-15', '2026-06-15',
    'federal_rule_status',
    'https://www.energy.gov/cmei/articles/doe-issues-request-information-rfi-energy-conservation-standards-distribution',
    'DOE states the April 2024 final standards remain scheduled for compliance on April 23, 2029 while DOE re-examines '
    'national-security, domestic-capacity, supply-chain and core-steel impacts. An RFI is not a rescission or replacement rule.')

COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS = Evidence(
    'COMMERCE2020_SECTION232_GOES_EMBODIED_CORES_2019', 68.0, 'kt GOES-equivalent', 'calendar 2019', '2021-11-18',
    'federal_report_estimate_from_industry_weight_estimate',
    'https://public-inspection.federalregister.gov/2021-24958.pdf',
    'Commerce Section 232 report (completed 2020-10-15; Federal Register publication 2021-11-18) estimates that U.S. imports of transformer laminations and cores contained 68,000 metric tons '
    'of GOES in 2019. Customs data for these core products are collected in units, not weight; Commerce states the weight '
    'estimate is based on Core Coalition public comments. The report notes possible but likely minimal double counting from '
    'U.S.-origin GOES exported and then re-imported in cores. This is derivative-product dependence, not direct GOES sheet imports.')

COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS = Evidence(
    'COMMERCE2020_SECTION232_CORE_COALITION_2020_ESTIMATE', 96.0, 'kt GOES-equivalent', 'calendar 2020 estimate', '2021-11-18',
    'industry_estimate_reported_by_federal_agency',
    'https://public-inspection.federalregister.gov/2021-24958.pdf',
    'Commerce Section 232 report (completed 2020-10-15; Federal Register publication 2021-11-18) reports the Core Coalition estimate that 2020 U.S. core imports would contain 96,000 metric tons of GOES and '
    'states that first-half 2020 trade data validated the direction of the increase. This is an industry estimate reported in an '
    'official federal investigation, not a directly measured annual customs weight.')

CLIFFS_2025_LAMINATION_IMPORT_UNITS_2024 = Evidence(
    'CLIFFS2025_DATAWEB_LAMINATION_IMPORTS_2024', 147_652_598.0, 'units', 'calendar 2024', '2025-06-03',
    'company_federal_docket_trade_table_citing_usitc_dataweb',
    'https://downloads.regulations.gov/BIS-2025-0023-0356/attachment_1.pdf',
    'A Cleveland-Cliffs submission in Commerce docket BIS-2025-0023 includes a USITC DataWeb table for HTS '
    '8504.90.9534 and 8504.90.9634 showing 147,652,598 U.S. imports in 2024 of laminations for incorporation '
    'into stacked cores, down 17% from 177,844,193 units in 2023. Mexico supplied 129,877,076 units in 2024. '
    'The customs quantity is units, not mass; it therefore documents the scale and routing of the derivative-product '
    'channel but cannot replace or update the 68 kt 2019 embodied-GOES estimate without a defensible unit-weight mapping.')

CLIFFS_2025_LAMINATION_IMPORT_UNITS_2025_YTD = Evidence(
    'CLIFFS2025_DATAWEB_LAMINATION_IMPORTS_2025_JAN_FEB', 25_059_726.0, 'units', 'January-February 2025', '2025-06-03',
    'company_federal_docket_trade_table_citing_usitc_dataweb',
    'https://downloads.regulations.gov/BIS-2025-0023-0356/attachment_1.pdf',
    'The same Cleveland-Cliffs/USITC DataWeb table reports 25,059,726 lamination units imported in January-February '
    '2025 under HTS 8504.90.9534 and 8504.90.9634, 6% above the same period of 2024. This is a partial-year unit '
    'count, not tonnes and not an annualized estimate; Radiant does not extrapolate it or insert it into the tonnage floor.')

DOE_2021_STACKED_CORE_IMPORT_UNITS = Evidence(
    'DOE2022_GRID_SUPPLY_CHAIN_STACKED_CORE_IMPORTS_2021_YTD_OCT', 842_929.0, 'units', '2021 through October', '2022-02-24',
    'federal_report_trade_count',
    'https://www.energy.gov/sites/default/files/2024-12/Electric%20Grid%20Supply%20Chain%20Report%20-%20Final%5B1%5D.pdf',
    'DOE reports 842,929 U.S. imports through October 2021 under HTS 8504.90.9638, Stacked Cores for Incorporation into '
    'Transformer Parts, versus 50,267 units in 2016, using USA Trade Online. Unit counts cannot be converted to GOES mass '
    'without a defensible weight distribution, so this evidence is not inserted into the tonnage floor.')

JFE_JSW_INDIA_GOES_JV_INVESTMENT = Evidence(
    'JFE2024_JSW_INDIA_GOES_JV_INVESTMENT', 670.0, 'USD million planned investment',
    'full operation planned FY2027', '2024-02-13', 'producer_announced_goes_capacity_investment_not_tonnage',
    'https://www.jfe-steel.co.jp/en/release/2024/02/240213.html',
    'JFE Steel states its 50:50 JSW joint venture in Bellary, India is dedicated to conventional and high-permeability GOES, '
    'with $670 million total investment and full operation planned from FY2027. No tonnage capacity is stated, so this is '
    'evidence of a new foreign GOES supply project, not a quantity available to the U.S. and not an input to the import floor.')

JFE_JSW_INDIA_GOES_CAPACITY_2030 = Evidence(
    'JFE2025_JSW_INDIA_GOES_CAPACITY_2030', 350.0, 'kt GOES/year planned capacity',
    'Vijayanagar by 2027; Nashik expansion phased 2028-2030', '2025-08-04',
    'producer_announced_future_goes_nameplate_capacity',
    'https://www.jfe-steel.co.jp/en/release/2025/08/250804.html',
    'JFE Steel states the two 50:50 JSW-JFE India GOES ventures are planned to reach 350,000 tonnes/year combined: '
    '100,000 tpy at Vijayanagar and 250,000 tpy at Nashik, whose current capacity is 50,000 tpy. This is announced future '
    'nameplate capacity aimed at Indian demand, not observed production, export availability, or capacity committed to the U.S.; '
    'therefore it is supply context only and is not subtracted from the U.S. import floor.')

THYSSENKRUPP_ISBERGUES_2026_CURTAILMENT = Evidence(
    'TKES2026_ISBERGUES_GOES_CURTAILMENT', 0.50, 'share of total site capacity operated',
    'January-May 2026; complete shutdown announced June-September 2026', '2026-03-26',
    'producer_reported_foreign_goes_supply_curtailment',
    'https://www.thyssenkrupp-steel.com/en/newsroom/press-releases/thyssenkrupp-electrical-steel-extends-production-cuts-at-its-isbergues-site-in-france.html',
    'thyssenkrupp Electrical Steel states its Isbergues, France GOES site had operated at 50% of total capacity since January '
    '2026 and would be fully shut June-September 2026. This is a supplier statement about utilization, not audited output, '
    'and does not identify how much material could otherwise have supplied the United States.')


DOE_2020_DIRECT_GOES_IMPORT_VALUE = Evidence(
    'DOE2022_GRID_SUPPLY_CHAIN_2020_DIRECT_GOES_IMPORT_VALUE', 29.0, 'USD million imports',
    'calendar 2020; HS 722511', '2022-02-24', 'federal_report_trade_value_and_source_shares',
    'https://www.energy.gov/sites/default/files/2024-12/Electric%2520Grid%2520Supply%2520Chain%2520Report%2520-%2520Final%5B1%5D.pdf',
    'DOE Electric Grid Supply Chain report states that in 2020 the United States spent $29 million on GOES imports under '
    'HS 722511; 85% of import value came from South Korea, 6% from Brazil, and 4% from Russia (citing USA Trade Online 2021). '
    'This is an official published trade-value observation with source-country shares, not tonnes. It covers HS 722511 only, '
    'so it must not be treated as the complete 7225.11 + 7226.11 direct-GOES mass panel or converted to mass without price data.')


COMMERCE_2019_NA_TRANSFORMER_COMPONENT_US_DESTINATION = Evidence(
    'COMMERCE2020_SECTION232_NA_COMPONENT_US_DESTINATION', 0.90, 'share of Canadian transformer-component exports to U.S. (lower bound)',
    'calendar 2019 context', '2021-11-18', 'federal_report_trade_share_lower_bound',
    'https://www.federalregister.gov/documents/2021/11/18/2021-24958/publication-of-a-report-on-the-effect-of-imports-of-transformers-and-transformer-components-on-the',
    'Commerce Section 232 report states that more than 90% of Canada transformer-component exports and more than 99% of '
    'Mexico transformer-component exports were destined for the United States. The report also states neither Canada nor '
    'Mexico had domestic GOES production capability, so their increased core/lamination production required imported GOES. '
    'The stored 0.90 value is only the published lower bound for Canada; Mexico >99% is retained in this scope note. This is '
    'routing/dependence evidence, not GOES mass and not a term in the U.S. import-floor equation.')

US_2026_GOES_SECTION232_TARIFF = Evidence(
    'US2026_SECTION232_GOES_STEEL_ARTICLE_TARIFF', 0.50, 'additional ad valorem share of full customs value',
    'effective 2026-04-06; confirmed in 2026-06-01 Proclamation 11032 annex', '2026-06-04',
    'federal_proclamation_current_tariff_parameter',
    'https://public-inspection.federalregister.gov/2026-11314.pdf',
    'Presidential Proclamation 11021 set a 50% Section 232 duty on products made of steel, effective April 6, 2026. '
    'Proclamation 11032, published June 4, 2026, retains a 50% tariff on the full value of steel articles in Annex I-A; '
    'that annex expressly includes headings 7225 and 7226, which contain GOES HTS 7225.11 and 7226.11. This is the '
    'additional Section 232 rate, not a measured trade response or an effect size. Country/product exceptions must be '
    'evaluated under the operative HTS Chapter 99 provisions for a specific entry.')

USITC_2026_GOES_COLUMN1_RATE = Evidence(
    'USITC2026_HTS_GOES_COLUMN1_GENERAL_RATE', 0.0, 'Column 1 general ad valorem rate',
    'current HTSUS accessed 2026-09-30', '2026-09-30', 'official_tariff_schedule_parameter',
    'https://hts.usitc.gov/',
    'Current HTSUS lists GOES 7225.11.00 and the 7226.11 grain-oriented provisions with a Free Column 1 general rate. '
    'That base rate is distinct from additional Chapter 99/Section 232 duties; it must not be interpreted as a zero total tariff.')


IEA_2023_GLOBAL_GOES_CAPACITY = Evidence(
    'IEA2023_GLOBAL_GOES_CAPACITY_AND_CONCENTRATION', 3.8, 'million tonnes GOES/year global production capacity',
    'capacity described as current in Energy Technology Perspectives 2023; demand scenario 2022-2030', '2023-01-12',
    'intergovernmental_agency_capacity_and_scenario',
    'https://www.iea.org/reports/energy-technology-perspectives-2023/enabling-infrastructure',
    'IEA Energy Technology Perspectives 2023 states global GOES production capacity is about 3.8 Mt/year and that China, '
    'Japan, Korea, Russia, and the United States account for almost 85% of it. In the IEA Net Zero Emissions scenario, GOES '
    'demand doubles to 6 Mt/year over 2022-2030. The 3.8 Mt/year figure is capacity context; 6 Mt/year is a scenario demand '
    'trajectory, not observed demand and not evidence of U.S.-available supply or a shortage.')

JFE_2024_US_EATON_GOES_ORDER = Evidence(
    'JFE2024_JGREEX_US_EATON_GOES_ORDER', 1.0, 'documented first U.S. JGreeX GOES application/order',
    'order announced 2024-06-20', '2024-06-20', 'producer_primary_documented_us_supply_route',
    'https://www.jfe-steel.co.jp/en/release/2024/06/240620.html',
    'JFE Steel states its grain-oriented JGreeX steel was selected by a U.S. manufacturer of IT data-center transformers, '
    'its first JGreeX application in the United States, with delivery to Eaton Corporation through Toyota Tsusho. The '
    'release gives no order mass, price, or recurring annual volume, so this proves an actual foreign-to-U.S. GOES supply '
    'route but cannot be converted into tonnes or subtracted from the U.S. import floor.')


COMMERCE_2014_US_GOES_HTS10_SCOPE = Evidence(
    'COMMERCE2014_GOES_HTS10_SCOPE', 4.0, 'HTSUS statistical/tariff lines covering GOES investigation scope',
    'Commerce GOES investigation; published 2014', '2014-03-05', 'federal_goes_product_scope_mapping',
    'https://enforcement.trade.gov/download/factsheets/factsheet-prc-goes-cvd-prelim-030514.pdf',
    'Commerce identifies GOES in U.S. customs statistics under HTSUS 7225.11.0000, 7226.11.1000, 7226.11.9030, and '
    '7226.11.9060. Commerce also reports its historical import statistics from U.S. Census Bureau data using exactly these '
    'four lines. This resolves the concrete HTS10 coverage needed by Radiant direct-GOES fetch/check path, but it does not '
    'supply the still-missing 2020-2025 annual quantities. The written product description remains dispositive for the '
    'investigation; codes are a customs/statistical mapping, not evidence that every future classification revision is unchanged.')

COMMERCE_2026_EU_GOES_SAFEGUARD_SCOPE = Evidence(
    'COMMERCE2026_EU_GOES_SAFEGUARD_SCOPE_CODES', 3.0, 'covered EU tariff headings',
    'EU safeguard investigation period 2021-2025; notice summarized 2026-03-27', '2026-03-27',
    'us_commerce_official_product_scope_mapping',
    'https://www.trade.gov/european-union-initiates-safeguard-investigation-global-imports-certain-grain-oriented-flat-rolled',
    'U.S. Commerce identifies the EU safeguard product scope as GOES under tariff headings 7225.11.00 and 7226.11.00, plus '
    'steel laminations and cores under 8504.90.13. This is an official scope mapping, not U.S. trade tonnage. It strengthens '
    'the measurement design by keeping direct GOES (7225.11/7226.11) separate from embodied core/lamination trade (8504.90).')

EU_2026_TRANSFORMER_CORE_SAFEGUARD_DUTY = Evidence(
    'EU2026_GOES_TRANSFORMER_CORE_PROVISIONAL_SAFEGUARD', 1140.0, 'EUR per tonne of core',
    'effective 2026-09-25 through 2027-02-26 (provisional)', '2026-09-23',
    'official_government_summary_of_eu_provisional_safeguard',
    'https://mpo.gov.cz/cz/zahranicni-obchod/spolecna-obchodni-politika-eu/ochrana-obchodu-antidumpingova-antisubvencni-a-ochranna-opatreni/ulozena-prozatimni-safeguardova-opatreni-na-dovozy-goes--294684/',
    'Czech Ministry of Industry and Trade summary of Commission Implementing Regulation (EU) 2026/2133 states that, from '
    '25 September 2026, transformer cores imported already incorporated in transformers are outside the quota mechanism but '
    'subject to a provisional specific duty of EUR 1,140 per tonne of core; the provisional measure runs through 26 February '
    '2027. The underlying EU regulation covers GOES, laminations and cores. This is a current foreign trade-policy constraint, '
    'not a measured diversion of GOES toward or away from the United States and not a U.S.-available supply quantity.')

COMMERCE_2019_CONSUMPTION_KT = 220.0   # COMMERCE2021_SECTION232_GOES (see goes_supply_panel)
COMMERCE_2019_IMPORTS_KT = 27.0
NLR2026_GRID_INCREMENT_KT = (94.0, 114.0)  # NLR2026 transmission expansion, see lpt_evidence_network


def import_floor(baseline_kt: float, increment_kt: float, domestic_cap_kt: float) -> float:
    if min(baseline_kt, increment_kt, domestic_cap_kt) < 0:
        raise ValueError('inputs must be non-negative')
    return max(0.0, baseline_kt + increment_kt - domestic_cap_kt)


def goes_import_floor_result(scenario_capacity_multiplier: float | None = 1.25) -> dict:
    cap = CLIFFS_ELECTRICAL_STEEL_CAPACITY.value
    lo_inc, hi_inc = NLR2026_GRID_INCREMENT_KT
    base = COMMERCE_2019_CONSUMPTION_KT
    floor = (import_floor(base, lo_inc, cap), import_floor(base, hi_inc, cap))
    breakeven = (cap - hi_inc, cap - lo_inc)
    out = {
        'schema': 'radiant.goes_import_floor.v1',
        'question': 'Minimum annual GOES imports (or stock drawdown) if grid expansion demand is added to 2019-level use',
        'domestic_capacity_upper_bound_kt': cap,
        'baseline_condition_kt': base,
        'grid_increment_kt': NLR2026_GRID_INCREMENT_KT,
        'import_floor_kt': floor,
        'import_floor_multiple_of_2019_imports': tuple(f / COMMERCE_2019_IMPORTS_KT for f in floor),
        'breakeven_baseline_kt': breakeven,
        'baseline_decline_needed_for_zero_floor': tuple(1 - b / base for b in breakeven),
        'identified': True,
        'evidence_class': 'identified_conditional_bound',
        'conditions': [
            'non-grid GOES use stays near its 2019 level (break-even baseline reported)',
            'domestic GOES output cannot exceed stated all-electrical-steel capacity',
            'exports and recurring stock drawdown are not counted as domestic supply (either would raise the floor or is non-recurring)',
            'NLR grid increment is annual planning-scenario demand, not an observed order book',
        ],
        'not_claimed': [
            'that imports will be unavailable (no shortage call)',
            'a price or tariff effect',
            'the timing of the NLR demand path',
        ],
        'evidence_ids': [CLIFFS_ELECTRICAL_STEEL_CAPACITY.evidence_id, 'COMMERCE2021_SECTION232_GOES',
                         'NLR2026_TP_6A40_97167_FIG10_USITC_APPARENT_CONSUMPTION'],
        'context_evidence': {
            'producer_2025_shipments': asdict(CLIFFS_2025_STAINLESS_ELECTRICAL_SHIPMENTS),
            'distribution_transformer_rule': asdict(DOE_2024_DISTRIBUTION_TRANSFORMER_FINAL_RULE),
            'distribution_transformer_core_steel_demand_2024': asdict(DOE_2024_DISTRIBUTION_TRANSFORMER_CORE_STEEL_DEMAND),
            'distribution_transformer_goes_consumption_mtc_2024': asdict(MTC_2024_DISTRIBUTION_TRANSFORMER_GOES_CONSUMPTION),
            'distribution_transformer_rule_status_2026': asdict(DOE_2026_DISTRIBUTION_TRANSFORMER_RFI),
            'embodied_goes_2019_core_imports': asdict(COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS),
            'embodied_goes_2020_core_imports_estimate': asdict(COMMERCE_2020_GOES_EMBODIED_IN_CORE_IMPORTS),
            'stacked_core_import_units_2021_ytd_oct': asdict(DOE_2021_STACKED_CORE_IMPORT_UNITS),
            'foreign_goes_project_jfe_jsw_india': asdict(JFE_JSW_INDIA_GOES_JV_INVESTMENT),
            'foreign_goes_capacity_jfe_jsw_india_2030': asdict(JFE_JSW_INDIA_GOES_CAPACITY_2030),
            'foreign_goes_curtailment_thyssenkrupp_isbergues_2026': asdict(THYSSENKRUPP_ISBERGUES_2026_CURTAILMENT),
            'direct_goes_import_value_2020': asdict(DOE_2020_DIRECT_GOES_IMPORT_VALUE),
            'na_transformer_component_us_destination_2019': asdict(COMMERCE_2019_NA_TRANSFORMER_COMPONENT_US_DESTINATION),
            'us_goes_section232_tariff_2026': asdict(US_2026_GOES_SECTION232_TARIFF),
            'us_goes_column1_rate_2026': asdict(USITC_2026_GOES_COLUMN1_RATE),
            'eu_transformer_core_safeguard_duty_2026': asdict(EU_2026_TRANSFORMER_CORE_SAFEGUARD_DUTY),
            'official_goes_vs_core_scope_mapping_2026': asdict(COMMERCE_2026_EU_GOES_SAFEGUARD_SCOPE),
            'us_goes_hts10_scope_commerce_2014': asdict(COMMERCE_2014_US_GOES_HTS10_SCOPE),
            'global_goes_capacity_iea_2023': asdict(IEA_2023_GLOBAL_GOES_CAPACITY),
            'documented_us_foreign_goes_order_jfe_eaton_2024': asdict(JFE_2024_US_EATON_GOES_ORDER),
            'embodied_core_to_direct_goes_import_ratio_2019': COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.value / COMMERCE_2019_IMPORTS_KT,
            'interpretation': (
                'The producer/policy facts constrain supply context. The 2020 DOE trade-value observation adds measured source-country concentration for HS 722511 but is not converted to tonnes. The core-import facts show that steel-form trade materially '
                'understates U.S. dependence on foreign GOES because GOES also arrives embedded in laminations and cores. '
                'The JFE/JSW 350 kt/year figure is planned Indian nameplate capacity and is not assumed available to the U.S. The 2026 tariff facts are policy parameters, not assumed quantity responses. These context facts do not change the tonnage floor. The 2019 68 kt figure is an estimate based on industry '
                'weight assumptions, the 2020 96 kt value is an industry estimate reported by Commerce, and the 2021 value is '
                'a unit count that cannot be converted to mass without an evidenced weight distribution.'
            )
        },
    }
    stock = DLA_GOES_STOCKPILE_CONTRACT.value
    out['defense_stockpile_adjustment'] = {
        'evidence_class': 'contract_ceiling_reported',
        'evidence_id': DLA_GOES_STOCKPILE_CONTRACT.evidence_id,
        'max_additional_floor_kt_per_year': stock,
        'import_floor_if_ceiling_fully_drawn_kt': (floor[0] + stock, floor[1] + stock),
        'note': 'Upper adjustment only: the identified floor above does not depend on it.',
    }
    try:
        from radiant.data.goes_trade_annual import load_annual_goes_trade, latest_complete_imports
        latest = latest_complete_imports(load_annual_goes_trade())
    except Exception:
        latest = None
    if latest:
        y, t = latest
        out['recent_imports_comparison'] = {
            'year': y, 'imports_kt': t / 1000.0,
            'import_floor_multiple_of_recent_imports': tuple(f / (t / 1000.0) for f in floor) if t else None,
            'source': 'data/goes/goes_trade_annual.csv (Census International Trade API, HS6 722511+722611; '
                      'tonnes from HS10 kg when Census reports no HS6 quantity)',
        }
    else:
        out['recent_imports_comparison'] = {'status': 'not_ingested',
            'how_to_fix': 'python scripts/fetch_goes_trade.py (needs access to api.census.gov)'}
    if scenario_capacity_multiplier is not None:
        scap = cap * scenario_capacity_multiplier
        sfloor = (import_floor(base, lo_inc, scap), import_floor(base, hi_inc, scap))
        out['scenario_capacity_expansion'] = {
            'evidence_class': 'scenario_assumption',
            'assumption': f'IF all electrical-steel capacity grew {scenario_capacity_multiplier - 1:.0%} and all of it were GOES',
            'related_evidence': asdict(CLIFFS_HOT_MILL_EXPANSION_2026),
            'import_floor_kt': sfloor,
            'import_floor_multiple_of_2019_imports': tuple(f / COMMERCE_2019_IMPORTS_KT for f in sfloor),
        }
    return out



def all_forms_view() -> dict:
    """Run 053: count foreign GOES in every form, not just sheet.

    The headline multiple "3-4x 2019 imports" divided a sheet-import floor by sheet
    imports alone (27 kt). Commerce estimates a further 68 kt of GOES entered in 2019
    already embodied in imported laminations/cores. The NLR grid increment is total
    GOES content regardless of where cores are made, so the like-for-like comparison
    counts sheet + embodied cores on both sides. Finished-transformer imports are
    excluded on both sides (no tonnage evidence), so they cancel rather than bias.
    """
    cap = CLIFFS_ELECTRICAL_STEEL_CAPACITY.value
    cores = COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.value
    use_2019 = COMMERCE_2019_CONSUMPTION_KT + cores
    foreign_2019 = COMMERCE_2019_IMPORTS_KT + cores
    lo, hi = NLR2026_GRID_INCREMENT_KT
    floor = (use_2019 + lo - cap, use_2019 + hi - cap)
    need = (use_2019 + lo, use_2019 + hi)
    return {
        'schema': 'radiant.goes_all_forms_view.v1',
        'us_goes_use_2019_all_forms_kt': use_2019,
        'foreign_goes_2019_all_forms_kt': foreign_2019,
        'foreign_share_2019': foreign_2019 / use_2019,
        'foreign_goes_floor_all_forms_kt': floor,
        'floor_multiple_of_2019_foreign_all_forms': tuple(f / foreign_2019 for f in floor),
        'foreign_share_floor': tuple(f / n for f, n in zip(floor, need)),
        'sheet_only_multiple_withdrawn_as_headline': True,
        'evidence_class': 'identified_conditional_bound',
        'conditions': ['non-grid GOES use stays near 2019 (sheet 220 kt + embodied cores 68 kt)',
                       '68 kt embodied-core figure is a Commerce estimate from industry weight data, not customs tonnage',
                       'finished-transformer imports excluded on both sides'],
        'evidence_ids': [CLIFFS_ELECTRICAL_STEEL_CAPACITY.evidence_id, 'COMMERCE2021_SECTION232_GOES',
                         COMMERCE_2019_GOES_EMBODIED_IN_CORE_IMPORTS.evidence_id, 'NLR2026_TP_6A40_97167_FIG10_USITC_APPARENT_CONSUMPTION'],
    }

if __name__ == '__main__':
    import json
    print(json.dumps({'sheet_channel': goes_import_floor_result(), 'all_forms': all_forms_view()}, indent=2, default=str))
