from hardware_controller.models import HardwareProfile
from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.base.simulation_request import IncrementType
from quafel_simulators.base.simulator import QuafelSimulatorBase
from quafel_simulators.quafelsubmitter import QuafelSimulationRequest
from simulation_controller.util.scripted_hardware_connection import HardwareWithScript
from simulation_data.models import SimulationRun, SimulatorProfile


def _exp_range(
    min: int, max: int, increment: int, increment_type: IncrementType
) -> list[int]:
    """
    Compute the range of values.
    """
    if increment_type == IncrementType.LINEAR:
        return list(range(min, max + 1, increment))
    else:
        return [2**i for i in range(min, max + 1, increment)]


class SimulationRequestRange:
    """
    Range of values for a simulation request.
    """

    def __init__(
        self,
        qubits_min: int,
        qubits_max: int,
        qubits_increment: int,
        qubits_increment_type: IncrementType,
        shots_min: int,
        shots_max: int,
        shots_increment: int,
        shots_increment_type: IncrementType,
        depth_min: int,
        depth_max: int,
        depth_increment: int,
        depth_increment_type: IncrementType,
    ):
        """
        Initialize the range.

        :raises ValueError: If the range is invalid.
        """

        self.qubits_min = qubits_min
        self.qubits_max = qubits_max
        self.qubits_increment = qubits_increment
        self.qubits_increment_type: IncrementType = qubits_increment_type

        self.shots_min = shots_min
        self.shots_max = shots_max
        self.shots_increment = shots_increment
        self.shots_increment_type = shots_increment_type

        self.depth_min = depth_min
        self.depth_max = depth_max
        self.depth_increment = depth_increment
        self.depth_increment_type = depth_increment_type

        self._check()

    def _check(self):
        """
        Check if the range is valid.
        """

        if self.qubits_min < 0:
            raise ValueError("Qubits min must be greater than 0.")

        if self.qubits_max < self.qubits_min:
            raise ValueError("Qubits max must be greater than qubits min.")

        if self.qubits_increment < 1:
            raise ValueError("Qubits increment must be greater than 0.")

        if self.shots_min < 0:
            raise ValueError("Shots min must be greater than 0.")

        if self.shots_max < self.shots_min:
            raise ValueError("Shots max must be greater than shots min.")

        if self.shots_increment < 1:
            raise ValueError("Shots increment must be greater than 0.")

        if self.depth_min < 0:
            raise ValueError("Depth min must be greater than 0.")

        if self.depth_max < self.depth_min:
            raise ValueError("Depth max must be greater than depth min.")

        if self.depth_increment < 1:
            raise ValueError("Depth increment must be greater than 0.")

    def expanded(self):
        """
        Return a new range with the values expanded by one on the edges.
        """
        return SimulationRequestRange(
            self.qubits_min - self.qubits_increment,
            self.qubits_max + self.qubits_increment,
            self.qubits_increment,
            self.qubits_increment_type,
            self.shots_min - self.shots_increment,
            self.shots_max + self.shots_increment,
            self.shots_increment,
            self.shots_increment_type,
            self.depth_min - self.depth_increment,
            self.depth_max + self.depth_increment,
            self.depth_increment,
            self.depth_increment_type,
        )

    def split(self, run: SimulationRun):
        """
        Split the range in two ranges.
        "Above" and "under" the simulation-runs values.
        """

        try:
            # Check if it is on the edge
            split1 = SimulationRequestRange(
                self.qubits_min,
                run.qubits - 1,
                self.qubits_increment,
                self.qubits_increment_type,
                self.shots_min,
                run.shots,
                self.shots_increment,
                self.shots_increment_type,
                self.depth_min,
                run.depth,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split1 = None

        try:
            # Check if it is on the edge
            split2 = SimulationRequestRange(
                self.qubits_min,
                run.qubits,
                self.qubits_increment,
                self.qubits_increment_type,
                self.shots_min,
                run.shots - 1,
                self.shots_increment,
                self.shots_increment_type,
                self.depth_min,
                run.depth,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split2 = None

        try:
            # Check if it is on the edge
            split3 = SimulationRequestRange(
                self.qubits_min,
                run.qubits,
                self.qubits_increment,
                self.qubits_increment_type,
                self.shots_min,
                run.shots,
                self.shots_increment,
                self.shots_increment_type,
                self.depth_min,
                run.depth - 1,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split3 = None

        try:
            split4 = SimulationRequestRange(
                run.qubits + 1,
                self.qubits_max,
                self.qubits_increment,
                self.qubits_increment_type,
                run.shots,
                self.shots_max,
                self.shots_increment,
                self.shots_increment_type,
                run.depth,
                self.depth_max,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split4 = None

        try:
            split5 = SimulationRequestRange(
                run.qubits,
                self.qubits_max,
                self.qubits_increment,
                self.qubits_increment_type,
                run.shots + 1,
                self.shots_max,
                self.shots_increment,
                self.shots_increment_type,
                run.depth,
                self.depth_max,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split5 = None

        try:
            split6 = SimulationRequestRange(
                run.qubits,
                self.qubits_max,
                self.qubits_increment,
                self.qubits_increment_type,
                run.shots,
                self.shots_max,
                self.shots_increment,
                self.shots_increment_type,
                run.depth + 1,
                self.depth_max,
                self.depth_increment,
                self.depth_increment_type,
            )
        except ValueError:
            split6 = None

        split_to_return = []

        if split1 is not None:
            split_to_return.append(split1)
        if split2 is not None:
            split_to_return.append(split2)
        if split3 is not None:
            split_to_return.append(split3)
        if split4 is not None:
            split_to_return.append(split4)
        if split5 is not None:
            split_to_return.append(split5)
        if split6 is not None:
            split_to_return.append(split6)

        return split_to_return

    def run_in_range(self, run: SimulationRun):
        """
        Returns true if the run is in the range.
        """

        for q in _exp_range(
            self.qubits_min,
            self.qubits_max,
            self.qubits_increment,
            self.qubits_increment_type,
        ):
            for s in _exp_range(
                self.shots_min,
                self.shots_max,
                self.shots_increment,
                self.shots_increment_type,
            ):
                for d in _exp_range(
                    self.depth_min,
                    self.depth_max,
                    self.depth_increment,
                    self.depth_increment_type,
                ):
                    if run.qubits == q and run.shots == s and run.depth == d:
                        return True
        return False


class SimulationRequest(QuafelSimulationRequest):
    """
    Simulation Request to send to the hardware.
    """

    def __init__(
        self,
        simulation_range: SimulationRequestRange,
        hardware: HardwareProfile,
        simulator: SimulatorProfile,
        username: str,
        password: str,
        top: str,
    ):
        self.simulation_range = simulation_range
        self.hardware = hardware
        self.simulator = simulator
        self.username = username
        self.password = password
        self.totp = top

    def get_hardware(self) -> QuafelHardwareBase:
        return HardwareWithScript(
            self.hardware, self.username, self.password, self.totp
        )

    def get_simulator(self) -> QuafelSimulatorBase:
        return self.simulator

    def get_min_qubits(self) -> int:
        return self.simulation_range.qubits_min

    def get_max_qubits(self) -> int:
        return self.simulation_range.qubits_max

    def get_qubits_increment(self) -> int:
        return self.simulation_range.qubits_increment

    def get_qubits_increment_type(self) -> IncrementType:
        return self.simulation_range.qubits_increment_type

    def get_min_depth(self) -> int:
        return self.simulation_range.depth_min

    def get_max_depth(self) -> int:
        return self.simulation_range.depth_max

    def get_depth_increment(self) -> int:
        return self.simulation_range.depth_increment

    def get_depth_increment_type(self) -> IncrementType:
        return self.simulation_range.depth_increment_type

    def get_min_shots(self) -> int:
        return self.simulation_range.shots_min

    def get_max_shots(self) -> int:
        return self.simulation_range.shots_max

    def get_shots_increment(self) -> int:
        return self.simulation_range.shots_increment

    def get_shots_increment_type(self) -> IncrementType:
        return self.simulation_range.shots_increment_type
