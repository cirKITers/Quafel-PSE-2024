from django.db import models
from hardware_controller.models import HardwareProfile
from simulation_controller.models import SimulatorProfile



class SimulationRun(models.Model):
  
  # ENV

  hardware_profile = models.ForeignKey(HardwareProfile, on_delete=models.CASCADE)

  simulator_name = models.ForeignKey(SimulatorProfile, on_delete=models.CASCADE)

  # CONF

  shots = models.IntegerField()

  qubits = models.IntegerField()

  depth = models.IntegerField()


  # STATUS

  finished = models.BooleanField(default=False) # enums in orm ??

  expressability = models.FloatField()  # how to represent optional SimulationResult data ?

  entangelment_cap = models.FloatField()

  durations = models.FloatField(max_length=100)

