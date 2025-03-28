from django.urls import path

import hardware_controller.views as views

urlpatterns = [
    path("", views.HardwareView.manage_profiles, name="hardware"),
    path("add/", views.HardwareView.add_profile, name="add_hardware"),
    path("delete/", views.HardwareView.delete_profile, name="delete_hardware"),
    path("delete_confirm/", views.HardwareView.delete_runs, name="delete_confirm"),
    path("configure/", views.HardwareView.configure_profile, name="configure_hardware"),
    path("configure/submit/", views.HardwareView.submit_change),
]
