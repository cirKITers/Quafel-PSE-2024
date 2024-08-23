from django.urls import path

import simulation_controller.views as views

urlpatterns = [
    path("", views.SimulationRequestView.configuration, name="simulation_configuration"),
    path("confirm/", views.SimulationRequestView.confirmation, name="simulation_confirmation"),
    path("submit/", views.SimulationRequestView.submit_request, name="submit"),
    path(
        "submit_request/",
        views.SimulationRequestView.submit_request,
        name="submit_request",
    ),
]
