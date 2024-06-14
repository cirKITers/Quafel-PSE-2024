from django.db import models

from source.model.hardware_profile.HardwareProfileModel import HardwareProfileModel


# This class represents an api_simulation program and version on a hardware_profile
class SimulationProfileModel(models.Model):
    # The name of the api_simulation program
    _name = models.CharField(max_length=100)

    # The version of the api_simulation program
    _version = models.CharField(max_length=100)

    # The hardware_profile this api_simulation is running on
    _hardware_profile = models.ForeignKey(HardwareProfileModel, on_delete=models.CASCADE)

    # TODO: getter
