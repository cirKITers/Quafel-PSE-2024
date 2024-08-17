import random

from django.core.management.base import BaseCommand

from hardware_controller.models import HardwareProfile  # Import your model
from simulation_data.models import SimulationRun, SimulatorProfile


class Command(BaseCommand):
    help = "Populates the database with example model entries"


    def handle(self, *args, **kwargs):
        HardwareProfile.objects.all().delete()
        SimulatorProfile.objects.all().delete()
        SimulationRun.objects.all().delete()
        
        hwp_example = HardwareProfile(
            name="HWP1",
            description="Dies ist ein Beispiel HWP",
            protocol="clust-gpu://192.168.0.95:22",
            ip_addr="100.0.0.0",
            port_addr="1",
            archived=False,
        )
        hwp_example.save()
        hwp_example = HardwareProfile(
            name="HWP2",
            description="Dies ist ein Beispiel HWP",
            protocol="clust-cpu://192.168.0.97:22",
            ip_addr="101.0.0.0",
            port_addr="2",
            archived=False,
            needs_totp=True,
        )
        hwp_example.save()
        hwp_example = HardwareProfile(
            name="HWP3",
            description="Dies ist ein Beispiel HWP",
            protocol="localhost",
            ip_addr="102.0.0.0",
            port_addr="3",
            archived=False,
            needs_totp=True,
        )
        hwp_example.save()

        smp_profile = SimulatorProfile(name="pennylane_fw")
        smp_profile.save()
        smp_profile = SimulatorProfile(name="qiskit_fw")
        smp_profile.save()
        smp_profile = SimulatorProfile(name="qibo_fw")
        smp_profile.save()

        id = 0
        for q in range(1, 10):
            for d in range(1, 10):
                for s in range(6, 10):

                    random_hwp = HardwareProfile.objects.order_by("?").first()
                    random_smp = SimulatorProfile.objects.order_by("?").first()
                    sim_run = SimulationRun(
                        id=id,
                        hardware=random_hwp,
                        simulator=random_smp,
                        user="tests",
                        shots=s,
                        qubits=q,
                        depth=d,
                        finished=True,
                        expressibility=random.uniform(1234, 11440),
                        entangling_capability=random.uniform(1234, 11440),
                        durations=[random.uniform(1234, 11440) for _ in range(100)],
                        duration_avg=random.uniform(1234, 11440),
                    )
                    sim_run.save()
                    id += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with example entries"
            )
        )
