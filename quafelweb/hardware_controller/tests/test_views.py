from django.test import TestCase, Client
from django.urls import reverse
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulationRun

class HardwareViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.hardware_url = reverse('hardware')
        self.add_url = reverse('add_hardware')
        self.delete_url = reverse('delete_hardware')
        self.delete_runs_url = reverse('delete_runs')
        self.configure_url = reverse('configure_hardware')
        self.submit_change_url = reverse('submit_change')

        # adjust data as needed
        self.hardware1 = HardwareProfile.objects.create(
            name='Hardware 1',
            description='Description 1',
            protocol='http',
            ip_addr='192.168.0.1',
            port_addr=8080
        )
        self.simulation_run = SimulationRun.objects.create(
            hardware=self.hardware1,
            simulator=None,  # adjust data
            user='TestUser',
            shots=100,
            qubits=5,
            depth=10,
            expressibility=0.5,
            entangling_capability=0.5,
            duration_avg=1.0,
            finished=True
        )

    def test_manage_profiles_GET(self):
        response = self.client.get(self.hardware_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'hardware.html')
        self.assertIn('profiles', response.context)

    def test_add_profile_POST_valid_data(self):
        initial_count = HardwareProfile.objects.count()

        response = self.client.post(self.add_url, {
            'name': 'Hardware 2',
            'description': 'Description 2',
            'connection': 'http://192.168.0.2:8080'
        })

        new_count = HardwareProfile.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count + 1)

    def test_add_profile_POST_invalid_data(self):
        initial_count = HardwareProfile.objects.count()

        response = self.client.post(self.add_url, {
            'name': '',
            'connection': 'http://192.168.0.2:8080'
        })

        new_count = HardwareProfile.objects.count()

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')
        self.assertEquals(new_count, initial_count)

    def test_delete_profile_POST_with_runs(self):
        response = self.client.post(self.delete_url, {
            'id': self.hardware1.uuid
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')
        self.assertIn('Deleting Simulation Data', response.context['header'])

    def test_delete_profile_POST_without_runs(self):

        SimulationRun.objects.filter(hardware=self.hardware1).delete()

        initial_count = HardwareProfile.objects.count()

        response = self.client.post(self.delete_url, {
            'id': self.hardware1.uuid
        })

        new_count = HardwareProfile.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count - 1)

    def test_delete_runs_POST(self):
        initial_simulation_count = SimulationRun.objects.count()
        initial_hardware_count = HardwareProfile.objects.count()

        response = self.client.post(self.delete_runs_url, {
            'id': self.hardware1.uuid
        })

        new_simulation_count = SimulationRun.objects.count()
        new_hardware_count = HardwareProfile.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_simulation_count, initial_simulation_count - 1)
        self.assertEquals(new_hardware_count, initial_hardware_count - 1)

    def test_configure_profile_GET(self):
        response = self.client.get(self.configure_url, {'id': self.hardware1.uuid})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'configuration.html')
        self.assertIn('hardware', response.context)

    def test_submit_change_POST_valid_data(self):
        response = self.client.post(self.submit_change_url, {
            'id': self.hardware1.uuid,
            'name': 'Updated Hardware 1',
            'connection': 'http://192.168.0.3:8080'
        })

        self.hardware1.refresh_from_db()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.hardware1.name, 'Updated Hardware 1')
        self.assertEquals(self.hardware1.ip_addr, '192.168.0.3')

    def test_submit_change_POST_invalid_data(self):
        response = self.client.post(self.submit_change_url, {
            'id': self.hardware1.uuid,
            'name': '',  # Invalid because name is empty
            'connection': 'http://192.168.0.3:8080'
        })

        self.hardware1.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')
        self.assertNotEquals(self.hardware1.name, '')