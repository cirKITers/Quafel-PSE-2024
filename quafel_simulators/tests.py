"""
Here are tests defined to test the quafel_simulators module.
"""

import unittest
from time import sleep

from quafel_simulators.runner import Runner


class TestRunner(unittest.TestCase):
    """
    Test the integer arithmetic operations
    """

    def test_run_update_loop_and_stop(self):
        """
        Test the update loop and the stop function
        """
        runner = Runner()
        runner.start_updater()

        self.assertTrue(runner.running)

        sleep(3)

        runner.stop_updater()


if __name__ == '__main__':
    unittest.main()
