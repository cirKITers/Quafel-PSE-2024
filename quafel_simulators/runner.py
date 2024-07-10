"""
The runner is responsible for running the simulation on the hardware
and update the available simulators and output data.
"""

from threading import Thread, Lock

from quafel_simulators.simulation_request import QuafelSimulationRequest


class Runner:
    """
    The runner class
    """
    running: bool = False
    running_lock = Lock()

    def __init__(self):
        """
        Initialize the runner
        """
        self.thread = None

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

            # TODO: implement the update loop.

    def submit(self, simulation_request: QuafelSimulationRequest):
        """
        Submit a simulation request
        """
        # TODO: define SimulationRequest
