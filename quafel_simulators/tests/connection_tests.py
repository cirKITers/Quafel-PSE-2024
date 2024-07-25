"""
Unit tests for the connection module
"""

import logging
import unittest

from quafel_simulators.base.hardware import QuafelHardwareBase
from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.tests.util import TestCase, TestClassSimulationRequest
from quafel_simulators.util.connection import SubmitConnection, Connection


class TestConnections(TestCase):
    """
    Test the connection module
    """

    def test_connecting_and_disconnecting_without_totp(self):
        """
        Test the connection and disconnection to the hardware without a totp
        """

        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)

        hardware_connection = SubmitConnection(TestClassSimulationRequest(), QuafelOutputHardware())

        assert hardware_connection.connect()

        assert hardware_connection.disconnect()

    @unittest.skip("Test needs credentials and KIT network")
    def test_connecting_and_disconnecting_with_totp(self):
        """
        Test the connection and disconnection to the hardware with a totp
        This test tries to connect to the bwUniCluster2.0
        If you do not have credentials, you can skip this test
        """

        logging.basicConfig()
        logging.getLogger("connection.connect").setLevel(logging.DEBUG)
        logging.getLogger("connection.disconnect").setLevel(logging.DEBUG)

        # Read the credentials from the command line
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        totp = input("Enter your totp: ")

        hardware = TestClassHardwareBWUniCluster(username, password, totp)

        connection = Connection(hardware)

        assert connection.connect()


class TestClassHardwareBWUniCluster(QuafelHardwareBase):
    """
    Test class for the bwUniCluster2.0
    """

    def __init__(self, username: str, password: str, totp: str):
        self.username = username
        self.password = password
        self.totp = totp

    def get_id(self) -> str:
        pass

    def get_host(self) -> str:
        return "bwunicluster.scc.kit.edu"

    def get_port(self) -> int:
        return 22

    def get_username(self) -> str:
        return self.username

    def get_password(self) -> str:
        return self.password

    def get_totp(self) -> str | None:
        return self.totp

    def get_setup_script(self) -> str:
        pass

    def get_run_script(self) -> str:
        pass
