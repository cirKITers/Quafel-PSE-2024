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

    # /hardware/add with post

    @AccountView.require_login
    def add_profile(request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        connection = request.POST.get("connection") or ""


        conn_match = regex.match(HardwareView.HARDWARE_ADDR_REGEX, connection)

        protocol, ip_addr, port_addr = conn_match.groups()
        
        if name and description and protocol and ip_addr:

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

        if id := request.POST.get("id"):

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
        description = request.POST.get("description")
        connection = request.POST.get("connection") or ""
        needs_totp = request.POST.get("totp") == "on"

        conn_match = regex.match(HardwareView.HARDWARE_ADDR_REGEX, connection)

        protocol, ip_addr, port_addr = conn_match.groups()
        
        if id and name and description and protocol and ip_addr:

            profile = HardwareProfile.objects.filter(uuid=id)


            if not profile.exists():
                raise RuntimeError("Invalid hardware profile requested")  # TODO

            profile.update(
                name=name,
                description=description,
                protocol=protocol,
                ip_addr=ip_addr,
                port_addr=port_addr or 22,
                needs_totp=needs_totp,
            )

        return redirect("hardware")
