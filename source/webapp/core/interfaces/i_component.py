"""
This module contains the interface for a component.
A component is a part of a site. 
"""
from abc import abstractmethod, ABC


# TODO: Somehow register the components to the core app.
class IComponent(ABC):
    """
    Interface for the component model.
    """

    @abstractmethod
    def get_html(self) -> str:
        """
        Returns the HTML of the component.
        """
