from django.test import TestCase
from simulation_data import SimulationRun, SimulatorProfile
from hardware_controller.models import HardwareProfile

#TODO fill out data
class SimulationRunTestCase(TestCase):
    def setUp(self):

        self.hardware = HardwareProfile.objects.create(name="QuantumHardware")
        self.simulator = SimulatorProfile.objects.create(name="QuantumSimulator")

        self.simulation_run = SimulationRun.objects.create(
            id=42,
            hardware=self.hardware,
            simulator=self.simulator,
            user="test_user",
            shots=50,
            qubits=2,
            depth=6,
            finished=False,
            expressibility=0.75,
            entangling_capability=0.25,
            durations=[1.2, 1.3, 1.4, 1.5, 1.6],
            duration_avg=1.4,
        )

    def test_simulation_run_creation(self):

        self.assertIsInstance(self.simulation_run, SimulationRun)
        self.assertEqual(self.simulation_run.user, "test_user")
        self.assertEqual(self.simulation_run.shots, 52)
        self.assertEqual(self.simulation_run.qubits, 2)
        self.assertEqual(self.simulation_run.depth, 6)
        self.assertEqual(self.simulation_run.finished, False)
        self.assertEqual(self.simulation_run.expressibility, 0.75)
        self.assertEqual(self.simulation_run.entangling_capability, 0.25)
        self.assertEqual(self.simulation_run.durations, [1.2, 1.3, 1.4, 1.5, 1.6])
        self.assertEqual(self.simulation_run.duration_avg, 1.4)

    def test_simulation_run_str_method(self):

        expected_str = "QuantumHardware QuantumSimulator test_user 52 2 6 False"
        self.assertEqual(str(self.simulation_run), expected_str)

    def test_simulation_run_default_values(self):

        simulation_run = SimulationRun.objects.create(
            id=2,
            hardware=self.hardware,
            simulator=self.simulator,
            user="default_test",
            shots=88,
            qubits=6,
            depth=66,
        )
        self.assertEqual(simulation_run.finished, False)
        self.assertEqual(simulation_run.duration_avg, 0.0)