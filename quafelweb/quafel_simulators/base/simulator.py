"""
Base class for a simulator object.
This class also is the registry of all simulators known to the system.
The simulators known to the system are stored in a json-like dictionary.
"""
from abc import abstractmethod


class QuafelSimulatorBase:
    """
    The base class for the simulation
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the simulator
        """

    @abstractmethod
    def get_version(self) -> str:
        """
        Get the version of the simulator
        """
