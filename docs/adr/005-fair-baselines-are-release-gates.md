# ADR 005 — Fair baselines are release gates, not footnotes

**Status:** accepted in Run 027.

## Context

Radiant's sequencing selector originally passed the evaluation gate by reducing MALE 77.5% relative to an all-history log-linear trend. Run 026 added a predeclared panel of stronger simple baselines and found that rolling-4 and rolling-3 trends beat the selector. The repository disclosed that result, but the executable release harness still marked the sequencing evaluation as passing because it continued to gate on the weak all-history comparator.

That created a contradiction: the documentation said the headline did not survive, while CI would still certify the old headline gate.

## Decision

The sequencing ship gate now uses the complete predeclared simple-baseline panel. A system passes only if it robustly beats every baseline in that panel. The strongest observed panel baseline is reported explicitly. The historical 77.5% result remains in diagnostics for provenance but cannot satisfy the release gate.

`python -m radiant.eval --strict` returns non-zero when the scientific gate fails, and GitHub Actions invokes strict mode. Plain `python -m radiant.eval` remains report-only so a pre-release checkout can still regenerate every diagnostic and demo in one command without hiding the failed gate.

## Consequences

- Radiant rc15 is farther from v1.0 numerically: the eval gate is now red in addition to the two unavailable hosted-CI gates.
- That is intentional. A release candidate should not become "green" by comparing against an opponent already shown to be weak.
- Future headline improvements must survive the strongest predeclared simple comparators or the gate stays red.
- Negative results and failed formulations remain first-class artifacts rather than being removed after a stronger baseline appears.
