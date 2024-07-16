"""
Here are the simulators defined that are pulled from a configuration file.
"""


import json
from pathlib import Path
from threading import Lock, Thread
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
    _simulators: list[QuafelSimulatorBase] = []  # list of simulators known to the system
    _simulators_lock = Lock()  # lock for the simulators list

    def update_simulators(self):
        """
        Update the simulators known to the system
        """

        # Check if the file exists
        if (not Path(self.configuration_file_path).exists()) or (not Path(self.configuration_file_path).is_file()):
            with open(self.configuration_file_path, "w") as file:
                file.write("[]")
                return

        # Read the simulators from the configuration file
        json_simulators = None
        with open(self.configuration_file_path, "r") as file:
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
        with self._simulators_lock:
            self._simulators = sims

    def get_simulators(self) -> list[QuafelSimulatorBase]:
        """
        Get the simulators known to the system
        """
        with self._simulators_lock:
            return self._simulators.copy()


# TODO: delete this class and just return the simulators by reading the configuration file
class QuafelSimulatorsUpdater:
    """
    The runner class
    """
    thread: Thread = None  # thread for the updater
    running: bool = False  # whether the updater is running
    running_lock = Lock()  # lock for the running variable

    def start_updater(self):
        """
        Start the updater
        """
        with self.running_lock:
            if self.running:
                return

            self.running = True

        # Start the update loop
        self.thread = Thread(target=self.update_loop)
        self.thread.start()

    def stop_updater(self):
        """
        Stop the updater
        """
        with self.running_lock:
            if (not self.running) or (self.thread is None):
                return

            self.running = False

    def update_loop(self):
        """
        The update loop
        """
        while True:
            with self.running_lock:
                if not self.running:
                    break

            simulators.update_simulators()
            # TODO: implement the update loop.


# The simulators singleton
simulators = QuafelSimulators()
