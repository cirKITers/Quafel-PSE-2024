import unittest
from unittest.mock import patch, MagicMock
import uuid
from hardware_controller.models import HardwareProfile
from quafel_simulators.base.simulation_request import IncrementType
from quafel_simulators.quafelsubmitter import QuafelSubmitter
from simulation_controller.util.output_handler import handle_output
from simulation_controller.util.simulation_request import SimulationRequest, SimulationRequestRange
from simulation_data.models import SimulatorProfile

# Somehow cant run the test, because of the import error, idk why
class TestSimulationRequestSubmission(unittest.TestCase):

    @patch('simulation_controller.util.simulation_request.SimulationRequestRange.save', MagicMock())
    @patch('hardware_controller.models.HardwareProfile.save', MagicMock())
    @patch('simulation_data.models.SimulatorProfile.save', MagicMock())
    @patch('quafel_simulators.quafelsubmitter.QuafelSubmitter.submit', MagicMock())
    def test_simulation_request_submission(self):
        
        # Example values for the parameters
        qubits_min = 2
        qubits_max = 4
        qubits_increment = 1
        qubits_increment_type = IncrementType.LINEAR  # Assuming IncrementType has a LINEAR value

        shots_min = 2
        shots_max = 6
        shots_increment = 1
        shots_increment_type = IncrementType.EXPONENTIAL  # Assuming IncrementType has an EXPONENTIAL value

        depth_min = 2
        depth_max = 4
        depth_increment = 1
        depth_increment_type = IncrementType.LINEAR  # Assuming IncrementType has a LINEAR value

        # Create an instance of SimulationRequestRange
        simulation_request_range = SimulationRequestRange(qubits_min, qubits_max, qubits_increment, qubits_increment_type, shots_min, shots_max, shots_increment, shots_increment_type, depth_min, depth_max, depth_increment, depth_increment_type)

        simulation_request_range.save()


        hwp = HardwareProfile(uuid=uuid.uuid4(),name="BWUniCluster GPU Cluster",description="BWUniCluster GPU Cluster",protocol="GPU-Cluster",ip_addr="bwunicluster.scc.kit.edu",port_addr=22,archived=False,needs_totp=True)
        hwp.save()

        smp = SimulatorProfile(name="pennylane_fw")
        smp.save()

        # Instantiate the SimulationRequest class
        simulation_request = SimulationRequest(simulation_range=simulation_request_range, hardware=hwp, simulator=smp, username="zn8422", password="!xKLiZf^g7BbAF", top="789737")
        QuafelSubmitter().submit(simulation_request, handle_output)

if __name__ == '__main__':
    unittest.main()