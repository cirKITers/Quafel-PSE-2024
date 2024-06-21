from abc import ABC
from simulation_data.simulation import SimulationGroup


class Simulator(ABC):

  def simulate(self, group : SimulationGroup):
    ...

  def collect(self) -> dict:
    ...