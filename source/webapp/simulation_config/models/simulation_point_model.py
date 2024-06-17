"""
This file contains the model for the simulation_point.
"""

from django.db import models

from source.webapp.simulation_config.models.simulation_profile_model import SimulationProfileModel
from source.webapp.simulation_config.models.simulation_config_model import SimulationQuery
from source.webapp.simulation_config.util.float_list_field import FloatListField


class SimulationPointModel(models.Model):
    """
    This class represents a point of an api_out_input (a points has multiple results for different shots)
    """

    # The api_out_input-program and version this point was made for
    _simulation_profile = models.ForeignKey(SimulationProfileModel, on_delete=models.CASCADE)

    # The state of the point if it is finished or not
    _finished = models.BooleanField(default=False)

    # The api_out_input run this point belongs to
    _simulation_run = models.ForeignKey("SimulationRunModel", on_delete=models.CASCADE, related_name='points')

    # Amount of shots
    _shots = models.IntegerField()

    # Amount of qubits
    _qubits = models.IntegerField()

    # Depth of the circuit
    _depth = models.IntegerField()

    # List of the results
    _results = FloatListField()  # TODO: implement this class with max_length=?

    # TODO: getter


def get_existing_points(query: SimulationQuery) -> [SimulationPointModel]:
    """
    Get the existing points for a query
    :param query: The query to get the points for.
    :return: The existing points for the query.
    """
    print(query)  # TODO: remove this line
    # TODO: implement this function


def get_non_exiting_points(query: SimulationQuery) -> [SimulationPointModel]:
    """
    Get the non-existing points for a query
    :param query: The query to get the points for.
    :return: The non-existing points for the query.
    """
    print(query)  # TODO: remove this line
    # TODO: implement this function
