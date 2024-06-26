# Create your models here.
from django.db import models
from simulation_data.models import SimulationRun

class SimulationRequest(models.Model):
  
  requested_runs = models.ForeignKey(SimulationRun, on_delete=models.CASCADE, max_length=1000) # yeah idk 

  user = models.CharField(max_length=40)

  