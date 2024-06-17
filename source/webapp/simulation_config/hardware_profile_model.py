"""
This file contains the model for the hardware_profile.
"""

from django.db import models


class HardwareProfileModel(models.Model):
    """
    This class represents a hardware_profile, where the simulations are run
    """

    # The name of the hardware_profile chosen by the admin
    _name = models.CharField(max_length="100")

    # The ip-address of the hardware_profile to access it
    _ipaddress = models.GenericIPAddressField()

    # The port of the hardware_profile to access it
    _port = models.IntegerField()

    # TODO: getter and setter
