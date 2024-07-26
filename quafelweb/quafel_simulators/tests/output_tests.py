"""
Tests for the output module.
"""

from pathlib import Path

from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.tests.util import TestCase
from quafel_simulators.util.json_handler import read_dict, write_json_file


class TestOutput(TestCase):
    """
    Test the output module
    """

    def test_create_output_hardware_configuration_file(self):
        """
        Test if the output_hardware.json file is created
        """

        # Delete the output_hardware.json file
        Path("output.json").unlink(missing_ok=True)

        # Check if the file exists
        assert not Path("output.json").exists()

        output_hardware = QuafelOutputHardware()
        assert not output_hardware.update()

        # Check if the file exists
        assert Path("output.json").exists()

        read = read_dict("output.json")
        assert read == {
            "output_location": "",
            "host": "",
            "port": 22,
            "username": "",
            "password": "",
        }

    def test_read_output_hardware_configuration_file(self):
        """
        Test if the output_hardware.json file is read
        """

        # write the file content
        write_json_file(
            "output.json",
            {
                "output_location": "test",
                "host": "localhost",
                "port": 2223,
                "username": "user",
                "password": "password",
            },
        )

        output_hardware = QuafelOutputHardware()
        assert output_hardware.update()

        assert output_hardware.get_output_location() == "test"
        assert output_hardware.get_host() == "localhost"
        assert output_hardware.get_port() == 2223
        assert output_hardware.get_username() == "user"
        assert output_hardware.get_password() == "password"
