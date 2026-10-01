import pytest
from radiant.data import goes_balance as b


def _rows():
    return {r['year']: r for r in b.balance_sheet()}


def test_balance_sheet_covers_2015_2025_with_typed_cells():
    rows = _rows()
    assert sorted(rows) == list(range(2015, 2026))
    for r in rows.values():
        for k, v in r.items():
            if k == 'year':
                continue
            (lo, hi), kind = v
            assert lo <= hi and (kind.split()[0] in {'measured', 'estimate', 'model'} or kind == 'not reported'), (r['year'], k)


def test_only_identified_years_are_estimates_the_rest_are_model():
    rows = _rows()
    assert {y for y, r in rows.items() if r['production'][1].startswith('estimate')} == {2017, 2019}
    assert rows[2025]['foreign_share_all_forms'][1] == 'model'


def test_identity_checks_pass():
    c = b.identity_checks()
    assert c['production_le_capacity'] and c['balance_closes_2019'] and c['top_down_vs_bottom_up_overlap_2019']


def test_headline_2019():
    h = b.headline()
    lo, hi = h['foreign_share_2019_all_forms']
    assert 0.50 < lo < hi < 0.67
    slo, shi = h['foreign_share_2019_sheet_and_cores']
    assert 0.35 < slo < shi < 0.41  # Commerce's ~44% falls once re-exports are netted
    ulo, uhi = h['all_forms_use_2019_kt']
    assert 280 < ulo < uhi < 380


def test_outlook_foreign_share_stays_high_in_every_scenario():
    o = b.outlook()
    assert o[2035]['evidence_type'] == 'model'
    for k in ('current', 'expansion', 'diversion'):
        assert o[2035][k]['foreign_share'][0] > 0.45
    # Ordering: keeping exports at home and expanding Butler both lower dependence.
    assert o[2035]['diversion']['domestic_kt'] > o[2035]['expansion']['domestic_kt'] > o[2035]['current']['domestic_kt']
    assert b.headline()['foreign_share_2035_min_across_scenarios'] == pytest.approx(0.49, abs=0.01)


def test_minimum_over_whole_outlook_is_46_percent_not_49():
    h = b.headline()
    assert h['foreign_share_min_2026_2035_any_scenario'] == pytest.approx(0.46, abs=0.006)
    assert h['foreign_share_min_2026_2035_any_scenario'] < h['foreign_share_2035_min_across_scenarios']


def test_headline_numbers_in_docs_match_code():
    from pathlib import Path
    h = b.headline()
    lo, hi = h['foreign_share_2019_all_forms']
    ulo, uhi = h['all_forms_use_2019_kt']
    slo, shi = h['foreign_share_2019_sheet_and_cores']
    need = [f'{lo:.0%}'.rstrip('%') + '–' + f'{hi:.0%}', f'{ulo:.0f}–{uhi:.0f} kt', f'{slo:.0%}'.rstrip('%') + '–' + f'{shi:.0%}',
            f"{h['foreign_share_min_2026_2035_any_scenario']:.0%} or more"]
    for doc in ('README.md', 'docs/FINDINGS.md'):
        text = Path(doc).read_text()
        for s in need:
            assert s in text, (doc, s)


def test_2015_canada_mexico_split_is_marked_not_reported():
    r = {row['year']: row for row in b.balance_sheet()}
    assert r[2015]['domestic_exports_to_canada_mexico'][1] == 'not reported'
    assert r[2019]['domestic_exports_to_canada_mexico'][1] == 'measured'
