from django.shortcuts import redirect, render

from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulationRun

import re as regex

# Create your views here.


class HardwareView:

    
    HARDWARE_ADDR_REGEX = r"^(.*?)://(.*?)(?::(\d+))?$"

    # /hardware

    @AccountView.require_login
    def manage_profiles(request):

        profiles = HardwareProfile.objects.all()

        if search := request.GET.get("search"):
            profiles = [profile for profile in profiles if search in profile.name]

        context = {"profiles": profiles}
        return render(request, "hardware.html", context=context)



    @AccountView.require_login
    def add_profile(request):

        name = request.POST.get("name")
        description = request.POST.get("description") or ""


        connection = request.POST.get("connection") or ""
        conn_match = regex.match(HardwareView.HARDWARE_ADDR_REGEX, connection)
        
        error_message = None
        if not name:
            error_message = "The specified name was empty"
        elif HardwareProfile.objects.filter(name=name).exists():
            error_message = "The specified name is already in use"
        elif not conn_match:
            error_message = "A connection has to be in the following format <protocol>://<remote>:<port>"
                
        if error_message: 
            return render(request, "info.html", context={
                "info_type": "error",
                "header": "Invalid Request",
                "message": error_message,
                "url_link" : "hardware"
            })

        protocol, ip_addr, port_addr = conn_match.groups()
        
        hp = HardwareProfile(
            name=name,
            description=description,
            protocol=protocol,
            ip_addr=ip_addr,
            port_addr = port_addr or 22
        )

        hp.save()

        return redirect("hardware")


    # /hardware/remove with post

    @AccountView.require_login
    def delete_profile(request):

        id = request.POST.get("id")

        if not id: return redirect("hardware")

        simulation_runs = SimulationRun.objects.filter(hardware=id)
        
        if len(simulation_runs) != 0:
            return render(request, "info.html", context={
                "info_type": "info",
                "header": "Deleting Simulation Data",
                "message": f"Through this action {len(simulation_runs)} simulation runs will be deleted",
                "url_link" : "delete_confirm"
            })

        HardwareProfile.objects.filter(uuid=id).delete()

        return redirect("hardware")

    @AccountView.require_login
    def delete_runs(request):
        
        id = request.POST.get("id")
        if not id: return redirect("hardware")

        SimulationRun.objects.filter(hardware=id).delete()
        HardwareProfile.objects.filter(uuid=id).delete()

        return redirect("hardware")


    @AccountView.require_login
    def configure_profile(request):

        if id := request.GET.get("id"):

            profile = HardwareProfile.objects.filter(uuid=id)

            if not profile.exists():
                redirect("hardware")

            context = {"hardware": profile.get()}

            return render(request, "configuration.html", context=context)

        return redirect("hardware")

    @AccountView.require_login
    def submit_change(request):
        id = request.POST.get("id")
        name = request.POST.get("name")
        description = request.POST.get("description") or ""
        connection = request.POST.get("connection") or ""
        needs_totp = request.POST.get("totp") == "on"

        conn_match = regex.match(HardwareView.HARDWARE_ADDR_REGEX, connection)


        if not id: # This is a malicious actor 
            return redirect("hardware")
        
        
        profile = HardwareProfile.objects.filter(uuid=id)
        if not profile.exists(): # also malicious
            return redirect("hardware")

        error_message = None
        if not name:
            error_message = "The specified name was empty"
        elif not conn_match:
            error_message = "A connection has to be in the following format <protocol>://<remote>(:<port>)"
                
        if error_message: 
            return render(request, "info.html", context={
                "info_type": "error",
                "header": "Invalid Request",
                "message": error_message,
                "url_link" : "configure_hardware"
            })
        
        protocol, ip_addr, port_addr = conn_match.groups()

        profile.update(
            name=name,
            description=description,
            protocol=protocol,
            ip_addr=ip_addr,
            port_addr=port_addr or 22,
            needs_totp=needs_totp,
        )

        return redirect("hardware")
