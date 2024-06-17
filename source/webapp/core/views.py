"""
Views for the core app.
"""

from django.http import HttpResponse


def index(request):
    """
    Index view for the core app.
    """
    print(request)  # TODO Remove this line
    return HttpResponse("Hello, world. You're at the cores index.")
