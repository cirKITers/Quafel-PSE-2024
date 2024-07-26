"""
Here are util classes that are used in the tests.
The tests need some interfaces implemented to test the simulators.
Also, the docker needs to be running for the tests to pass, because hardware.profiles and the output server are 
required for the tests to pass.
"""

import os
import unittest
from pathlib import Path

from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.base.simulator import QuafelSimulatorBase


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
        with open(
            "../script/test_script_setup.bash", "r", encoding="utf-8"
        ) as test_script_setup_file:
            return test_script_setup_file.read()

    def get_run_script(self) -> str:
        # read the run script from the file
        with open(
            "../script/test_script_run.bash", "r", encoding="utf-8"
        ) as test_script_run_file:
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
    """
    Test simulation request 2
    """

    def get_max_qubits(self) -> int:
        return 2


class TestCase(unittest.TestCase):
    """
    Base class for the tests
    This class changes the sandbox directory to the test directory
    """

    @classmethod
    def setUpClass(cls):
        # The test_dir is one directory above the current sandbox directory
        cls.test_dir = Path.joinpath(Path(__file__).parent, "sandbox")
        # Change the current sandbox directory to the test_dir
        os.chdir(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        # Change back to the original sandbox directory
        os.chdir(Path(__file__).parent)
