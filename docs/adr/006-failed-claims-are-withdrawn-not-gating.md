# ADR 006 — Failed claims are withdrawn, not release blockers

**Status:** accepted in Run 028. Amends ADR 005.

## Context

ADR 005 correctly stopped CI from certifying the sequencing headline against a weak baseline. It did this by making "robustly beat every simple baseline" a release requirement. That coupled the ability to ship *anything* to winning a forecasting contest the evidence says Radiant does not win, and forecasting is not the project's stated aim. The result was a permanently red CI and an unshippable repository, while the actual failure was already fully disclosed.

## Decision

Every eval row carries a `claim_status`:

- `claimed`: an asserted result. It must pass its gate or release fails.
- `integrity`: an asserted property of the machinery (for example, no-leak vintage replay). It must pass.
- `withdrawn`: a result that failed its gate. It is published as a negative result and never asserted in README, FINDINGS or interviews.

`release_decision()` blocks release if any claimed or integrity row fails. `--strict` CI mode uses that decision.

## What does not change

- The fair-baseline panel, its numbers, and `passed: false` for sequencing remain in every eval report.
- A withdrawn result can only be re-claimed by passing the same predeclared fair gate. Flipping a failing row to `claimed` blocks release (tested).
- Comparing against a weaker opponent still cannot make anything pass.

## Consequence

Honesty is enforced by what is asserted, not by what is attempted. The repository can ship with its failures on display.
