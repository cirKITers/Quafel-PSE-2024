import random

from django.core.management.base import BaseCommand

from hardware_controller.models import HardwareProfile  # Import your model
from simulation_data.models import SimulationRun, SimulatorProfile


class Command(BaseCommand):
    help = 'Populates the database with example model entries'

    HardwareProfile.objects.all().delete()
    SimulatorProfile.objects.all().delete()
    SimulationRun.objects.all().delete()

    def handle(self, *args, **kwargs):
        hwp_example = HardwareProfile(name='HWP1', description='Dies ist ein Beispiel HWP', protocol='clust-gpu://192.168.0.95:22', ip_addr='100.0.0.0', port_addr='1', archived=False)
        hwp_example.save()
        hwp_example = HardwareProfile(name='HWP2', description='Dies ist ein Beispiel HWP', protocol='clust-cpu://192.168.0.97:22', ip_addr='101.0.0.0', port_addr='2', archived=False)
        hwp_example.save()
        hwp_example = HardwareProfile(name='HWP3', description='Dies ist ein Beispiel HWP', protocol='localhost', ip_addr='102.0.0.0', port_addr='3', archived=False)
        hwp_example.save()

        smp_profile = SimulatorProfile(name='pennylane_fw', version='1.0')
        smp_profile.save()
        smp_profile = SimulatorProfile(name='pennylane_fw', version='1.3')
        smp_profile.save()
        smp_profile = SimulatorProfile(name='qiskit_fw', version='2.0')
        smp_profile.save()
        smp_profile = SimulatorProfile(name='qibo_fw', version='1.3')
        smp_profile.save()


        for q in range(1, 10):
            for d in range(1, 10):
                for s in range(6, 10):
                    for e in range(20, 31, 10):
                        random_hwp = HardwareProfile.objects.order_by('?').first()
                        random_smp = SimulatorProfile.objects.order_by('?').first()
                        sim_run = SimulationRun(hardware_profile=random_hwp, simulator_name=random_smp, user='test', shots=s, qbits=q, depth=d, evals=e, finished=True, expressability=random.randint(12345678, 987654321), entangelment_cap=random.randint(12345678, 987654321), durations=random.randint(12345678, 1147483640))
                        sim_run.save()
        
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with example entries'))