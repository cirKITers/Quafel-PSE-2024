"""
In this module functions are defined to pull and handle the output of the simulation.
"""

from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.quafelsubmitter import QuafelSubmitter, QuafelSubmissionState
from simulation_controller.util.simulation_request import SimulationRequest
from simulation_controller.util.simulation_request_helper import fill_runs_from_csv


def handle_output(request: SimulationRequest) -> None:
    """
    Handle the output of the simulation
    (pull and write to database)
    """
    
    # Pull the output
    submitter = QuafelSubmitter()
    state = submitter.get_state(request)
    print(state)

    if state == QuafelSubmissionState.ERROR:
        return  # Error handling

    assert state == QuafelSubmissionState.READY

    output = submitter.get_output(request)
    print(output)
    if output is None:
        return  # Error handling


    # Write the output to the database
    fill_runs_from_csv(request, output)