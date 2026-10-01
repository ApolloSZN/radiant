"""Evidence-backed macro arithmetic for the U.S. LPT case.

Unlike stage capacities, these quantities are directly reported/derived from reported
2019 unit counts. They constrain what claims are possible but do not identify which
factory stage is binding.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LPT2019Macro:
    domestic_output: float = 137.0
    imports: float = 617.0
    exports: float = 4.0
    reported_capacity_utilization: float = .40

    @property
    def apparent_consumption(self): return self.domestic_output + self.imports - self.exports
    @property
    def import_share(self): return self.imports / self.apparent_consumption
    @property
    def implied_nameplate_capacity(self): return self.domestic_output / self.reported_capacity_utilization
    @property
    def unused_nameplate_capacity(self): return self.implied_nameplate_capacity - self.domestic_output


def domestic_capacity_counterfactual(m: LPT2019Macro=LPT2019Macro()):
    """Accounting bound only: assumes reported nameplate capacity could be fully utilized.
    It does NOT claim feasibility, because labor/material/design/test constraints may
    explain the utilization gap.
    """
    cap=m.implied_nameplate_capacity
    return {
      'apparent_consumption':m.apparent_consumption,
      'observed_import_share':m.import_share,
      'implied_nameplate_capacity':cap,
      'unused_nameplate_capacity':m.unused_nameplate_capacity,
      'max_import_displacement_if_full_utilization':min(m.imports,m.unused_nameplate_capacity),
      'residual_imports_if_full_utilization':max(0,m.imports-m.unused_nameplate_capacity),
    }
