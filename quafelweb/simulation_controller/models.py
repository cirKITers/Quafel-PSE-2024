# Create your models here.
from django.db import models

class SimulatorProfile(models.Model):

  name = models.CharField(max_length=50)

  version = models.CharField(max_length=50)