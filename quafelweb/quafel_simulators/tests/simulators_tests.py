"""
Tests for the simulators module
"""

from pathlib import Path

from quafel_simulators.simulators import QuafelSimulators
from quafel_simulators.tests.util import TestCase


class TestSimulators(TestCase):
    """
    Test the simulators module
    """

    def test_create_configuration_file(self):
        """
        Test the creation of the configuration file
        """

        # Delete the simulators.json file
        Path("simulators.json").unlink(missing_ok=True)

        # Check if the file exists
        assert not Path("simulators.json").exists()

        sims = QuafelSimulators().get_simulators()

        # Check if the file exists
        assert Path("simulators.json").exists()
        assert not sims

    def test_read_configuration_file(self):
        """
        Test the reading of the configuration file
        """

        # write the file content
        with open("simulators.json", "w", encoding="utf-8") as file:
            file.write(
                '[{"name": "sim1", "version": "1.0"}, {"name": "sim2", "version": "2.0"}]'
            )

        # Check if the simulators are read
        assert len(QuafelSimulators().get_simulators()) == 2
        assert QuafelSimulators().get_simulators()[0].get_name() == "sim1"
        assert QuafelSimulators().get_simulators()[0].get_version() == "1.0"
        assert QuafelSimulators().get_simulators()[1].get_name() == "sim2"
        assert QuafelSimulators().get_simulators()[1].get_version() == "2.0"

    def test_configuration_file_changed(self):
        """
        Test if the simulators module detects changes in the configuration file
        """

        # write the file content
        with open("simulators.json", "w", encoding="utf-8") as file:
            file.write(
                '[{"name": "sim1", "version": "1.0"}, {"name": "sim2", "version": "2.0"}]'
            )

        first_read = QuafelSimulators().get_simulators()

        # change the file content
        with open("simulators.json", "w", encoding="utf-8") as file:
            file.write(
                '[{"name": "sim1", "version": "1.0"}, '
                '{"name": "sim2", "version": "2.0"}, '
                '{"name": "sim3", "version": "3.0"}]'
            )

        last_read = QuafelSimulators().get_simulators()

        assert len(first_read) != len(last_read)
