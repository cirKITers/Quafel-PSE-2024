from django.db import models


# List of floats to store the results of the api_simulation in the database
class FloatListField(models.Field):  # Maybe it needs something else than models.Field
    # The maximum length of the list
    _max_length: int

    # Get the floats of this list
    def get_all(self) -> [float]:
        return None  # TODO: implement this function

    # Get the float at the given index
    def get(self, index: int) -> float:
        return 0  # TODO: implement this function

    # Set the float at the given index
    def set(self, index: int, value: float):
        pass  # TODO: implement this function

    # Get the maximum length of the list
    def get_max_length(self) -> int:
        return self._max_length

    # Get the average of all floats in the list
    def get_average(self) -> float:
        return 0.0  # TODO: implement this function
