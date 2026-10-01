# ADR 004: Hosted CI requires two-phase evidence

## Decision
Radiant separates **execution inside hosted CI** from **successful completion of hosted CI**.

`radiant.ci_attest` is generated during GitHub Actions and proves that the release checks executed in the hosted environment for a specific commit/run. It cannot prove that the workflow later completed successfully. A second record, `artifacts/completed_ci_run.json`, must be captured from GitHub only after the run reports `status=completed` and `conclusion=success` and must bind the same commit SHA.

## Why
A running workflow cannot non-circularly certify its own future success. Treating an in-job environment record as a green-CI attestation would make the v1.0 ship gate semantically false.

## Consequences
Local reproduction remains necessary but insufficient. The in-workflow release verifier is expected to remain one gate short until an external completed-run record exists. Final v1.0 shipment is an external verification step against GitHub's completed run state.
