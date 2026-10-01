"""Fail-closed v1.0 release verifier.

A release is allowed only when every ship-bar artifact exists and the scientific
headline contains at least one strict historical-vintage evaluation. Retrospective
real-data wins are useful evidence but cannot satisfy that gate.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import json, re, subprocess, sys
from radiant.hosted_release import load as load_completed_ci
from radiant.source_fingerprint import fingerprint

@dataclass(frozen=True)
class Gate:
    name: str
    passed: bool
    evidence: str


def _word_count(path: Path) -> int:
    text=path.read_text() if path.exists() else ''
    return len(re.findall(r"\b[\w'-]+\b", text))


def _hosted_ci(root: Path, expected_sha: str | None = None) -> tuple[bool,str]:
    p=root/'artifacts/hosted_ci_attestation.json'
    if not p.exists(): return False, 'missing artifacts/hosted_ci_attestation.json'
    try: d=json.loads(p.read_text())
    except Exception as exc: return False, f'invalid hosted CI attestation: {exc}'
    ok=(d.get('schema')=='radiant.hosted_ci.v1' and d.get('provider')=='github_actions'
        and bool(re.fullmatch(r'[0-9a-f]{40}',str(d.get('commit_sha',''))))
        and str(d.get('run_id','')).isdigit() and str(d.get('run_url','')).startswith('https://github.com/'))
    if expected_sha is not None:
        ok = ok and str(d.get('commit_sha','')).lower() == expected_sha.lower()
    return ok, (d.get('run_url','invalid attestation') if ok else 'invalid hosted CI attestation')

def _candidate_sha(root: Path) -> str | None:
    # Bind hosted evidence to the exact checked-out candidate. A copied ZIP has no
    # trustworthy commit identity and therefore cannot satisfy hosted release gates.
    try:
        cp=subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True,check=True)
        sha=cp.stdout.strip().lower()
        return sha if re.fullmatch(r'[0-9a-f]{40}', sha) else None
    except Exception:
        return None

def verify(root: str|Path='.', run_commands: bool=False, ci_mode: bool=False, candidate_sha: str|None=None) -> dict:
    root=Path(root)
    eval_path=root/'artifacts/eval_report.json'
    eval_data=json.loads(eval_path.read_text()) if eval_path.exists() else {}
    results=eval_data.get('results',[])
    strict=[r for r in results if r.get('evidence_class')=='strict_historical_vintage' and r.get('passed')]
    measured=[r for r in results if r.get('claim_status')=='claimed' and r.get('passed') and float(r.get('relative_improvement',0)) > 0]
    writeup=root/'docs/technical_writeup.md'
    wc=_word_count(writeup)
    candidate_sha=(candidate_sha or _candidate_sha(root))
    hosted_ok, hosted_evidence=_hosted_ci(root, candidate_sha)
    completed_ok, completed_evidence=load_completed_ci(root/'artifacts/completed_ci_run.json', candidate_sha)
    # Both records must describe the same hosted run, not merely two independently
    # well-shaped successful records.
    if hosted_ok and completed_ok:
        try:
            h=json.loads((root/'artifacts/hosted_ci_attestation.json').read_text())
            c=json.loads((root/'artifacts/completed_ci_run.json').read_text())
            same=(h.get('repository')==c.get('repository') and str(h.get('commit_sha','')).lower()==str(c.get('commit_sha','')).lower()
                  and str(h.get('run_id'))==str(c.get('run_id')) and h.get('run_url')==c.get('run_url'))
            if not same:
                completed_ok=False; completed_evidence='completed run does not match hosted attestation'
        except Exception:
            completed_ok=False; completed_evidence='unable to cross-check hosted CI records'
    current_fp=fingerprint(root)
    def _json_pass(path: Path, schema: str) -> bool:
        try:
            d=json.loads(path.read_text())
            return d.get('schema')==schema and d.get('passed') is True and d.get('source_fingerprint')==current_fp
        except Exception:
            return False
    reproduction_ok=_json_pass(root/'artifacts/reproduction_report.json','radiant.reproduction.v2')
    container_reproduction_ok=_json_pass(root/'artifacts/container_reproduction_report.json','radiant.container_reproduction.v1')
    demo_ok=_json_pass(root/'artifacts/demo_report.json','radiant.demo.v2')
    try:
        test_data=json.loads((root/'artifacts/test_report.json').read_text())
        test_ok=(test_data.get('schema')=='radiant.tests.v2' and test_data.get('returncode') == 0 and test_data.get('source_fingerprint')==current_fp)
    except Exception:
        test_ok=False
    gates=[
      Gate('eval_harness_ci', bool(eval_data.get('release', {}).get('release_ok', eval_data.get('all_passed'))) and bool(measured) and (root/'.github/workflows/ci.yml').exists(), f'artifacts/eval_report.json + CI workflow; passing measured claimed rows={len(measured)}'),
      Gate('one_command_reproduction', (root/'scripts/reproduce_container.sh').exists() and (root/'Dockerfile').exists() and reproduction_ok and container_reproduction_ok, 'scripts/reproduce_container.sh + Dockerfile + passing source-bound host/clean-container reproduction receipts'),
      Gate('readme_10_minute', (root/'README.md').exists() and _word_count(root/'README.md')>=500, 'README.md'),
      Gate('adrs', len(list((root/'docs/adr').glob('*.md')))>=3, 'docs/adr/*.md'),
      Gate('limitations_negative_results', (root/'docs/limitations.md').exists(), 'docs/limitations.md'),
      Gate('working_demo', (root/'examples/demo.py').exists() and demo_ok, 'examples/demo.py + passing source-bound artifacts/demo_report.json'),
      Gate('technical_writeup_1500_2500', 1500<=wc<=2500, f'docs/technical_writeup.md words={wc}'),
      Gate('tests_ci_green', test_ok, 'source-bound artifacts/test_report.json returncode=0'),
      Gate('hosted_ci_execution', hosted_ok, hosted_evidence),
      Gate('hosted_ci_completed_green', completed_ok, completed_evidence),
      Gate('strict_no_leak_headline_evidence', bool(strict), f'strict passing eval rows={len(strict)}'),
    ]
    if run_commands:
        cp=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=root,capture_output=True,text=True)
        (root/'artifacts').mkdir(exist_ok=True)
        # Preserve the same typed, source-bound receipt contract used by
        # scripts/reproduce.sh.  A previous implementation overwrote the v2
        # receipt with an untyped JSON object here; hosted CI could pass in
        # --ci mode but the downloaded artifact could never satisfy the final
        # verifier.  --run must strengthen evidence, never destroy it.
        (root/'artifacts/test_report.json').write_text(json.dumps({
            'schema':'radiant.tests.v2',
            'returncode':cp.returncode,
            'source_fingerprint':fingerprint(root),
            'stdout':cp.stdout,
            'stderr':cp.stderr,
        },indent=2)+'\n')
        # update gate after command
        gates=[Gate(g.name, cp.returncode==0 if g.name=='tests_ci_green' else g.passed,
                    cp.stdout.strip() if g.name=='tests_ci_green' else g.evidence) for g in gates]
    required=[g for g in gates if not (ci_mode and g.name=='hosted_ci_completed_green')]
    report={'schema':'radiant.release.v1','release':'v1.0','mode':'ci' if ci_mode else 'final','passed':all(g.passed for g in required),'gates':[asdict(g) for g in gates]}
    return report

if __name__=='__main__':
    report=verify('.', '--run' in sys.argv, '--ci' in sys.argv)
    Path('artifacts').mkdir(exist_ok=True)
    Path('artifacts/release_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['passed'] else 2)
