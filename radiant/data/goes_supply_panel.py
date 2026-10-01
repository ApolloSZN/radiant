"""Vintage-safe GOES supply-response observations and trade-code coverage.

GOES spans two HS-6 headings (722511 and 722611), but direct U.S. import extraction
uses more granular HTSUSA codes.  Treating the two headings as if they were the
literal query codes can silently omit part of the <600 mm material.  This module
therefore keeps classification level, direction, and effective-period metadata
separate from the observations themselves.

Current Commerce/SIMA import coverage used in Run 027:
  7225110000  width >=600 mm, GOES
  7226111000  width 300-600 mm, GOES
  7226119030  width <300 mm, GOES, one thickness split
  7226119060  width <300 mm, GOES, other thickness split

Current export concordance is coarser for the narrow material:
  7225110000, 7226110000

These code sets are source/effective-period facts, not timeless ontology.  Historical
panel construction must use the concordance valid for each period rather than
blindly applying the current list backward.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# Coarse commodity identity. This remains useful for reasoning about coverage at
# HS-6, but is not sufficient by itself for a 10-digit U.S. import API query.
GOES_TRADE_CODES = {
    '7225.11': 'grain-oriented silicon electrical steel, width >=600 mm',
    '7226.11': 'grain-oriented silicon electrical steel, width <600 mm',
}

COMMERCE_SIMA_PRODUCT_CODES_URL = 'https://www.trade.gov/steel-products-hts-codes'
COMMERCE_EXPORT_CONCORDANCE_URL = 'https://www.trade.gov/export-monitor-concordance'
CENSUS_IMPORT_API_URL = 'https://api.census.gov/data/timeseries/intltrade/imports/hs'


@dataclass(frozen=True)
class TradeCodeSet:
    name: str
    direction: str
    classification: str
    effective_from: str
    effective_to: str | None
    codes: tuple[str, ...]
    source_url: str
    evidence_id: str


CURRENT_IMPORT_HTS = TradeCodeSet(
    name='goes_us_import_hts_current',
    direction='import',
    classification='HTSUSA-10',
    effective_from='current Commerce/SIMA concordance checked 2026-09-30',
    effective_to=None,
    codes=('7225110000', '7226111000', '7226119030', '7226119060'),
    source_url=COMMERCE_SIMA_PRODUCT_CODES_URL,
    evidence_id='COMMERCE_SIMA_CURRENT_HTS_GOES',
)

CURRENT_EXPORT_SCHEDULE_B = TradeCodeSet(
    name='goes_us_export_schedule_b_current',
    direction='export',
    classification='ScheduleB-10',
    effective_from='current Commerce export concordance checked 2026-09-30',
    effective_to=None,
    codes=('7225110000', '7226110000'),
    source_url=COMMERCE_EXPORT_CONCORDANCE_URL,
    evidence_id='COMMERCE_EXPORT_CURRENT_GOES',
)


@dataclass(frozen=True)
class VintageObservation:
    metric: str
    value: float
    unit: str
    period: str
    published_year: int
    evidence_id: str
    evidence_class: str
    scope: str = 'United States'


@dataclass(frozen=True)
class TradeCoverage:
    codes_present: tuple[str, ...]
    complete_for_goes_flat_products: bool
    missing_codes: tuple[str, ...]
    classification: str = 'HS6'
    direction: str = 'both/coarse'
    evidence_id: str = 'GOES_HS6_IDENTITY'


def _digits(code: str) -> str:
    return ''.join(ch for ch in str(code) if ch.isdigit())


def _normalize_hs6(code: str) -> str:
    d = _digits(code)
    if len(d) < 6:
        raise ValueError(f'commodity code must contain at least 6 digits: {code!r}')
    return d[:6]


def validate_trade_code_coverage(codes: Iterable[str], *, code_set: TradeCodeSet | None = None) -> TradeCoverage:
    """Validate GOES commodity coverage at the level actually being queried.

    With no ``code_set``, coverage is checked at HS-6 and preserves the Run 025 API.
    When a direction-specific 10-digit code set is supplied, every exact code in
    that concordance is required.  This prevents a query of 7225110000 + one
    722611 subcode from being mislabeled as total GOES imports.
    """
    raw = tuple(sorted({_digits(c) for c in codes}))
    if code_set is None:
        present6 = tuple(sorted({_normalize_hs6(c) for c in raw}))
        required6 = {'722511', '722611'}
        missing6 = tuple(sorted(required6 - set(present6)))
        pretty = tuple(f'{c[:4]}.{c[4:]}' for c in present6)
        missing_pretty = tuple(f'{c[:4]}.{c[4:]}' for c in missing6)
        return TradeCoverage(pretty, not missing6, missing_pretty)

    present = set(raw)
    required = set(code_set.codes)
    missing = tuple(sorted(required - present))
    return TradeCoverage(tuple(sorted(present)), not missing, missing,
                         code_set.classification, code_set.direction, code_set.evidence_id)


def aggregate_trade_quantity(rows: Iterable[dict], *, code_set: TradeCodeSet,
                             code_field: str = 'code', quantity_field: str = 'quantity_kg') -> float:
    """Aggregate a period only after exact concordance coverage is demonstrated.

    ``rows`` should already refer to one period and compatible quantity units.
    Missing codes are a hard error rather than an implicit zero because Census data
    can distinguish missing values from true zeroes.
    """
    rows = list(rows)
    coverage = validate_trade_code_coverage((r[code_field] for r in rows), code_set=code_set)
    if not coverage.complete_for_goes_flat_products:
        raise ValueError(f'incomplete {code_set.direction} GOES code coverage; missing {coverage.missing_codes}')
    by_code: dict[str, float] = {}
    for row in rows:
        code = _digits(row[code_field])
        if code not in code_set.codes:
            continue
        q = float(row[quantity_field])
        if q < 0:
            raise ValueError('trade quantity cannot be negative')
        by_code[code] = by_code.get(code, 0.0) + q
    return float(sum(by_code[c] for c in code_set.codes))


# Historical observations explicitly reported in Commerce's Section 232 transformer/
# GOES investigation. They are useful anchors, not a 2026 capacity forecast.
COMMERCE_2019 = (
    VintageObservation('apparent_consumption', 220_000.0, 'metric_tons/year', '2019', 2021,
                       'COMMERCE2021_SECTION232_GOES', 'reported_historical_estimate'),
    VintageObservation('imports', 27_000.0, 'metric_tons/year', '2019', 2021,
                       'COMMERCE2021_SECTION232_GOES', 'reported_historical_estimate'),
)


def historical_import_share_2019() -> float:
    vals = {o.metric: o.value for o in COMMERCE_2019}
    return vals['imports'] / vals['apparent_consumption']


def adequacy_identification_status(observations=COMMERCE_2019):
    """Fail closed unless the modeled horizon has a compatible supply envelope.

    Historical consumption/import observations cannot identify 2026+ available GOES
    supply. This function makes the missing empirical contract machine-readable.
    """
    metrics = {o.metric for o in observations}
    required = {'domestic_production_or_capacity', 'imports', 'exports', 'inventory_or_stock_change',
                'competing_consumption'}
    return {
        'historical_metrics_present': sorted(metrics),
        'modeled_horizon': '2026+ planning scenario',
        'adequacy_identified': False,
        'missing_supply_response_metrics': sorted(required - metrics),
        'reason': '2019 consumption/import anchors are not same-vintage 2026+ supply-response bounds.',
    }
