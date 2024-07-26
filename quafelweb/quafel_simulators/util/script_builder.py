"""
Util for building scripts
"""

from pathlib import Path

import yaml

from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.output import QuafelOutputHardware


def build_quafel_yml_configuration(simulation_request: QuafelSimulationRequest) -> str:
    """
    Creates the yml configuration file from the simulation request
    """

    data_generation = {
        "data_generation": {
            "seed": 1113,
            "samples_per_parameter": 20,
            "haar_samples_per_qubit": 60,
            "min_qubits": simulation_request.get_min_qubits(),
            "max_qubits": simulation_request.get_max_qubits(),
            "qubits_increment": simulation_request.get_qubits_increment(),
            "qubits_type": str(simulation_request.get_qubits_increment_type()),
            "min_depth": simulation_request.get_min_depth(),
            "max_depth": simulation_request.get_max_depth(),
            "depth_increment": simulation_request.get_depth_increment(),
            "depth_type": str(simulation_request.get_depth_increment_type()),
            "min_shots": simulation_request.get_min_shots(),
            "max_shots": simulation_request.get_max_shots(),
            "shots_increment": simulation_request.get_shots_increment(),
            "shots_type": str(simulation_request.get_shots_increment_type()),
            "skip_combinations": [],
            "frameworks": [simulation_request.get_simulator().get_name()],
        },
    }

    return yaml.dump(data_generation)


def build_quafel_script_setup(simulation_request: QuafelSimulationRequest) -> str:
    """
    Build the quafel script
    """
    return simulation_request.get_hardware().get_setup_script()


def build_quafel_script_submit(
        simulation_request: QuafelSimulationRequest, output_hardware: QuafelOutputHardware) -> str:
    """
    Build the quafel script
    """

    script = simulation_request.get_hardware().get_run_script()

    configuration = build_quafel_yml_configuration(simulation_request)
    simulation_id = simulation_request.get_id()

    script = script.replace("CONFIGURATION=\"\"", "CONFIGURATION=\'" + configuration + "\'")
    script = script.replace("OUTPUT_LOCATION=\"\"", "OUTPUT_LOCATION=\'" + output_hardware.get_output_location() + "\'")
    script = script.replace("SIMULATION_ID=\"\"", "SIMULATION_ID=\'" + simulation_id + "\'")

    return script


def build_quafel_script_pull_output(output_hardware: QuafelOutputHardware, submit_id: str) -> str:
    """
    Build the quafel script
    """

    script = output_hardware.get_run_script()

    if script == "":
        # Read the default script from the directory
        path = f"{Path(__file__).parent}/pull_output.bash"

        with open(path, mode="r", encoding="utf-8") as file:
            script = file.read()

    script = script.replace("REMOTE_HOST=\"\"", "REMOTE_HOST=\'" + output_hardware.get_host() + "\'")
    script = script.replace("REMOTE_PORT=\"\"", "REMOTE_PORT=" + str(output_hardware.get_port()))
    script = script.replace("REMOTE_USERNAME=\"\"", "REMOTE_USERNAME=\'" + output_hardware.get_username() + "\'")
    script = script.replace("REMOTE_PASSWORD=\"\"", "REMOTE_PASSWORD=\'" + output_hardware.get_password() + "\'")
    script = script.replace("OUTPUT_LOCATION=\"\"", "OUTPUT_LOCATION=\'" + output_hardware.get_output_location() + "\'")
    script = script.replace("SIMULATION_ID=\"\"", "SIMULATION_ID=\'" + submit_id + "\'")

    return script
