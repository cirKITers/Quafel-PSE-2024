"""
Apps configuration for simulation config app.
"""

from django.apps import AppConfig


class SimulationConfigConfig(AppConfig):
    """
    Configuration for the simulation submit app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simulation_configuration'
