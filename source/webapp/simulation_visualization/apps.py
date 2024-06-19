"""
Apps configuration for simulation visual app.
"""

from django.apps import AppConfig


class SimulationVisualConfig(AppConfig):
    """
    Configuration for the simulation submit app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simulation_visualization'
