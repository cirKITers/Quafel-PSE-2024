from source.model.simulation.SimulationProfileModel import SimulationProfileModel


# This class represents a query for the points that should be created or drawn as a graph
class SimulationQuery:
    # List of api_simulation profiles the points should be got from
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

    # Check if the query is valid for creation
    def is_valid(self) -> bool:
        # TODO: check ranges etc. (implement)
        return False

    # Check if the query is drawable as a 2d graph
    def is_drawable_2d(self) -> bool:
        # TODO: check if the query is drawable (implement)
        return False

    # TODO: getter
