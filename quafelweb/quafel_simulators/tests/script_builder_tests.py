"""
Tests for the module responsible for building the scripts.
"""

import yaml

from quafel_simulators.output import QuafelOutputHardware
from quafel_simulators.tests.util import TestCase, TestClassSimulationRequest
from quafel_simulators.util.script_builder import (
    build_quafel_yml_configuration,
    build_quafel_script_submit,
    build_quafel_script_setup,
    build_quafel_script_pull_output,
)


class TestScriptBuilder(TestCase):
    """
    Test the script builder module
    """

    def test_build_quafel_yml_configuration(self):
        """
        Test the building of the yml configuration
        """

        simulation_request = TestClassSimulationRequest()
        generated_yml = build_quafel_yml_configuration(simulation_request)

        # Read yml from path:
        with open("../script/quafel_test_yml.yml", "r", encoding="utf-8") as yml_file:
            read_yml = yml_file.read()

        assert str(yaml.compose(generated_yml)) == str(yaml.compose(read_yml))

    def test_build_quafel_script_submit(self):
        """
        Test the building of the quafel script
        """

        build_script = build_quafel_script_submit(
            TestClassSimulationRequest(), QuafelOutputHardware()
        )
        print(build_script)

    def test_build_quafel_script_setup(self):
        """
        Test the building of the quafel script
        """

        build_script = build_quafel_script_setup(TestClassSimulationRequest())
        print(build_script)

        assert str.find(build_script, "'") == -1

    def test_build_quafel_script_pull_output(self):
        """
        Test the building of the pull output script
        """

        build_script = build_quafel_script_pull_output(QuafelOutputHardware(), "tests")
        print(build_script)
