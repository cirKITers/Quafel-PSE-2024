"""
Here the simulation request is defined to request a simulation from specific a hardware profile and data.
"""
from quafel_simulators.hardware_base import HardwareBase
from quafel_simulators.simulation_base import QuafelSimulationBase


class QuafelSimulationRequest:
    """
    The simulation request class
    """

    def __init__(self, hardware: HardwareBase, software: QuafelSimulationBase):
        """
        Initialize the simulation request
        """
        self.hardware = hardware
        self.software = software

        self.min_qubits = 0
        self.max_qubits = 0
        self.qubits_increment = 0

        self.min_depth = 0
        self.max_depth = 0
        self.depth_increment = 0

        self.min_shots = 0
        self.max_shots = 0
        self.shots_increment = 0

        self.totp = ""
