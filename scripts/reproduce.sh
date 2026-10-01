#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
pytest -q > artifacts/reproduce_pytest.txt
cat artifacts/reproduce_pytest.txt
python - <<'PYTESTREPORT'
import json
from pathlib import Path
from radiant.source_fingerprint import fingerprint
d=fingerprint('.')
Path('artifacts/test_report.json').write_text(json.dumps({'schema':'radiant.tests.v2','returncode':0,'source_fingerprint':d,'stdout':Path('artifacts/reproduce_pytest.txt').read_text(),'stderr':''},indent=2)+'\n')
PYTESTREPORT
python -m radiant.eval --strict
python -m examples.demo > artifacts/demo_output.txt
python - <<'PY'
import json
from pathlib import Path
from radiant.source_fingerprint import fingerprint
p=Path('artifacts/demo_output.txt')
text=p.read_text()
required=['Toy protocell','Toy research lab','Toy industrial region','Criticality ranking','Counterfactual: cut grid power','Counterfactual: halve electrolyzer cost']
missing=[x for x in required if x not in text]
report={'schema':'radiant.demo.v2','passed':not missing,'source_fingerprint':fingerprint('.'),'required_sections':required,'missing_sections':missing,'output':'artifacts/demo_output.txt'}
Path('artifacts/demo_report.json').write_text(json.dumps(report,indent=2)+'\n')
if missing:
    raise SystemExit('demo output missing required sections: '+', '.join(missing))
PY
python - <<'PY'
import json
from pathlib import Path
from radiant.source_fingerprint import fingerprint
Path('artifacts/reproduction_report.json').write_text(json.dumps({
  'schema':'radiant.reproduction.v2',
  'source_fingerprint':fingerprint('.'),
  'passed':True,
  'commands':['pytest -q','python -m radiant.eval --strict','python -m examples.demo'],
  'demo_report':'artifacts/demo_report.json',
  'eval_report':'artifacts/eval_report.json'
},indent=2)+'\n')
PY
