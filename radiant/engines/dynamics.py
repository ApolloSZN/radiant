"""Curve (R1), composition (R2) and loop (R3) engines.

All costs are handled in natural-log space. A positive rate r means cost falls.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------- curves (R1)

@dataclass(frozen=True)
class CurveFit:
    form: str            # 'moore' (x = time) or 'wright' (x = log cumulative production)
    intercept: float     # log cost at x = 0
    rate: float          # progress rate r (moore) or Wright exponent w; positive = improving
    rate_se: float       # standard error of the rate
    resid_sd: float
    n: int
    x_mean: float
    sxx: float

    def predict(self, x: float) -> tuple[float, float]:
        """Mean log cost and predictive sd at x (standard OLS prediction interval)."""
        mean = self.intercept - self.rate * x
        sd = self.resid_sd * np.sqrt(1 + 1 / self.n + (x - self.x_mean) ** 2 / self.sxx)
        return float(mean), float(sd)


def _ols(x: np.ndarray, y: np.ndarray, form: str) -> CurveFit:
    if len(x) < 3:
        raise ValueError("need at least 3 observations to fit a curve with an error estimate")
    xm = x.mean()
    sxx = float(((x - xm) ** 2).sum())
    slope = float(((x - xm) * (y - y.mean())).sum() / sxx)
    intercept = float(y.mean() - slope * xm)
    resid = y - (intercept + slope * x)
    s = float(np.sqrt((resid ** 2).sum() / (len(x) - 2)))
    return CurveFit(form, intercept, -slope, s / np.sqrt(sxx), s, len(x), float(xm), sxx)


def fit_moore(years, log_cost) -> CurveFit:
    return _ols(np.asarray(years, float), np.asarray(log_cost, float), "moore")


def fit_wright(log_cum_production, log_cost) -> CurveFit:
    return _ols(np.asarray(log_cum_production, float), np.asarray(log_cost, float), "wright")


def sahal_rate(wright_exponent: float, production_growth: float) -> float:
    """R1: exponential production growth g turns Wright exponent w into time rate r = w * g."""
    return wright_exponent * production_growth


# ----------------------------------------------------------- composition (R2)

def composite_cost(c0, rates, t: float, law: str = "additive") -> float:
    """Composite cost at time t. 'additive': costs sum. 'multiplicative': factors multiply."""
    c0, rates = np.asarray(c0, float), np.asarray(rates, float)
    parts = c0 * np.exp(-rates * t)
    return float(parts.sum() if law == "additive" else parts.prod())


def shares(c0, rates, t: float) -> np.ndarray:
    parts = np.asarray(c0, float) * np.exp(-np.asarray(rates, float) * t)
    return parts / parts.sum()


def composite_rate(c0, rates, t: float, law: str = "additive") -> float:
    """r_C = -d ln C / dt.  Additive: share-weighted mean. Multiplicative: sum of rates."""
    rates = np.asarray(rates, float)
    if law == "multiplicative":
        return float(rates.sum())
    return float((shares(c0, rates, t) * rates).sum())


def composite_rate_drift(c0, rates, t: float) -> float:
    """R2 identity: d r_C / dt = -Var_s(r)  (additive law)."""
    s = shares(c0, rates, t)
    r = np.asarray(rates, float)
    mean = (s * r).sum()
    return float(-(s * (r - mean) ** 2).sum())


def bottleneck_leverage(c0, rates, t: float) -> np.ndarray:
    """Score s_i * (r_C - r_i). Positive = a growing share of cost; the breakthrough target."""
    s = shares(c0, rates, t)
    r = np.asarray(rates, float)
    return s * ((s * r).sum() - r)


# ------------------------------------------------------------------ loops (R3)

@dataclass(frozen=True)
class LoopState:
    """Read / write / model / verify leg times in seconds, plus human-free share of each."""
    read: float
    write: float
    model: float
    verify: float
    automated: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

    def legs(self) -> dict[str, float]:
        return {"read": self.read, "write": self.write, "model": self.model, "verify": self.verify}

    def cycle_time(self) -> float:
        return sum(self.legs().values())

    def closure_index(self) -> float:
        v = list(self.legs().values())
        return min(v) / max(v)

    def bottleneck(self) -> str:
        return max(self.legs(), key=self.legs().get)

    def automation_fraction(self) -> float:
        times = list(self.legs().values())
        return sum(t * a for t, a in zip(times, self.automated)) / self.cycle_time()

    def amdahl(self, leg: str, speedup: float) -> float:
        f = self.legs()[leg] / self.cycle_time()
        return 1.0 / ((1 - f) + f / speedup)

    def amdahl_ceiling(self, leg: str) -> float:
        f = self.legs()[leg] / self.cycle_time()
        return float("inf") if f >= 1 else 1.0 / (1 - f)
