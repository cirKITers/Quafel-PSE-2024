"""
Util for building scripts
"""

import yaml

from quafel_simulators.base.simulation_request import QuafelSimulationRequest


def build_quafel_yml_configuration(simulation_request: QuafelSimulationRequest) -> str:
    """
    Creates the yml configuration file from the simulation request
    """

    data_generation = {
        "data_generation": {
            "seed": 1113,
            "samples_per_parameter": 1,
            "haar_samples_per_qubit": 1,
            "min_qubits": simulation_request.get_min_qubits(),
            "max_qubits": simulation_request.get_max_qubits(),
            "qubits_increment": simulation_request.get_qubits_increment(),
            "qubits_type": "linear",
            "min_depth": simulation_request.get_min_depth(),
            "max_depth": simulation_request.get_max_depth(),
            "depth_increment": simulation_request.get_depth_increment(),
            "depth_type": "linear",
            "min_shots": simulation_request.get_min_shots(),
            "max_shots": simulation_request.get_max_shots(),
            "shots_increment": simulation_request.get_shots_increment(),
            "shots_type": "linear",
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


def build_quafel_script_submit(simulation_request: QuafelSimulationRequest) -> str:
    """
    Build the quafel script
    """

    script = simulation_request.get_hardware().get_run_script()

    configuration = build_quafel_yml_configuration(simulation_request)
    output_location = simulation_request.get_id()

    script = script.replace("CONFIGURATION=\"\"", "CONFIGURATION=\'" + configuration + "\'")
    script = script.replace("OUTPUT_LOCATION=\"\"", "OUTPUT_LOCATION=\'" + output_location + "\'")

    return script
