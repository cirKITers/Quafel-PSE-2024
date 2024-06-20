"""
Apps configuration for chart app.
"""

from django.apps import AppConfig


class ChartConfig(AppConfig):
    """
    Configuration for the simulation submit app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chart'
