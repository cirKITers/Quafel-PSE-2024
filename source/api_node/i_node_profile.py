"""
This modules purpose is to define the interface for a node profile outside the hardware-node-app of django.
This prevents that the simulation_config app is dependent on the hardware-node app.

This module contains the interface for a hardware-node.
A hardware-node has a description to describe the hardware-node and some information to connect to the node.
"""

from abc import abstractmethod, ABC


class INodeProfile(ABC):
    """
    Interface for the hardware-node model.
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the hardware-node.
        """

    @abstractmethod
    def get_description(self) -> str:
        """
        Returns the description of the hardware-node.
        """

    @abstractmethod
    def get_ip(self) -> str:
        """
        Returns the ip of the hardware-node.
        """

    @abstractmethod
    def get_port(self) -> int:
        """
        Returns the port of the hardware-node.
        """
