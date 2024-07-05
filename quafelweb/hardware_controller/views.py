from django.shortcuts import render
from account_controller.views import AccountView
# Create your views here.

class HardwareView:

  # /hardware

  @AccountView.require_login
  def manage_profiles(request):
    context = {
      'hardware_profiles' : []
    }
    return render(request, 'hardware.html', context=context)

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


  
