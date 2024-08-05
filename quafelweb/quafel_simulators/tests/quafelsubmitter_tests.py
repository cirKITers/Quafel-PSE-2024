"""
Tests for the quafel submitter module and the output module
"""

import logging
import unittest
from time import sleep

from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.quafelsubmitter import QuafelSubmissionState, QuafelSubmitter
from quafel_simulators.tests.util import (
    TestClassSimulationRequest,
    TestCase,
    TestClassSimulationRequest2,
)
from quafel_simulators.util.connection import SubmitConnection
from quafel_simulators.util.json_handler import write_json_file


def write_output_file_submission():
    """
    Write the output file for the submission
    """

    write_json_file(
        "output.json",
        {
            "output_location": "~",
            "host": "output.server",
            "port": 22,
            "username": "user",
            "password": "password",
        },
    )


def write_output_file_pull_output():
    """
    Write the output file for the pull output
    """

    write_json_file(
        "output.json",
        {
            "output_location": "~",
            "host": "localhost",
            "port": 2223,
            "username": "user",
            "password": "password",
        },
    )


class TestSubmitter(TestCase):
    """
    Test the submitter module
    """

    # Run This test if other test cases are not running
    @unittest.skip("This test does take a long time to run.")
    def test_forced_initiate(self):
        """
        Test the forced initiation of the hardware
        """

        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        hardware_connection = SubmitConnection(
            TestClassSimulationRequest(), QuafelOutputHardware()
        )

        assert hardware_connection.connect()

        assert hardware_connection.initiate(force=True)

        assert hardware_connection.disconnect()

    @unittest.skip("Just run the simultaneous submissions test")
    def test_submitter_class(self):
        """
        Test the submitter class
        """

        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        write_output_file_submission()
        submitter = QuafelSubmitter()
        assert submitter.submit(TestClassSimulationRequest())

        counter = 600
        for i in range(counter):
            if (
                submitter.get_state(TestClassSimulationRequest())
                == QuafelSubmissionState.READY
            ):
                break
            elif (
                submitter.get_state(TestClassSimulationRequest())
                == QuafelSubmissionState.ERROR
            ):
                assert False

            if i == counter - 1:
                assert False  # The simulation did not finish in time

            print("waiting for simulation to finish")
            sleep(1.0)

        write_output_file_pull_output()
        assert submitter.get_output(TestClassSimulationRequest()) is not None

    def test_simultaneous_submissions(self):
        """
        Test the simultaneous submission of multiple requests on one hardware_profile
        """

        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        write_output_file_submission()
        submitter = QuafelSubmitter()

        request_1 = TestClassSimulationRequest()
        request_2 = TestClassSimulationRequest2()

        submitter.submit(request_1)

        sleep(2.0)

        submitter.submit(request_2)

        counter = 900
        for i in range(counter):
            if (
                submitter.get_state(request_1) == QuafelSubmissionState.READY
                and submitter.get_state(request_2) == QuafelSubmissionState.READY
            ):
                break
            elif (
                submitter.get_state(request_1) == QuafelSubmissionState.ERROR
                or submitter.get_state(request_2) == QuafelSubmissionState.ERROR
            ):
                assert False

            if i == counter - 1:
                assert False  # The simulation did not finish in time

            print("waiting for simulations to finish")
            sleep(1.0)

        write_output_file_pull_output()
        output1 = submitter.get_output(request_1)
        output2 = submitter.get_output(request_2)

        print(output1)
        print(output2)

        assert output1 is not None
        assert output2 is not None
