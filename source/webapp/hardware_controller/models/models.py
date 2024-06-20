from django.db import models

class Hardwareprofil(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)