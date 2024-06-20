from django.db import models

# Create your models here.

class QuafelAdmin(models.Model):
    
  identifier = models.CharField(max_length=200, primary_key=True)

  def __str__(self):
    return self.identifier
