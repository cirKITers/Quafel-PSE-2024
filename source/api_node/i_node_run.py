"""
This modules purpose is to define the interface for a node run outside the hardware-node-app of django.
This prevents that the simulation_config app is dependent on the hardware-node app.

This module contains the interface for a node-run.
A node-run has a node_profile to describe where it runs and the postion of the output of the run.
"""

from abc import abstractmethod, ABC


class INodeRun(ABC):
    """
    Interface for the node-run model.
    """

    @abstractmethod
    def get_node_profile(self) -> str:
        """
        Returns the node_profile of the node-run.
        """

    @abstractmethod
    def get_output_position(self) -> str:
        """
        Returns the output position of the node-run.
        """
