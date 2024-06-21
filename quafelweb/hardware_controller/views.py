from account_controller.manager import AccountManager

# Create your views here.

class HardwareView:

  # /hardware
  def index(request):
    ...

  # /hardware/add with post
  def add_profile(request):
    ...

  # /hardware/remove with post
  def remove_profile(request):
    ...

  # /hardware/archive with post
  def archive_profile(request):
    ...

  # return List of HardwareProfile Ids connected with the request (persistent Links)
  def getConst(request):
    ...

  
