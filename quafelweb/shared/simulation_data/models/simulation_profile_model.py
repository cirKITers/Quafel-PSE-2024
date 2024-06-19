"""
This file contains the SimulationProfileModel class,
which represents an api_out_input program and version on a hardware_profile.
"""

from django.db import models
from quafelweb.quafelweb.simulation_data.hardware_profile_model import HardwareProfileModel


class SimulationProfileModel(models.Model):
    """
    This class represents an api_out_input program and version on a hardware_profile.
    """

    # The name of the api_out_input program
    _name = models.CharField(max_length=100)

    # The version of the api_out_input program
    _version = models.CharField(max_length=100)

    # The hardware_profile this api_out_input is running on
    _hardware_profile = models.ForeignKey(HardwareProfileModel, on_delete=models.CASCADE)

    # TODO: getter
