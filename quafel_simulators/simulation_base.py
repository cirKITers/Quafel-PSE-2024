"""
Base class for a simulator object.
This class also is the registry of all simulators known to the system.
The simulators known to the system are stored in a json-like dictionary.
"""
from threading import Lock


class QuafelSimulationBase:
    """
    The base class for the simulation
    """

    def get_name(self) -> str:
        """
        Get the name of the simulator
        """

    def get_version(self) -> str:
        """
        Get the version of the simulator
        """


simulators: list[QuafelSimulationBase] = []
simulators_lock = Lock()


def update_simulators():
    """
    Update the simulators known to the system
    """

    # TODO: Read the simulators from a configuration file

    # TODO: Write the simulators to the list
    with simulators_lock:
        pass


def get_simulators() -> list[QuafelSimulationBase]:
    """
    Get the simulators known to the system
    """
    with simulators_lock:
        return simulators.copy()
