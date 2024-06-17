"""
This module contains the interface for a site of the core app. 
The sites of the core app are displayed as tabs in the web interface if registered as sub sites.
The main site is the default site of the core app.
The login site is the login site of the core app.
"""
from abc import abstractmethod

from source.webapp.core.interfaces.i_component import IComponent


class ISite(IComponent):
    """
    Interface for the site.
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the component.
        If the component is a site, the name of the tab is this name.
        """

    @abstractmethod
    def get_url(self) -> str:
        """
        Returns the URL of the component.
        If the component is a site, the URL of the tab is this URL.
        """

    @abstractmethod
    def get_render_parameters(self) -> dict[str, object]:
        """
        Returns the render parameters of the component.
        """
        return {}
