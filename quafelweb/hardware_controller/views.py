from django.shortcuts import render
from account_controller.views import AccountView
# Create your views here.

class HardwareView:

  # /hardware

  @AccountView.require_login
  def manage_profiles(request):
    return render(request, 'hardware.html')

  # /hardware/add with post
  
  @AccountView.require_login
  def add_profile(request):
    ...

  # /hardware/remove with post
  
  @AccountView.require_login
  def remove_profile(request):
    ...

  # /hardware/archive with post
  
  @AccountView.require_login
  def archive_profile(request):
    ...


  
