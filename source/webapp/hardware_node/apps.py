"""
Apps configuration for hardware node app.
"""

from django.apps import AppConfig


class HardwareNodeConfig(AppConfig):
    """
    Configuration for the simulation submit app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hardware_node'
