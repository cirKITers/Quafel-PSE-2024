"""
This file contains the SimulationProfileModel class, 
which represents an api_simulation program and version on a hardware_profile.
"""

from django.db import models
from source.model.hardware_profile.hardware_profile_model import HardwareProfileModel


class SimulationProfileModel(models.Model):
    """
    This class represents an api_simulation program and version on a hardware_profile.
    """

    # The name of the api_simulation program
    _name = models.CharField(max_length=100)

    # The version of the api_simulation program
    _version = models.CharField(max_length=100)

    # The hardware_profile this api_simulation is running on
    _hardware_profile = models.ForeignKey(HardwareProfileModel, on_delete=models.CASCADE)

    # TODO: getter
