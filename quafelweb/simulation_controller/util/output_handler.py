"""
In this module functions are defined to pull and handle the output of the simulation.
"""

from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.quafelsubmitter import QuafelSubmitter, QuafelSubmissionState


def handle_output(request: QuafelSimulationRequest) -> None:
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
    print("write points") 
