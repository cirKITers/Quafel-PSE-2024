"""
Defines the models used for creating new simulations runs
"""

from django.db import models

from simulation_data.models import SimulationRun


class SimulationRequest(models.Model):
    """
    Defines a SimulationRequest
    """

    requested_runs = models.ForeignKey(
        SimulationRun, on_delete=models.CASCADE, max_length=1000
    )

    user = models.CharField(max_length=40)
