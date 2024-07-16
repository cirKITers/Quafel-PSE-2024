from django.shortcuts import redirect, render
from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
# Create your views here.

class HardwareView:

  # /hardware

  @AccountView.require_login
  def manage_profiles(request):

    profiles =  HardwareProfile.objects.all()

    if search := request.GET.get("search"):
      profiles = [profile for profile in profiles if search in profile.name]

    
    context = { 'hardware_profiles' : profiles  }
    return render(request, 'hardware.html', context=context)

  # /hardware/add with post
  
  @AccountView.require_login
  def add_profile(request):
    
    if request.method == "POST":
      name = request.POST["name"]
      description = request.POST["description"]
      connection = request.POST["connection"] # slurm://192.168.0.34:82

      protocol, ip, port = connection.replace("//", "").split(":", 2)

      HardwareProfile(name=name, description=description, protocol=protocol, ip_addr=ip, port_addr=port).save()

    return redirect("hardware")

  # /hardware/remove with post
  
  @AccountView.require_login
  def delete_profile(request):
     
    if request.method == "POST":
      id = request.POST["hardware_id"]
      HardwareProfile.objects.filter(uuid=id).delete()

    return redirect("hardware")


  # /hardware/archive with post
  
  @AccountView.require_login
  def archive_profile(request):
    ...


  
