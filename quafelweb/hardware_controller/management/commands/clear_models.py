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


        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared the database"
            )
        )
