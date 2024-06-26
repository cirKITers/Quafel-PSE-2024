from abc import ABC
from simulation_data.simulation import SimulationGroup, HardwareProfile


class Simulator(ABC):

  def simulate(self, ip : str, port : int , simulators : list[str], qbits : set[int]):
    ...

  def collect(self) -> dict:
    ...
