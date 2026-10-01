"""Adaptive-System Kernel.

One representation for a protocell, a lab, a firm and an industrial region:

  B  boundary        what counts as inside
  X  state           named variables with viability bounds (V)
  R  resources       the food set: what the environment supplies
  O  observation     which state variables the system senses
  M  memory          (carried by the evidence series below)
  P  controller      maps observations to actions
  A  action          which state variables its actions move
  V  viability       bounds on X that define persistence
  U  update          whether errors change future behavior

A kernel alone is just a data structure; every thermostat satisfies it.
What makes this usable is that each property below is an operational test
on evidence, returning a verdict plus the numbers that produced it.

  persistent      returns inside viability bounds after perturbation
  regulated       actions measurably oppose observed deviations (negative feedback)
  self_producing  catalytic closure: a non-empty RAF over its own processes
  learning        error falls with repetition
  self_improving  capability raises its own rate of improvement (beta > 0, R6)

  autonomous = persistent and regulated and self_producing
  (closure of production plus closure of regulation; in the spirit of the
  Moreno and Mossio account of biological autonomy)
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from radiant.engines.raf import Process, max_raf


def _slope_t(x, y) -> tuple[float, float]:
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return float("nan"), float("nan")
    xm = x.mean()
    sxx = ((x - xm) ** 2).sum()
    b = ((x - xm) * (y - y.mean())).sum() / sxx
    resid = y - (y.mean() + b * (x - xm))
    se = np.sqrt((resid ** 2).sum() / (len(x) - 2) / sxx)
    if se > 0:
        return float(b), float(b / se)
    return float(b), (float("-inf") if b < 0 else float("inf") if b > 0 else float("nan"))


@dataclass
class AdaptiveSystem:
    id: str
    name: str
    scale: str                                   # 'chemical', 'cell', 'lab', 'firm', 'region', ...
    boundary: str
    viability: dict[str, tuple[float, float]]    # X with V bounds
    food: set[str] = field(default_factory=set)  # R
    processes: list[Process] = field(default_factory=list)
    observes: set[str] = field(default_factory=set)   # O
    acts_on: set[str] = field(default_factory=set)    # A
    parent: str | None = None

    # ---------------------------------------------------------------- tests
    def persistent(self, trials: list[dict], min_trials: int = 3, min_rate: float = 0.8) -> dict:
        """trials: [{'var': name, 'recovered': bool}] after perturbation outside bounds."""
        n = len(trials)
        rate = sum(t["recovered"] for t in trials) / n if n else 0.0
        return {"pass": n >= min_trials and rate >= min_rate, "trials": n, "recovery_rate": rate}

    def regulated(self, deviation, response, t_crit: float = -2.0) -> dict:
        """deviation: observed x - setpoint; response: next-step change in x from action."""
        linked = bool(self.observes & self.acts_on)
        b, t = _slope_t(deviation, response)
        return {"pass": linked and b < 0 and t < t_crit, "sense_act_link": linked,
                "feedback_slope": b, "t_stat": t}

    def self_producing(self) -> dict:
        res = max_raf(self.food, self.processes)
        cov = len(res.core) / len(self.processes) if self.processes else 0.0
        return {"pass": res.self_sustaining, "core": sorted(res.core), "coverage": cov,
                "pruned": res.removal_log}

    def learning(self, errors, t_crit: float = -2.0) -> dict:
        """errors on repeated attempts at the same task, in order."""
        b, t = _slope_t(np.arange(len(errors)), errors)
        return {"pass": b < 0 and t < t_crit, "error_slope": b, "t_stat": t}

    def self_improving(self, capability, dt: float = 1.0, z: float = 2.0) -> dict:
        """R6: regress log growth rate on log capability; slope = 1 + beta."""
        a = np.asarray(capability, float)
        growth = np.diff(a) / dt
        mask = growth > 0
        if mask.sum() < 3:
            return {"pass": False, "beta": float("nan"), "reason": "too few positive-growth steps"}
        x, y = np.log(a[:-1][mask]), np.log(growth[mask])
        b, t = _slope_t(x, y)
        beta = b - 1.0
        se = abs(b / t) if np.isfinite(t) and t != 0 else 0.0
        return {"pass": beta - z * se > 0, "beta": beta, "beta_se": se}

    def profile(self, evidence: dict) -> dict:
        """Run every test the evidence supports; untested properties are reported as None."""
        out = {
            "persistent": self.persistent(evidence["perturbations"]) if "perturbations" in evidence else None,
            "regulated": self.regulated(*evidence["feedback"]) if "feedback" in evidence else None,
            "self_producing": self.self_producing() if self.processes else None,
            "learning": self.learning(evidence["errors"]) if "errors" in evidence else None,
            "self_improving": self.self_improving(evidence["capability"]) if "capability" in evidence else None,
        }
        passed = {k: (v["pass"] if v else None) for k, v in out.items()}
        passed["autonomous"] = bool(passed["persistent"] and passed["regulated"] and passed["self_producing"])
        return {"system": self.id, "scale": self.scale, "verdicts": passed, "details": out}
