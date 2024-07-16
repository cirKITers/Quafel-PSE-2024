from django.shortcuts import render
from account_controller.views import AccountView


class SimulationRequestView:

  @AccountView.require_login
  def select_configuration(request):
    return render(request, 'simulation_configuration.html')


  @AccountView.require_login
  def select_environments(request):
    
    return render(request, 'environment_configuration.html')


  @AccountView.require_login
  def submit_request(request):
    ...


  @AccountView.require_login
  def claim_results(request):
    ...
