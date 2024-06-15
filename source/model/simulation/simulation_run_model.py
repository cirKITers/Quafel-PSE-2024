"""
This file contains the SimulationRunModel class, 
which represents an api_simulation run containing multiple or one point(s).
"""


from django.db import models
from source.model.simulation.simulation_point_model import SimulationPointModel


class SimulationRunModel(models.Model):
    """
    This class represents an api_simulation run containing multiple or one point(s).
    This class is used to identify the location, where the result of run is stored to complete the api_simulation.
    """

    def get_points(self) -> [SimulationPointModel]:
        """
        Get the points of this run
        :return: The points of this run
        """
        return self.points.all()  # TODO: check

    def get_finished_points(self) -> [SimulationPointModel]:
        """
        Get the finished points of this run
        :return: The finished points of this run
        """
        return self.points.filter(_finished=True)  # TODO: check

    def get_unfinished_points(self) -> [SimulationPointModel]:
        """
        Get the unfinished points of this run
        :return: The unfinished points of this run
        """
        return self.points.filter(_finished=False)  # TODO: check

    def is_finished(self) -> bool:
        """
        Check if this run is finished
        :return: True if this run is finished, False otherwise
        """
        return self.get_unfinished_points().count() == 0

    def get_path(self) -> str:
        """
        Get the path of the run
        The path is the location where the result of the run is stored to complete the api_simulation.
        :return: The path of the run
        """
        # TODO: implement this function

    # TODO: getter
