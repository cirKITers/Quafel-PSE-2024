from django.test import TestCase, Client
from django.urls import reverse
from simulation_data.models import SimulatorProfile, HardwareProfile, SimulationRun

class SimulationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('simulation_index')

        # Create mock data thats needed, pls adjust
        self.simulator1 = SimulatorProfile.objects.create(name='Simulator 1')
        self.simulator2 = SimulatorProfile.objects.create(name='Simulator 2')
        self.hardware1 = HardwareProfile.objects.create(name='Hardware 1')
        self.hardware2 = HardwareProfile.objects.create(name='Hardware 2')

        # Create mock data thats needed, pls adjust
        self.simulation_run = SimulationRun.objects.create(
            hardware=self.hardware1,
            simulator=self.simulator1,
            user='TestUser',
            shots=100,
            qubits=5,
            depth=10,
            expressibility=0.5,
            entangling_capability=0.5,
            duration_avg=1.0,
            finished=True
        )

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulation_view.html')
        self.assertIn('environments', response.context)
        self.assertIn('hardware_profiles', response.context)
        self.assertIn('simulator_profiles', response.context)

    def test_index_GET_with_filters(self):
        response = self.client.get(self.index_url, {
            'simulator_filter': 'Simulator 1',
            'hardware_filter': 'Hardware 1'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulation_view.html')
        self.assertTrue(any(env.simulator.name == 'Simulator 1' and env.hardware.name == 'Hardware 1' for env in response.context['environments']))

    def test_index_GET_with_no_matching_filters(self):
        response = self.client.get(self.index_url, {
            'simulator_filter': 'NonExistentSimulator',
            'hardware_filter': 'NonExistentHardware'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulation_view.html')
        self.assertEqual(len(response.context['environments']), 0)