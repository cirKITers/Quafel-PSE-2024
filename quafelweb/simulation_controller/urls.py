from django.urls import path
import simulation_controller.views as views

urlpatterns = [
  path('', views.SimulationRequestView.default, name='simulation_configuration'),
  path('select_configuration/', views.SimulationRequestView.select_configuration, name='select_configuration'),
  path('select_environments/', views.SimulationRequestView.select_environments, name='simulation_environment_configuration'),
  path('submit_request/', views.SimulationRequestView.submit_request, name='submit_request'),

]
