"""
Test the split function
"""

import unittest
import uuid

from hardware_controller.models import HardwareProfile
from quafel_simulators.base.simulation_request import IncrementType
from simulation_controller.util.simulation_request import SimulationRequestRange, _exp_range
from simulation_data.models import SimulationRun, SimulatorProfile


class TestSplit(unittest.TestCase):
    """
    Test the split() function
    """

    def test_split(self):
        """
        Test the the split() function
        """

        # Create test data
        simulationrequestrange: SimulationRequestRange = SimulationRequestRange(1, 10, 1, IncrementType.LINEAR, 1, 20, 2, IncrementType.LINEAR, 5, 30, 1, IncrementType.EXPONENTIAL)

        hwp = HardwareProfile(
            uuid=uuid.uuid4(),
            name="BWUniCluster",
            description="BWUniClusterGPUCluster",
            protocol="GPU-Cluster",
            ip_addr="bwunicluster.scc.kit.edu",
            port_addr=22,
            archived=False, 
            needs_totp=True)
        hwp.save()

        smp = SimulatorProfile(name="pennylane_fw")
        smp.save()

        existingSimulationRun = SimulationRun(1, hwp, smp, "user1", 5, 10, 10, True, 1.0, 1.0, [1.0], 1.0)

        # Test the split function

        splittedRanges = simulationrequestrange.split(existingSimulationRun)
        for q in _exp_range(
            simulationrequestrange.qubits_min,
            simulationrequestrange.qubits_max,
            simulationrequestrange.qubits_increment,
            simulationrequestrange.qubits_increment_type,
        ):
            for s in _exp_range(
                simulationrequestrange.shots_min,
                simulationrequestrange.shots_max,
                simulationrequestrange.shots_increment,
                simulationrequestrange.shots_increment_type,
            ):
                for d in _exp_range(
                    simulationrequestrange.depth_min,
                    simulationrequestrange.depth_max,
                    simulationrequestrange.depth_increment,
                    simulationrequestrange.depth_increment_type,
                ):
                    singelRun = SimulationRun(1, hwp, smp, "user1", s, q, d, True, 1.0, 1.0, [1.0], 1.0)
                    for r in splittedRanges:
                        if r.run_in_range(singelRun):
                            break
                    else:  # no break = singleRun wasnt found in any splitted range
                        if singelRun.qubits == existingSimulationRun.qubits and singelRun.shots == existingSimulationRun.shots and singelRun.depth == existingSimulationRun.depth:
                            continue
                        else:
                            self.assertTrue(False, f"Missing run: {singelRun}")
        self.assertTrue(True)
