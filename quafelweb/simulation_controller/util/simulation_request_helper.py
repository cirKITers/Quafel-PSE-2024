from os import remove

from hardware_controller.models import HardwareProfile
from simulation_controller.util.simulation_request import SimulationRequestRange
from simulation_data.models import SimulatorProfile, SimulationRun


def get_missing_runs_as_ranges(
    range: SimulationRequestRange,
    hardware: HardwareProfile,
    simulator: SimulatorProfile,
) -> list[SimulationRequestRange]:
    """
    Get all missing runs as a list of SimulationRequest objects
    """

    # query all existing runs with the given hardware and simulator that could be in the range
    existing_runs = SimulationRun.objects.filter(
        hardware=hardware,
        simulator=simulator,
        qubits__gte=int(range.qubits_min),
        qubits__lte=int(range.qubits_max),
        shots__gte=int(range.shots_min),
        shots__lte=int(range.shots_max),
        depth__gte=int(range.depth_min),
        depth__lte=int(range.depth_max),
    )

    # create a list of ranges to submit for the hardware and simulator
    missing_ranges: list[SimulationRequestRange] = [range.expanded()]

    # The range contains all points that have to exist.
    # Now we check for each existing point if it is in one of the ranges
    # and split the range with the point if necessary.
    for run in existing_runs:
        for r in missing_ranges.copy():
            if r.run_in_range(run):
                missing_ranges.remove(r)
                to_append_list = r.split(run)
                for to_append in to_append_list:
                    missing_ranges.append(to_append)
                break

    ranges_to_return = []
    # Check if the ranges all do not contain any points of the expansion
    for r in missing_ranges.copy():
        if r.qubits_min < range.qubits_min:
            try:
                r = SimulationRequestRange(
                    range.qubits_min,
                    r.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    r.shots_min,
                    r.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    r.depth_min,
                    r.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        if r.qubits_max > range.qubits_max:
            try:
                r = SimulationRequestRange(
                    r.qubits_min,
                    range.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    r.shots_min,
                    r.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    r.depth_min,
                    r.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        if r.shots_min < range.shots_min:
            try:
                r = SimulationRequestRange(
                    r.qubits_min,
                    r.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    range.shots_min,
                    r.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    r.depth_min,
                    r.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        if r.shots_max > range.shots_max:
            try:
                r = SimulationRequestRange(
                    r.qubits_min,
                    r.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    r.shots_min,
                    range.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    r.depth_min,
                    r.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        if r.depth_min < range.depth_min:
            try:
                r = SimulationRequestRange(
                    r.qubits_min,
                    r.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    r.shots_min,
                    r.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    range.depth_min,
                    r.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        if r.depth_max > range.depth_max:
            try:
                r = SimulationRequestRange(
                    r.qubits_min,
                    r.qubits_max,
                    range.qubits_increment,
                    range.qubits_increment_type,
                    r.shots_min,
                    r.shots_max,
                    range.shots_increment,
                    range.shots_increment_type,
                    r.depth_min,
                    range.depth_max,
                    range.depth_increment,
                    range.depth_increment_type,
                )
            except ValueError:
                continue

        ranges_to_return.append(r)

    return ranges_to_return
