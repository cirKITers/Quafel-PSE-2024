from django.db import models


# This class represents a hardware-profile, where the simulations are run
class HardwareProfileModel(models.Model):
    # The name of the hardware_profile chosen by the admin
    _name = models.CharField(max_length="100")

    # The ip-address of the hardware_profile to access it
    _ipaddress = models.GenericIPAddressField()

    # The port of the hardware_profile to access it
    _port = models.IntegerField()

    # TODO: getter

    # TODO: Additional information for the cluster:
    # TODO: maybe add this information in another class
    # TODO: how to start it on the other side (ssh, etc.)?
