from django.db import models

class Hardwareprofil(models.Model):
    description = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)