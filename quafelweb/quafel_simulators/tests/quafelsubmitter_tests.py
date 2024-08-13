"""
Tests for the quafel submitter module and the output module
"""

import logging
import unittest
from time import sleep

from django.db.transaction import Atomic

from quafel_simulators.base.simulation_request import QuafelSimulationRequest
from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.quafelsubmitter import QuafelSubmissionState, QuafelSubmitter
from quafel_simulators.tests.util import (
    TestClassSimulationRequest,
    TestCase,
    TestClassSimulationRequest2, TestClassSimulationRequest3,
)
from quafel_simulators.util.connection import SubmitConnection, OutputConnection
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

    # Run This tests if other tests cases are not running
    @unittest.skip("This tests does take a long time to run.")
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

    @unittest.skip("Just run the simultaneous submissions tests")
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
            if (
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
            if (
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

    def test_submission_with_handler(self):
        """
        Test the submission with a handler
        """
        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)
        logging.getLogger("connection.initiate").setLevel(logging.DEBUG)
        logging.getLogger("connection.setup_script").setLevel(logging.DEBUG)
        logging.getLogger("connection.run").setLevel(logging.DEBUG)

        submitter = QuafelSubmitter()

        def handle(r: QuafelSimulationRequest):
            sleep(2.0)  # Wait for the tests to read the state of the request
            write_output_file_pull_output()
            assert submitter.get_state(r) == QuafelSubmissionState.READY
            assert submitter.quafel_output_hardware.update()
            
            connection = OutputConnection(submitter.quafel_output_hardware, request.get_id())
            o = connection.get_output()

            if o is None:
                submitter.quafel_output_hardware = None  # To make assertion in tests thread

            assert o is not None

        write_output_file_submission()
        
        request = TestClassSimulationRequest3()
        submitter.submit(request, handle)
        
        # Wait for the simulation to finish
        counter = 600
        for i in range(counter):
            if submitter.get_state(request) == QuafelSubmissionState.READY:
                break
            if submitter.get_state(request) == QuafelSubmissionState.ERROR:
                assert False

            if i == counter - 1:
                assert False

            sleep(1.0)

        sleep(4.0) # Wait for the handler to finish
        assert submitter.quafel_output_hardware is not None
