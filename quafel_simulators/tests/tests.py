"""
Here are tests defined to test the quafel_simulators module.
"""
import logging
import unittest
from logging import warning

import yaml

from quafel_simulators.base.hardware import HardwareBase
from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.base.simulator import QuafelSimulatorBase
from quafel_simulators.submitter import HardwareConnection
from quafel_simulators.util.script_builder import build_quafel_script_submit


class TestHardware(HardwareBase):

    def get_host(self) -> str:
        return "localhost"

    def get_port(self) -> int:
        return 2222

    def get_username(self) -> str:
        return "user"

    def get_password(self) -> str:
        return "password"

    def needs_totp(self) -> bool:
        return False

    def get_setup_script(self) -> str:
        # read the setup script from the file
        with open("test_script_setup.bash", "r") as test_script_setup_file:
            return test_script_setup_file.read()

    def get_run_script(self) -> str:
        # read the run script from the file
        with open("test_script_run.bash", "r") as test_script_run_file:
            return test_script_run_file.read()


class TestSimulator(QuafelSimulatorBase):
    def get_name(self) -> str:
        return "cirq_fw"

    def get_version(self) -> str:
        return "test"


class TestSimulationRequest(QuafelSimulationRequest):

    def get_totp(self) -> None | str:
        return None

    def get_hardware(self) -> HardwareBase:
        return TestHardware()

    def get_min_qubits(self) -> int:
        return 1

    def get_max_qubits(self) -> int:
        return 1

    def get_qubits_increment(self) -> int:
        return 1

    def get_min_depth(self) -> int:
        return 1

    def get_max_depth(self) -> int:
        return 1

    def get_depth_increment(self) -> int:
        return 1

    def get_min_shots(self) -> int:
        return 1

    def get_max_shots(self) -> int:
        return 1

    def get_shots_increment(self) -> int:
        return 1

    def get_simulator(self) -> QuafelSimulatorBase:
        return TestSimulator()


class TestSimulators(unittest.TestCase):
    """
    Test the simulators module
    """

    def test_create_configuration_file(self):
        """
        Test the creation of the configuration file
        """

        # Delete the simulators.json file
        from pathlib import Path
        Path("simulators.json").unlink(missing_ok=True)

        # Check if the file exists
        assert not Path("simulators.json").exists()

        from quafel_simulators.simulators import simulators
        simulators.update_simulators()

        # Check if the file exists
        assert Path("simulators.json").exists()

    def test_read_configuration_file(self):
        """
        Test the reading of the configuration file
        """

        # write the file content
        with open("simulators.json", "w") as file:
            file.write('[{"name": "sim1", "version": "1.0"}, {"name": "sim2", "version": "2.0"}]')

        from quafel_simulators.simulators import simulators
        simulators.update_simulators()

        # Check if the simulators are read
        assert len(simulators.get_simulators()) == 2
        assert simulators.get_simulators()[0].get_name() == "sim1"
        assert simulators.get_simulators()[0].get_version() == "1.0"
        assert simulators.get_simulators()[1].get_name() == "sim2"
        assert simulators.get_simulators()[1].get_version() == "2.0"


class TestScriptBuilder(unittest.TestCase):
    """
    Test the script builder module
    """

    def test_build_quafel_yml_configuration(self):
        """
        Test the building of the yml configuration
        """

        simulation_request = TestSimulationRequest()
        from quafel_simulators.util.script_builder import build_quafel_yml_configuration
        generated_yml = build_quafel_yml_configuration(simulation_request)

        # Read yml from path:
        with open("quafel_test_yml.yml", "r") as yml_file:
            read_yml = yml_file.read()

        assert str(yaml.compose(generated_yml)) == str(yaml.compose(read_yml))

    def test_build_quafel_script_submit(self):
        """
        Test the building of the quafel script
        """

        build_script = build_quafel_script_submit(TestSimulationRequest())
        print(build_script)

    def test_build_quafel_script_setup(self):
        """
        Test the building of the quafel script
        """

        from quafel_simulators.util.script_builder import build_quafel_script_setup
        build_script = build_quafel_script_setup(TestSimulationRequest())
        print(build_script)

        assert str.find(build_script, "\'") == -1


class TestSubmitter(unittest.TestCase):
    """
    Test the submitter module
    """

    def test_disconnecting_without_totp(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)

        hardware_connection = HardwareConnection(TestSimulationRequest())

        success = hardware_connection.connect()
        assert success

        success = hardware_connection.disconnect()
        assert success

    def test_set_setup_script(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        hardware_connection = HardwareConnection(TestSimulationRequest())

        success = hardware_connection.connect()
        assert success

        success = hardware_connection._set_setup_script()
        assert success

        success = hardware_connection._setup_script_is_set()
        assert success

        success = hardware_connection.disconnect()
        assert success

    def test_forced_initiate(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        hardware_connection = HardwareConnection(TestSimulationRequest())

        success = hardware_connection.connect()
        assert success

        # This test takes a long time to run
        warning("forced initiate test skipped")
        # success = hardware_connection.initiate(force=True)
        assert success

        success = hardware_connection.disconnect()
        assert success

    def test_submit(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)
        hardware_connection = HardwareConnection(TestSimulationRequest())

        success = hardware_connection.connect()
        assert success

        success = hardware_connection.submit()
        assert success

        success = hardware_connection.disconnect()
        assert success


if __name__ == '__main__':
    unittest.main()
