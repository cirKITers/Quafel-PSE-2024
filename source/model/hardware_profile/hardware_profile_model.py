from django.db import models


# This class represents a hardware_profile, where the simulations are run
class HardwareProfileModel(models.Model):
    # The name of the hardware_profile chosen by the admin
    _name = models.CharField(max_length="100")

    # The ip-address of the hardware_profile to access it
    _ipaddress = models.GenericIPAddressField()

    # The port of the hardware_profile to access it
    _port = models.IntegerField()

    # TODO: getter and setter