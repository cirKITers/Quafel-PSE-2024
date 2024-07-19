"""
Here are tests defined to test the quafel_simulators module.
"""
import logging
import unittest
from time import sleep

import yaml

from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.base.simulator import QuafelSimulatorBase
from quafel_simulators.quafelsubmitter import SubmitConnection, QuafelOutputHardware, OutputConnection, QuafelSubmitter, \
    QuafelSubmissionState
from quafel_simulators.util.json_handler import read_dict, write_json_file
from quafel_simulators.util.script_builder import build_quafel_script_submit


class TestClassHardware(QuafelHardwareBase):
    """
    Test hardware (docker)
    """

    def get_totp(self) -> str | None:
        return None

    def get_id(self) -> str:
        return "testid"

    def get_host(self) -> str:
        return "localhost"

    def get_port(self) -> int:
        return 2222

    def get_username(self) -> str:
        return "user"

    def get_password(self) -> str:
        return "password"

    def get_setup_script(self) -> str:
        # read the setup script from the file
        with open("test_script_setup.bash", "r") as test_script_setup_file:
            return test_script_setup_file.read()

    def get_run_script(self) -> str:
        # read the run script from the file
        with open("test_script_run.bash", "r") as test_script_run_file:
            return test_script_run_file.read()


class TestClassSimulator(QuafelSimulatorBase):
    """
    Test simulator
    """

    def get_name(self) -> str:
        return "cirq_fw"

    def get_version(self) -> str:
        return "test"


class TestClassSimulationRequest(QuafelSimulationRequest):
    """
    Test simulation request
    """
    def get_totp(self) -> None | str:
        return None

    def get_hardware(self) -> QuafelHardwareBase:
        return TestClassHardware()

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
        return TestClassSimulator()


class TestClassSimulationRequest2(TestClassSimulationRequest):
    def get_max_qubits(self) -> int:
        return 2


class TestJsonHandler(unittest.TestCase):
    """
    Test the json_handler module
    """

    def test_read_dict_without_file(self):
        # assure the file is not existent
        from pathlib import Path
        Path("test.json").unlink(missing_ok=True)

        # read the dict
        from quafel_simulators.util.json_handler import read_dict
        read = read_dict("test.json")

        # check if the dict is empty
        assert read == {}

    def test_write_and_read_dict(self):
        # write the dict
        from quafel_simulators.util.json_handler import write_json_file, _read_json_file
        write_json_file("test.json", {"test": "test"})

        # read the dict
        read = _read_json_file("test.json")

        # check if the dict is correct
        assert read == {"test": "test"}

    def test_write_and_read_list(self):
        # write the list
        from quafel_simulators.util.json_handler import write_json_file, _read_json_file
        write_json_file("test.json", ["test", "test"])

        # read the list
        read = _read_json_file("test.json")

        # check if the list is correct
        assert read == ["test", "test"]


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

        simulation_request = TestClassSimulationRequest()
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

        build_script = build_quafel_script_submit(TestClassSimulationRequest(), QuafelOutputHardware())
        print(build_script)

    def test_build_quafel_script_setup(self):
        """
        Test the building of the quafel script
        """

        from quafel_simulators.util.script_builder import build_quafel_script_setup
        build_script = build_quafel_script_setup(TestClassSimulationRequest())
        print(build_script)

        assert str.find(build_script, "\'") == -1

    def test_build_quafel_script_pull_output(self):
        """
        Test the building of the pull output script
        """

        from quafel_simulators.util.script_builder import build_quafel_script_pull_output
        build_script = build_quafel_script_pull_output(QuafelOutputHardware(), "test")
        print(build_script)


class TestSubmitter(unittest.TestCase):
    """
    Test the submitter module
    """

    def test_create_output_hardware_configuration_file(self):
        """
        Test if the output_hardware.json file is created
        """

        # Delete the output_hardware.json file
        from pathlib import Path
        Path("output.json").unlink(missing_ok=True)

        # Check if the file exists
        assert not Path("output.json").exists()

        from quafel_simulators.quafelsubmitter import QuafelOutputHardware
        output_hardware = QuafelOutputHardware()
        assert not output_hardware.update()

        # Check if the file exists
        assert Path("output.json").exists()

        read = read_dict("output.json")
        assert read == {"output_location": "", "host": "", "port": 22, "username": "", "password": ""}

    def test_read_output_hardware_configuration_file(self):
        """
        Test if the output_hardware.json file is read
        """

        # write the file content
        write_json_file("output.json", {
            "output_location": "test",
            "host": "localhost",
            "port": 2223,
            "username": "user",
            "password": "password"
        })

        from quafel_simulators.quafelsubmitter import QuafelOutputHardware
        output_hardware = QuafelOutputHardware()
        assert output_hardware.update()

        assert output_hardware.get_output_location() == "test"
        assert output_hardware.get_host() == "localhost"
        assert output_hardware.get_port() == 2223
        assert output_hardware.get_username() == "user"
        assert output_hardware.get_password() == "password"

    def test_connecting_and_disconnecting_without_totp(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)

        hardware_connection = SubmitConnection(TestClassSimulationRequest(), QuafelOutputHardware())

        assert hardware_connection.connect()
        
        assert hardware_connection.disconnect()

    def test_set_setup_script(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        hardware_connection = SubmitConnection(TestClassSimulationRequest(), QuafelOutputHardware())

        assert hardware_connection.connect()

        assert hardware_connection._set_setup_script()

        assert hardware_connection._setup_script_is_set()

        assert hardware_connection.disconnect()

    @unittest.skip("This test does take a long time to run.")
    def test_forced_initiate(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        hardware_connection = SubmitConnection(TestClassSimulationRequest(), QuafelOutputHardware())

        assert hardware_connection.connect()

        assert hardware_connection.initiate(force=True)

        assert hardware_connection.disconnect()

    def test_submit_and_get_output_process(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        # write output file for the docker container
        write_json_file("output.json", {
            "output_location": "~",
            "host": "server_side",
            "port": 22,
            "username": "user",
            "password": "password"
        })

        submit_connection = SubmitConnection(TestClassSimulationRequest(), QuafelOutputHardware())

        assert submit_connection.connect()

        assert submit_connection.initiate()

        assert submit_connection.submit()

        assert submit_connection.disconnect()

        # write output file for localhost to connect to container
        write_json_file("output.json", {
            "output_location": "~",
            "host": "localhost",
            "port": 2223,
            "username": "user",
            "password": "password"
        })
        output_hardware = QuafelOutputHardware()
        output_hardware.update()
        output_connection = OutputConnection(output_hardware, TestClassSimulationRequest().get_id())
        assert output_connection._move_remote_output()
        
        assert output_connection._get_local_output() is not None

    def test_submitter_class(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        submitter = QuafelSubmitter()
        assert submitter.submit(TestClassSimulationRequest())

        counter = 120
        for i in range(counter):
            if submitter.get_state(TestClassSimulationRequest()) == QuafelSubmissionState.READY:
                break
            if i == counter - 1:
                assert False # The simulation did not finish in time

            print("waiting for simulation to finish")
            sleep(1.0)
        
        assert submitter.get_output(TestClassSimulationRequest()) is not None

    def test_simultaneous_submissions(self):
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        submitter = QuafelSubmitter()
        
        request_1 = TestClassSimulationRequest()
        request_2 = TestClassSimulationRequest2()

        submitter.submit(request_1)

        sleep(2.0)

        submitter.submit(request_2)

        counter = 200
        for i in range(counter):
            if (submitter.get_state(request_1) == QuafelSubmissionState.READY and 
                    submitter.get_state(request_2) == QuafelSubmissionState.READY):
                break
            if i == counter - 1:
                assert False # The simulation did not finish in time

            print("waiting for simulations to finish")
            sleep(1.0)
        
        assert submitter.get_output(request_1) is not None
        assert submitter.get_output(request_2) is not None
     
if __name__ == '__main__':
    unittest.main()
