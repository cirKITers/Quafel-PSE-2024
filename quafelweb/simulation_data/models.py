'''
Defines the models used to store SimulationRuns in an database
'''
from django.db import models
from django.db.models.signals import post_init
from django.contrib.postgres.fields import ArrayField
from hardware_controller.models import HardwareProfile


#TODO do this from a conf file maybe even in the settings
class SimulatorProfile(models.Model):

  name = models.CharField(max_length=50)


class SimulationRun(models.Model):
  
  # ENV

  hardware_profile = models.ForeignKey(HardwareProfile, on_delete=models.CASCADE)

  simulator_name = models.ForeignKey(SimulatorProfile, on_delete=models.CASCADE)

  user = models.CharField(max_length=100)

  # CONF

  shots = models.IntegerField()

  qbits = models.IntegerField()
  
  depth = models.IntegerField()

  evals = models.IntegerField()


  # STATUS

  finished = models.BooleanField(default=False) # enums in orm ??

  expressability = models.FloatField()  # how to represent optional SimulationResult data ?

  entangelment_cap = models.FloatField()

  durations = models.FloatField(max_length=100) # ArrayField(models.FloatField())


  def __repr__(self) -> str:
     return f"Simulatorporfile {self.shots=} {self.qbits=} {self.depth=} {self.evals=}"


def my_handler(**kwargs):
    print("Run Handler")


post_init.connect(my_handler, sender=SimulatorProfile)