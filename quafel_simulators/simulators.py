"""
Here are the simulators defined that are pulled from a configuration file.
"""


import json
from pathlib import Path
from threading import Lock

from quafel_simulators.base.simulator import QuafelSimulatorBase


class QuafelSimulator(QuafelSimulatorBase):
    """
    Quafel simulator read from the configuration file
    """

    name: str
    version: str

    def __init__(self, name: str, version: str):
        """
        Initialize the simulator
        :param name: The name of the simulator
        :param version: The version of the simulator
        """
        self.name = name
        self.version = version

    def get_name(self) -> str:
        """
        Get the name of the simulator
        """
        return self.name

    def get_version(self) -> str:
        """
        Get the version of the simulator
        """
        return self.version


class QuafelSimulators:
    """
    The simulators that are inside the simulators.json file
    """
    configuration_file_path: str = "simulators.json"  # path to the configuration file

    _last_change = None  # last time the configuration file was changed
    _simulators: list[QuafelSimulatorBase] = []  # list of simulators known to the system

    def _configuration_changed(self) -> bool:
        # Check if the file exists
        if (not Path(self.configuration_file_path).exists()) or (not Path(self.configuration_file_path).is_file()):
            with open(self.configuration_file_path, "w", encoding="utf-8") as file:
                file.write("[]")
                return True

        last_change = Path(self.configuration_file_path).stat().st_mtime
        if last_change != self._last_change:
            self._last_change = last_change
            return True

        return False

    def _update_simulators(self):
        """
        Update the simulators known to the system
        """

        # Read the simulators from the configuration file
        json_simulators = None
        with open(self.configuration_file_path, "r", encoding="utf-8") as file:
            try:
                json_simulators = json.load(file)
            except json.JSONDecodeError:
                return
        sims: list[QuafelSimulatorBase] = []
        for simulator in json_simulators:
            if ("name" not in simulator) or ("version" not in simulator):
                continue
            sims.append(QuafelSimulator(simulator["name"], simulator["version"]))

        # Write the simulators to the list
        self._simulators = sims

    def get_simulators(self) -> list[QuafelSimulatorBase]:
        """
        Get the simulators known to the system
        """
        
        # Update the simulators if the configuration file has changed
        if self._configuration_changed():
            self._update_simulators()
        
        return self._simulators


# The simulators singleton
simulators = QuafelSimulators()
