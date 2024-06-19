"""
Views for the core app.
"""

from django.http import HttpResponse

from source.webapp.core import registry


def index(request):
    """
    Index view for the core app.
    The index should be the main site of the core app.
    """
    print(request)  # TODO: delete this line.

    main_site = registry.registry.get_main_site()
    if main_site is not None:
        return HttpResponse(main_site.get_html())

    return HttpResponse("It is no main site registered.")
