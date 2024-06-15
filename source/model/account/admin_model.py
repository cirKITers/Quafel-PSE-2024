"""
This file contains the class definition of the AdminModel.
"""

from django.db import models


# This class represents an admin.
class AdminModel(models.Model):
    """" This class represents an admin. """
    # The first name of the admin
    _first_name = models.CharField(max_length=30)

    # The last name of the admin
    _last_name = models.CharField(max_length=30)

    # The e-Mail address of the admin (kit-mail)
    _e_mail = models.CharField(max_length=60)
