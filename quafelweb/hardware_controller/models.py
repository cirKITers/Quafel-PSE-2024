from django.db import models
import uuid

class HardwareProfile(models.Model):

  uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

  name = models.CharField(max_length=100)

  description = models.CharField(max_length=500)

  # example "clust-gpu://192.168.0.95:22"
  protocol = models.CharField(max_length=100)

  ip_addr = models.CharField(default='')

  port_addr = models.IntegerField(default=0)

  archived = models.BooleanField(default=False)

  needs_totp = models.BooleanField(default=False)

  def __str__(self):
    return self.name + " " + self.description + " " + self.protocol + " " + self.ip_addr + " " + str(self.port_addr) + " " + str(self.archived)