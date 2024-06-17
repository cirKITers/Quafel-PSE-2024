"""
This modules purpose is to define the interface for a drawable outside the chart-app of django.
This prevents that the simulation_config app is dependent on the chart app.

This module contains the interface for a drawable.
A point can be drawn on a chart.
"""
from abc import abstractmethod, ABC

from source.api_chart.i_point import IPoint


class IDrawable(ABC):
    """
    Interface for the drawable model.
    """

    @abstractmethod
    def get_points(self) -> list[IPoint]:
        """
        Returns the list of points of the drawable.
        """

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the drawable.
        """
