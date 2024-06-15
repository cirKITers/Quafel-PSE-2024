"""
This file contains the FloatListField class, which is a custom field for Django models.
"""
from django.db import models


class FloatListField(models.Field):  # Maybe it needs something else than models.Field
    """
    This class represents a list of floats as a custom field for Django models.
    """

    # The maximum length of the list
    _max_length: int

    def get_all(self) -> [float]:
        """
        Get all floats in the list.
        :return: List of float containing all floats in the list.
        """
        # TODO: implement this function

    def get(self, index: int) -> float:
        """
        Get the float at the given index.
        :param index: The index of the float.
        :return: The float at the given index.
        """
        # TODO: implement this function

    def set(self, index: int, value: float):
        """
        Set the float at the given index to the given value.
        :param index: Index of the float.
        :param value: Value to set the float to.
        """
        # TODO: implement this function

    def get_max_length(self) -> int:
        """
        Get the maximum length of the list.
        :return: The maximum length of the list.
        """
        return self._max_length

    def get_average(self) -> float:
        """
        Get the average of all floats in the list.
        :return: The average of all floats in the list.
        """
        return 0.0  # TODO: implement this function
