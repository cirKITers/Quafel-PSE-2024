from django.db import models

from source.model.hardware_profile.HardwareProfileModel import HardwareProfileModel


# This class represents a simulation program and version on a hardware_profile
class SimulationProfileModel(models.Model):
    # The name of the simulation program
    _name = models.CharField(max_length=100)

    # The version of the simulation program
    _version = models.CharField(max_length=100)

    # The hardware_profile this simulation is running on
    _hardware_profile = models.ForeignKey(HardwareProfileModel, on_delete=models.CASCADE)

    # TODO: getter
