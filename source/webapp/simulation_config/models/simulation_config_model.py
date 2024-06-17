"""
This class represents a query for the points that should be created or drawn as a graph.
"""

from source.webapp.simulation_config.models.simulation_profile_model import SimulationProfileModel


class SimulationQuery:
    """
    This class represents a query for the points that should be created or drawn as a graph.
    """
    # List of api_hardware profiles the points should be got from
    _simulation_profiles: [SimulationProfileModel]

    # Range and step of the shots
    _shots_min: int
    _shots_max: int
    _shots_step: int

    # Range and step of the qubits
    _qubits_min: int
    _qubits_max: int
    _qubits_step: int

    # Range and step of the depth
    _depth_min: int
    _depth_max: int
    _depth_step: int

    # Amounts of the results that should be got (only creation)
    _amount_results: int

    def is_valid(self) -> bool:
        """
        Check if the query is valid.
        :return: True, if the query is valid, False otherwise.
        """
        # TODO: check ranges etc. (implement)
        return False

    def is_drawable_2d(self) -> bool:
        """
        Check if the query is drawable as a 2d graph.
        :return:  True, if the query is drawable as a 2d graph, False otherwise.
        """
        # TODO: check if the query is drawable (implement)
        return False

    # TODO: getter
