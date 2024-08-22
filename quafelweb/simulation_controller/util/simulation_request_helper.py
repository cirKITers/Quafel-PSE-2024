import csv
import io

from django.db import models

from hardware_controller.models import HardwareProfile
from simulation_controller.util.simulation_request import SimulationRequestRange, SimulationRequest, exp_range
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


def write_unfinished_runs_in_database(
        simulation_request: SimulationRequest,
):
    """
    Write the runs in the database without any results and with the status "unfinished"
    """

    for q in exp_range(
            simulation_request.get_min_qubits(),
            simulation_request.get_max_qubits(),
            simulation_request.get_qubits_increment(),
            simulation_request.get_qubits_increment_type(),
    ):
        for s in exp_range(
                simulation_request.get_min_shots(),
                simulation_request.get_max_shots(),
                simulation_request.get_shots_increment(),
                simulation_request.get_shots_increment_type(),
        ):
            for d in exp_range(
                    simulation_request.get_min_depth(),
                    simulation_request.get_max_depth(),
                    simulation_request.get_depth_increment(),
                    simulation_request.get_depth_increment_type(),
            ):
                # Check if the run exists:
                runs = SimulationRun.objects.filter(
                    hardware=simulation_request.hardware,
                    simulator=simulation_request.simulator,
                    qubits=q,
                    depth=d,
                    shots=s,
                )
                if len(runs) > 0:
                    continue  # Run already exists (overwrite it in the future but let it be for now)

                SimulationRun.objects.create(
                    id=SimulationRun.objects.count() + 1,
                    hardware=simulation_request.hardware,
                    simulator=simulation_request.simulator,
                    qubits=q,
                    depth=d,
                    shots=s,
                    durations=[],
                    finished=False,
                )
                
                print("Run created")

def fill_runs_from_csv(
        simulation_request: SimulationRequest,
        csv_string: str,
):
    """
    Fill the runs from a csv file
    """

    csv_file = io.StringIO(csv_string)
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

    for i in range(0, len(data)):
        qubits = data[i]["qubits"]
        depth = data[i]["depth"]
        shots = data[i]["shots"]
        expressibility = data[i]["expressibility"]
        entangling_capability = data[i]["entangling_capability"]

        length = (len(data[i]) - 6) / 2
        durations = []
        for j in range(int(length)):
            durations.append(
                data[i][f"duration_proc_{j}"]
            )

        duration_average = 0
        for duration in durations:
            duration_average += float(duration)
        duration_average /= len(durations)

        # Get the run from the database
        run = SimulationRun.objects.filter(
            hardware=simulation_request.hardware,
            simulator=simulation_request.simulator,
            qubits=qubits,
            depth=depth,
            shots=shots,
        )

        if len(run) != 1:
            print("Error: Run not found")
            continue
        run = run[0]

        # Update the run with the durations
        run.durations = durations
        run.duration_avg = duration_average
        run.finished = True

        # Save the run in the database
        run.save(force_update=True)
