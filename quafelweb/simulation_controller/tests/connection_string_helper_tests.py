"""
Test the disassembling of a connection string
"""

import unittest

from quafelweb.simulation_controller.util.connection_string_helper import disassemble_connection_string


class TestConnectionStringHelper(unittest.TestCase):
    """
    Test the connection string helper
    """

    def test_disassemble_connection_string(self):
        """
        Test the disassembling of a connection string
        """

        # Test a valid connection string
        connection_string = "http://localhost:8080"
        type_, host, port = disassemble_connection_string(connection_string)

        self.assertEqual(type_, "http")
        self.assertEqual(host, "localhost")
        self.assertEqual(port, 8080)

        # Test a connection string with an invalid port
        connection_string = "http://localhost:65536"
        with self.assertRaises(ValueError):
            disassemble_connection_string(connection_string)

        # Test an invalid connection string
        connection_string = "http://localhost"
        with self.assertRaises(ValueError):
            disassemble_connection_string(connection_string)

        # Test an invalid connection string with a wrong port
        connection_string = "http://localhost:900000"
        with self.assertRaises(ValueError):
            disassemble_connection_string(connection_string)
