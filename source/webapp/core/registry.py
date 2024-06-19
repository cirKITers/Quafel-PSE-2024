"""
This module contains the registry singleton for the core app.
The registry singleton is used to register the sites of the core app.
The i_sites can be rendered using the render_site function.
"""
from django.shortcuts import render

from source.webapp.core.interfaces.i_site import ISite


class Registry:
    """
    The registry class for the sites of the core app.
    """

    main_site: ISite  # The main site of the core app. This site is visible to any user.
    login_site: ISite  # The login site of the core app. This site is visible to any user.
    sub_sites: dict[int, ISite]  # Sites that are visible to any user.
    admin_sites: dict[int, ISite]  # Sites that are only visible to admins.

    def __init__(self):
        self.main_site = None
        self.login_site = None
        self.sub_sites = {}
        self.admin_sites = {}

    def register_main_site(self, main_site: ISite):
        """
        Registers the main site.
        :param main_site: The main site to register.
        """
        self.main_site = main_site

    def register_login_site(self, login_site: ISite):
        """
        Registers the login site.
        :param login_site: The login site to register.
        """
        self.login_site = login_site

    def register_sub_site(self, index: int, site: ISite, admin_only: bool = False):
        """
        Registers a site.
        :param index: The index of the site.
        :param site: The site to register.
        :param admin_only: If the site is only visible to admins.
        """
        # TODO: Check if the site is already registered.
        # TODO: Check if the index is already used.
        # TODO: Register site.
        if admin_only:
            self.admin_sites[index] = site
        else:
            self.sub_sites[index] = site

    def get_main_site(self) -> ISite:
        """
        Returns the main site.
        :return: The main site.
        """
        return self.main_site

    def get_login_site(self) -> ISite:
        """
        Returns the login site.
        :return: The login site.
        """
        return self.login_site

    def get_sub_sites(self, admin: bool) -> dict[int, ISite]:
        """
        Returns a dict with all sub sites visible to the user.
        :param admin: If the user is an admin.
        :return: The sub sites visible to the user.
        """
        to_return = {}
        for index, site in self.sub_sites.items():
            to_return[index] = site
        if admin:
            for index, site in self.admin_sites.items():
                to_return[index] = site
        return to_return


def render_site(request, site: ISite):
    """
    Renders a site.
    :param request: The request to render the site.
    :param site: The site to render.
    """
    render_parameters = site.get_render_parameters()

    # Add the main site name to the render parameters.
    if (registry.main_site is not None) and (registry.main_site.get_name() is not None):
        # TODO: make it a button and beautify it.
        render_parameters["main_site_name"] = registry.get_main_site().get_name()
    else:
        render_parameters["main_site_name"] = "Main Site"

    # Add the tabs to the render parameters.
    tabs = []
    sub_sites = registry.get_sub_sites(admin=False)  # TODO: Check if the user is an admin.
    # TODO: Bring the sites in the right order.
    for _, sub_site in sub_sites:
        tabs.append({"name": sub_site.get_name(), "url": sub_site.get_url()})
    render_parameters["tabs"] = tabs

    # TODO: login button better

    return render(request, site.get_url(), render_parameters)


# The registry singleton for the core app.
registry = Registry()
