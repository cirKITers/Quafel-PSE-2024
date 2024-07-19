"""
Here the simulation request is defined to request a simulation from specific a hardware profile and data.
"""


from abc import abstractmethod
from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.base.simulator import QuafelSimulatorBase


class QuafelSimulationRequest:
    """
    The simulation request class
    """

    @abstractmethod
    def get_hardware(self) -> QuafelHardwareBase:
        """
        Get the hardware profile of the simulation request
        """

    @abstractmethod
    def get_simulator(self) -> QuafelSimulatorBase:
        """
        Get the simulator of the simulation request
        """

    @abstractmethod
    def get_min_qubits(self) -> int:
        """
        Get the minimum number of qubits
        """

    @abstractmethod
    def get_max_qubits(self) -> int:
        """
        Get the maximum number of qubits
        """

    @abstractmethod
    def get_qubits_increment(self) -> int:
        """
        Get the increment of qubits
        """

    @abstractmethod
    def get_min_depth(self) -> int:
        """
        Get the minimum depth
        """

    @abstractmethod
    def get_max_depth(self) -> int:
        """
        Get the maximum depth
        """

    @abstractmethod
    def get_depth_increment(self) -> int:
        """
        Get the increment of depth
        """

    @abstractmethod
    def get_min_shots(self) -> int:
        """
        Get the minimum number of shots
        """

    @abstractmethod
    def get_max_shots(self) -> int:
        """
        Get the maximum number of shots
        """

    @abstractmethod
    def get_shots_increment(self) -> int:
        """
        Get the increment of shots
        """

    def get_id(self) -> str:
        """
        Get a unique identifier for the simulation request
        """
        return (f"{self.get_hardware().get_id()}_"
                f"{self.get_simulator().get_name()}_"
                f"{self.get_simulator().get_version()}_"
                f"{self.get_min_qubits()}_"
                f"{self.get_max_qubits()}_"
                f"{self.get_qubits_increment()}_"
                f"{self.get_min_depth()}_"
                f"{self.get_max_depth()}_"
                f"{self.get_depth_increment()}_"
                f"{self.get_min_shots()}_"
                f"{self.get_max_shots()}_"
                f"{self.get_shots_increment()}")
