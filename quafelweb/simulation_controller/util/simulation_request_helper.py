from hardware_controller.models import HardwareProfile
from simulation_controller.util.simulation_request import SimulationRequestRange
from simulation_data.models import SimulatorProfile, SimulationRun


def get_missing_runs_as_ranges(
        range: SimulationRequestRange, 
        hardware: HardwareProfile, 
        simulator: SimulatorProfile)-> list[SimulationRequestRange]:
    """
    Get all missing runs as a list of SimulationRequest objects
    """

    # query all existing runs with the given hardware and simulator that could be in the range
    existing_runs = SimulationRun.objects.filter(
        hardware=hardware, simulator=simulator, 
        qubits__gte=range.qubits_min, 
        qubits__lte=range.qubits_max, 
        shots__gte=range.shots_min, 
        shots__lte=range.shots_max, 
        depth__gte=range.depth_min, 
        depth__lte=range.depth_max)

    # create a list of ranges to submit for the hardware and simulator
    missing_ranges: list[SimulationRequestRange] = [range]

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

    return missing_ranges
