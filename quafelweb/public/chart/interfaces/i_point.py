"""
This modules purpose is to define the interface for a point outside the chart-app of django.
This prevents that the simulation_configuration app is dependent on the chart app.

This module contains the interface for a point.
A point can be drawn on a chart.
"""
from abc import abstractmethod, ABC


class IPoint(ABC):
    """
    Interface for the point model.
    """

    @abstractmethod
    def get_x(self) -> float:
        """
        Returns the x value of the point.
        """

    @abstractmethod
    def get_y(self) -> list[float]:
        """
        Returns the y value of the point.
        """
