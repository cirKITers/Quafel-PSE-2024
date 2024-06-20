from django.db import models


class HardwareProfile(models.Model):

  name = models.CharField(max_length=100, primary_key=True)

  description = models.CharField(max_length=1000)

  connection = models.CharField(max_length=100)





