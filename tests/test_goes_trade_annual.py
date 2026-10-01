import csv, importlib.util
from pathlib import Path
from radiant.data.goes_trade_annual import load_annual_goes_trade, latest_complete_imports
from radiant.data.goes_import_floor import goes_import_floor_result

F = ['year','direction','level','code','quantity','unit','value_usd','status','source_url','retrieved_at']

def _write(p, rows):
    with open(p, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=F); w.writeheader()
        for r in rows: w.writerow({**{k: '' for k in F}, **r})

def _row(y, d, lvl, c, q, unit='KG', status='ok'):
    return dict(year=y, direction=d, level=lvl, code=c, quantity=q, unit=unit, status=status, source_url='u')

def test_missing_file_is_none_and_floor_says_not_ingested(tmp_path, monkeypatch):
    assert load_annual_goes_trade(tmp_path / 'nope.csv') is None
    monkeypatch.chdir(tmp_path)
    assert goes_import_floor_result()['recent_imports_comparison']['status'] == 'not_ingested'

def test_year_incomplete_if_one_hs6_heading_missing(tmp_path):
    p = tmp_path / 't.csv'
    _write(p, [_row(2024,'imports','HS6','722511', 30_000_000), _row(2024,'imports','HS6','722611', '', status='no_rows_returned')])
    t = load_annual_goes_trade(p)
    assert t[2024]['imports']['complete'] is False and t[2024]['imports']['tonnes'] is None
    assert latest_complete_imports(t) is None

def test_complete_year_sums_hs6_and_checks_hs10(tmp_path):
    p = tmp_path / 't.csv'
    _write(p, [_row(2024,'imports','HS6','722511', 30_000_000), _row(2024,'imports','HS6','722611', 10_000_000),
               _row(2024,'imports','HS10','7225110000', 30_000_000), _row(2024,'imports','HS10','7226111000', 4_000_000),
               _row(2024,'imports','HS10','7226119030', 3_000_000), _row(2024,'imports','HS10','7226119060', 3_000_000)])
    t = load_annual_goes_trade(p)
    assert t[2024]['imports']['tonnes'] == 40_000 and t[2024]['imports']['hs10_check'] == 'match'
    assert latest_complete_imports(t) == (2024, 40_000)

def test_wrong_unit_fails_closed(tmp_path):
    p = tmp_path / 't.csv'
    _write(p, [_row(2024,'imports','HS6','722511', 1, unit='T'), _row(2024,'imports','HS6','722611', 1)])
    assert load_annual_goes_trade(p)[2024]['imports']['complete'] is False

def test_stockpile_is_upper_adjustment_only():
    r = goes_import_floor_result()
    adj = r['defense_stockpile_adjustment']
    assert 9 < adj['max_additional_floor_kt_per_year'] < 10
    assert adj['import_floor_if_ceiling_fully_drawn_kt'][0] > r['import_floor_kt'][0]
    assert 'DLA_SP8000-25-D-0008_GOES' not in r['evidence_ids']

def test_fetch_script_world_total_prefers_total_row():
    spec = importlib.util.spec_from_file_location('f', Path('scripts/fetch_goes_trade.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    rows = [['I_COMMODITY','CTY_CODE','CTY_NAME','CON_QY1_YR','UNIT_QY1','CON_VAL_YR','time'],
            ['722511','-','TOTAL FOR ALL COUNTRIES','500','KG','9','2024-12'],
            ['722511','5880','JAPAN','300','KG','5','2024-12'], ['722511','4280','GERMANY','200','KG','4','2024-12']]
    assert m._world_total(rows) == (500.0, 'KG', 9.0)
    assert m._world_total([rows[0]] + rows[2:])[0] == 500.0

def test_run030_context_evidence_is_typed_and_does_not_change_floor():
    r = goes_import_floor_result()
    assert r['import_floor_kt'][0] > 80
    c = r['context_evidence']
    assert c['producer_2025_shipments']['value'] == 575.0
    assert 'combined stainless AND electrical' in c['producer_2025_shipments']['scope_note']
    assert c['distribution_transformer_rule']['value'] == 0.75
    assert c['distribution_transformer_rule_status_2026']['value'] == 2029.0
    assert 'do not change the tonnage floor' in c['interpretation']

def test_fetch_main_fails_closed_when_required_hs6_errors(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('fetch_fail_closed', Path('scripts/fetch_goes_trade.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    monkeypatch.setattr(m, 'OUT', tmp_path / 'trade.csv')
    def fake_get(direction, year, code, level):
        if level == 'HS6' and code == '722611':
            raise OSError('network unavailable')
        q = '1' if direction == 'imports' else '2'
        commodity = 'I_COMMODITY' if direction == 'imports' else 'E_COMMODITY'
        qty = 'CON_QY1_YR' if direction == 'imports' else 'QTY_1_YR'
        val = 'CON_VAL_YR' if direction == 'imports' else 'ALL_VAL_YR'
        return [[commodity,'CTY_CODE','CTY_NAME',qty,'UNIT_QY1',val],
                [code,'-','TOTAL FOR ALL COUNTRIES',q,'KG','10']], 'https://example.test'
    monkeypatch.setattr(m, '_get', fake_get)
    assert m.main(['fetch_goes_trade.py','2025','2025']) == 2
    rows = list(csv.DictReader((tmp_path/'trade.csv').open()))
    assert any(r['level']=='HS6' and r['status'].startswith('error:') for r in rows)


def test_fetch_contract_uses_consumption_quantities_and_sourced_hts10_scope():
    spec = importlib.util.spec_from_file_location('fetch_contract', Path('scripts/fetch_goes_trade.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    assert m.IMPORT_HS10 == ('7225110000','7226111000','7226119030','7226119060')
    # Census defines CON_QY1_YR as year-to-date imports-for-consumption quantity 1.
    # Material-balance ingestion must not silently switch to general-import quantity.
    class Resp:
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def read(self): return b'[["I_COMMODITY","CTY_CODE","CTY_NAME","CON_QY1_YR","UNIT_QY1","CON_VAL_YR"],["722511","-","TOTAL FOR ALL COUNTRIES","1","KG","2"]]'
    seen = {}
    def fake_urlopen(url, timeout=60):
        seen['url'] = url; return Resp()
    old = m.urllib.request.urlopen; m.urllib.request.urlopen = fake_urlopen
    try: rows, _ = m._get('imports', 2025, '722511', 'HS6')
    finally: m.urllib.request.urlopen = old
    assert 'CON_QY1_YR' in seen['url'] and 'CON_VAL_YR' in seen['url']
    assert 'GEN_QY1_YR' not in seen['url']
    assert rows[1][3] == '1'


def test_fetch_census_key_redirect_or_non_json_is_clear_status_and_not_retried(tmp_path, monkeypatch):
    # Regression (Run 055): Census began redirecting keyless requests to missing_key.html; the
    # fetcher retried each one and recorded a bare JSONDecodeError for every row.
    spec = importlib.util.spec_from_file_location('fetch_key', Path('scripts/fetch_goes_trade.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    class Resp:
        def __init__(self, final_url, body): self.final_url, self.body = final_url, body
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def read(self): return self.body
        def geturl(self): return self.final_url
    calls = []
    def fake_urlopen(final_url, body):
        def f(url, timeout=60):
            calls.append(url); return Resp(final_url, body)
        return f
    def no_sleep(_): raise AssertionError('must not retry')
    monkeypatch.setattr(m.time, 'sleep', no_sleep)
    monkeypatch.setenv('CENSUS_API_KEY', 'SECRETKEY123')
    for final in ('https://api.census.gov/data/missing_key.html', 'https://api.census.gov/data/invalid_key.html'):
        calls.clear()
        monkeypatch.setattr(m.urllib.request, 'urlopen', fake_urlopen(final, b'<html>key</html>'))
        try: m._get('imports', 2025, '722511', 'HS6'); assert False
        except m.CensusResponseError as e: assert str(e) == 'census_missing_or_invalid_key'
        assert len(calls) == 1
    calls.clear()
    monkeypatch.setattr(m.urllib.request, 'urlopen', fake_urlopen('https://api.census.gov/x', b'<html>' + b'x' * 300))
    try: m._get('imports', 2025, '722511', 'HS6'); assert False
    except m.CensusResponseError as e: assert str(e) == 'census_non_json_body:<html>' + 'x' * 94
    assert len(calls) == 1
    monkeypatch.setattr(m, 'OUT', tmp_path / 'trade.csv')
    monkeypatch.setattr(m.urllib.request, 'urlopen', fake_urlopen('https://api.census.gov/data/missing_key.html', b'<html/>'))
    assert m.main(['fetch_goes_trade.py','2025','2025']) == 2
    text = (tmp_path/'trade.csv').read_text()
    rows = list(csv.DictReader(text.splitlines()))
    assert {r['status'] for r in rows} == {'census_missing_or_invalid_key'}
    assert 'SECRETKEY123' not in text
