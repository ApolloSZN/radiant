# Owner handoff — what Logan does, in order

Total hands-on time: about 15 minutes on a computer. Steps 1–3 happen once. Step 4 sets up the scheduled runs.

---

## Step 0 — Pause the scheduled GPT task until Step 1 is done

Without a GitHub repo, the scheduled runs can't get data and keep hardening release checks instead (Runs 031–038). Resume it after the push.

## Step 1 — Put Radiant on GitHub (pick A or B)

After the push, GitHub runs everything automatically: `ci` (tests, eval, demo, Docker reproduction, about 5–10 minutes), then `finalize-release`, which records the completed run and checks the full v1.0 bar. **Both green = v1.0 passed (11/11).** Nothing to run locally afterwards.

### A. Easiest: paste this into Claude Code inside the unzipped folder

```
This folder is my Radiant repository. Get it onto GitHub. Explain each step in one line before doing it.

1. Check git and the GitHub CLI (gh) are installed and `gh auth status` is logged in. If not, stop and tell me to run `gh auth login`.
2. pip install -r requirements.txt, then run `pytest -q` and `python -m radiant.eval --strict`. Both must pass. If either fails, stop and show me the error. Don't change scientific results to make it pass.
3. git init -b main (if not already a repo), commit everything as "Radiant v0.14-rc27", then `gh repo create radiant --public --source=. --push` (use radiant-research if the name is taken).
4. Watch the `ci` workflow (`gh run watch`), then the `finalize-release` workflow that starts after it. If either fails, show me the failing step's log and propose the smallest fix. Do not weaken tests or gates. This is the first real hosted run, so a failure is expected information, not a disaster.
5. When both are green, tag the commit v1.0.0 and push the tag.
6. Run `gh workflow run goes-data`, wait for it, `git pull`, then run `python -m radiant.data.goes_import_floor` and explain the recent_imports_comparison section to me in plain English.
7. Give me the repo URL and a 3-line summary.
```

### B. By hand (terminal)

```bash
cd radiant-v0.14-rc27
pip install -r requirements.txt && pytest -q && python -m radiant.eval --strict
git init -b main && git add -A && git commit -m "Radiant v0.14-rc27"
gh auth login                                   # once
gh repo create radiant --public --source=. --push
gh run watch                                    # ci, then finalize-release: both should go green
git tag v1.0.0 && git push --tags
gh workflow run goes-data                       # pulls Census steel trade data
```

If a run fails, copy the failing step's log into Claude. The first real hosted run is the only way to find out.

## Step 2 — Check the data landed

On github.com → your repo → **Actions** → `goes-data` should be green, and `data/goes/goes_trade_annual.csv` should exist. If the Census API rejected a field name, the CSV rows will say `error:` — paste them into Claude or GPT and ask for the fix to `scripts/fetch_goes_trade.py`.

Optional: a free Census API key (api.census.gov/data/key_signup.html) added as a repo secret named `CENSUS_API_KEY` avoids rate limits.

## Step 3 — Pin it

Pin the repo on your GitHub profile. Put the URL on your resume and LinkedIn.

## Step 4 — Scheduled GPT task prompt (resume after Step 1; replace the current prompt)

```
You are running one scheduled research run on Radiant.

INPUT: the latest Radiant repository (GitHub URL: <paste your repo URL>, or the attached zip). Read docs/RUN_PROTOCOL.md first. Section 6 ("Owner priorities") overrides any "next action" in older run logs.

DO, in order:
1. Inspect the current state. Run `pytest -q` and `python -m radiant.eval --strict` if you can execute code.
2. Add at least one NEW sourced fact about the real world to the GOES work (evidence ID, source URL, publication date, scope, evidence class). Priority order is in RUN_PROTOCOL §6.2. If the trade CSV exists, interpret the import trend since 2019 in plain English.
3. Update the calculation only if the new fact changes it. Keep the no-shortage rule unless the evidence identifies one.
4. Update docs/FINDINGS.md (plain English), docs/interview_walkthrough.md, PROGRESS.md and a new logs/run_NNN.md.
5. Before finishing: tests pass and `python -m radiant.eval --strict` exits 0. If new work would break it, withdraw the failing claim (ADR 006). Never add a gate that blocks release on a claim that already failed.

DON'T: work on forecasting; add infrastructure-only changes two runs in a row; rewrite README/FINDINGS for style; use market-research-site numbers as evidence; convert qualitative statements ("25% growth") into quantities.

OUTPUT: (a) the updated repository as a zip, or as a commit/PR if you have GitHub access; (b) at most 8 plain-English lines: what new fact you found, what changed in the finding, what's next. No jargon.
```

## Step 5 — Resume / LinkedIn lines (edit to taste)

- **Resume bullet:** Built Radiant, an evidence-tracked Python system (148 tests, CI-gated) for testing claims about industrial supply chains. Used it to show that U.S. grid expansion raises reliance on foreign transformer-grade electrical steel from ~33% to at least 41–44% of national use, even at full domestic capacity. Corrected my own headline when new evidence showed most imports were hidden inside transformer cores, and withdrew a forecasting result that failed a fair-baseline audit.
- **One-liner:** I build tools that separate what the data proves from what people assume. My latest found that America's grid buildout pushes reliance on foreign transformer steel from a third to over 40%, much of it hidden inside imported parts.
