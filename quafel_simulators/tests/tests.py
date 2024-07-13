"""
Here are tests defined to test the quafel_simulators module.
"""

import unittest


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


class TestSubmitter(unittest.TestCase):
    """
    Test the submitter module
    """

    def test_setup_hardware(self):
        """
        Test the setup of the hardware
        """

        # TODO


if __name__ == '__main__':
    unittest.main()
