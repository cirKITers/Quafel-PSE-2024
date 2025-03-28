"""
Defines the models used to store SimulationRuns in an database
"""

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.template.defaultfilters import default

from hardware_controller.models import HardwareProfile
from quafel_simulators.base.simulator import QuafelSimulatorBase


class SimulatorProfile(models.Model, QuafelSimulatorBase):

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return "latest"

    name = models.CharField(max_length=50, primary_key=True, unique=True)


class SimulationRun(models.Model):

    id = models.IntegerField(primary_key=True)

    # ENV

    hardware = models.ForeignKey(HardwareProfile, on_delete=models.CASCADE)

    simulator = models.ForeignKey(SimulatorProfile, on_delete=models.CASCADE)

    user = models.CharField(max_length=100, default="")

    # CONF

    shots = models.IntegerField()

    qubits = models.IntegerField()

    depth = models.IntegerField()

    # STATUS

    finished = models.BooleanField(default=False)

    expressibility = models.FloatField(default=0.0)

    entangling_capability = models.FloatField(default=0.0)

    durations = ArrayField(models.FloatField(), 100)

    duration_avg = models.FloatField(default=0.0)

    def __str__(self):
        return (
            self.hardware.name
            + " "
            + self.simulator.name
            + " "
            + self.user
            + " "
            + str(self.shots)
            + " "
            + str(self.qubits)
            + " "
            + str(self.depth)
            + " "
            + str(self.finished)
        )
