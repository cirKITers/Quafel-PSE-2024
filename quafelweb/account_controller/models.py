import uuid
from django.db import models

# Create your models here.
class AdminAccount(models.Model):
    
  uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  identifier = models.CharField(max_length=50)
