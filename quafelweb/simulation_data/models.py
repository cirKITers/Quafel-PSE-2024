'''
Defines the models used to store SimulationRuns in an database
'''
from django.contrib.postgres.fields import ArrayField
from django.db import models

from hardware_controller.models import HardwareProfile


class SimulatorProfile(models.Model):

  name = models.CharField(max_length=50, primary_key=True, unique=True)


class SimulationRun(models.Model):

  id = models.IntegerField(primary_key=True)
  
  # ENV

  hardware = models.ForeignKey(HardwareProfile, on_delete=models.CASCADE)

  simulator = models.ForeignKey(SimulatorProfile, on_delete=models.CASCADE)

  user = models.CharField(max_length=100)

  # CONF

  shots = models.IntegerField()

  qubits = models.IntegerField()

  depth = models.IntegerField()

  # STATUS

  finished = models.BooleanField(default=False)

  expressibility = models.FloatField()

  entangling_capability = models.FloatField()

  durations = ArrayField(models.FloatField(), 100)

  duration_avg = models.FloatField(default=0.0)
