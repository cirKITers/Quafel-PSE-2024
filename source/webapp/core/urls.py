"""
This file is used to define the URL patterns for the core app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
