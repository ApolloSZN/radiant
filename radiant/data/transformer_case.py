"""Large-power-transformer constraint case.

IMPORTANT: the topology is evidence-backed; normalized coefficients/capacities below are
SCENARIO PARAMETERS, not measured U.S. quantities. They exist to test the constraint
engine while preventing qualitative DOE claims from being converted into fake numbers.
"""
from radiant.engines.viability import FlowProcess
from radiant.engines.constraint_resolution import ProductionSystem

def lpt_scenario() -> ProductionSystem:
    ps=(
      FlowProcess('core_fabrication',{'goes':1.0},{'core':1.0},capacity=1.0),
      FlowProcess('winding',{'ctc_copper':1.0},{'winding':1.0},capacity=.82),
      FlowProcess('insulation_prep',{'insulation':1.0},{'insulated_parts':1.0},capacity=1.15),
      FlowProcess('assembly',{'core':1.0,'winding':1.0,'insulated_parts':1.0},{'assembled_lpt':1.0},capacity=.78),
      FlowProcess('test_and_qualification',{'assembled_lpt':1.0},{'qualified_lpt':1.0},capacity=.72),
    )
    return ProductionSystem(ps,{'goes':1.3,'ctc_copper':1.2,'insulation':1.2},'qualified_lpt',evidence={
      'import:goes':('DOE2024_GOES','DOE2024_IMPORT'),
      'capacity:core_fabrication':('DOE2024_EQUIP','DOE2022_INPUTS'),
      'capacity:winding':('DOE2024_EQUIP','DOE2022_INPUTS'),
      'capacity:assembly':('DOE2024_EQUIP',),
      'capacity:test_and_qualification':('DOE2014_CUSTOM',),
    })
