from django.urls import path
import simulation_controller.views as views

urlpatterns = [
  path('', views.SimulationRequestView.select_configuration, name='simulation_configuration'),
  path('environments/', views.SimulationRequestView.select_environments, name='simulation_environment_configuration'),
]
