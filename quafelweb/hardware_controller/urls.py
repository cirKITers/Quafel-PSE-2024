from django.urls import path

import hardware_controller.views as views

urlpatterns = [
  path('', views.HardwareView.manage_profiles, name='hardware'),
  path('add/', views.HardwareView.add_profile),
  path('delete/', views.HardwareView.delete_profile, name="delete_hardware"),
  path('configure/', views.HardwareView.configure_profile),
  path('configure/submit/', views.HardwareView.submit_change),
]