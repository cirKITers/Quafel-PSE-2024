# Create your models here.
from django.db import models


#TODO do this from a conf file maybe even in the settings
class SimulatorProfile(models.Model):

  name = models.CharField(max_length=50)

  version = models.CharField(max_length=50)