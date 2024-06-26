from django.db import models


class HardwareProfile(models.Model):

  name = models.CharField(max_length=100, primary_key=True)

  description = models.CharField(max_length=1000)

  # example "clust-gpu://192.168.0.95:22"
  protocol = models.CharField(max_length=100)

  ip_addr = models.GenericIPAddressField(default='240.0.0.0')

  port_addr = models.IntegerField(default=0)

  archived = models.BooleanField(default=False)




