from django.shortcuts import redirect, render

from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulationRun

import re as regex

# Create your views here.

class HardwareView:

    # /hardware

    @AccountView.require_login
    def manage_profiles(request):

        profiles = HardwareProfile.objects.all()

        if search := request.GET.get("search"):
            profiles = [profile for profile in profiles if search in profile.name]

        context = {"hardware_profiles": profiles}
        return render(request, "hardware.html", context=context)

    # /hardware/add with post

    @AccountView.require_login
    def add_profile(request):
        id = request.POST.get("hardware_id")
        name = request.POST.get("hardware_name")
        description = request.POST.get("hardware_description")
        connection = request.POST.get("hardware_connection")

        addr_match = r"^([a-zA-Z]+)://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$"

        if id and name and description and regex.match(addr_match, connection):

            protocol, ip_addr, port_addr = connection.replace("//", "").split(":", 2)
            HardwareProfile(
                name=name,
                description=description,
                protocol=protocol,
                ip_addr=ip_addr,
                port_addr=port_addr,
            ).save()

        return redirect("hardware")

    # /hardware/remove with post

    @AccountView.require_login
    def delete_profile(request):

        if id := request.POST.get("hardware_id"):

            SimulationRun.objects.filter(hardware=id).delete()
            HardwareProfile.objects.filter(uuid=id).delete()

        return redirect("hardware")

    @AccountView.require_login
    def configure_profile(request):

        if id := request.GET.get("hardware_id"):

            profile = HardwareProfile.objects.filter(uuid=id)

            if not profile.exists():
                redirect("hardware")

            context = {"hardware": profile.get()}

            return render(request, "configuration.html", context=context)

        return redirect("hardware")

    @AccountView.require_login
    def submit_change(request):
        id = request.POST.get("hardware_id")
        name = request.POST.get("hardware_name")
        description = request.POST.get("hardware_description")
        connection = request.POST.get("hardware_connection")

        addr_match = r"^([a-zA-Z]+)://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$"

        if id and name and description and regex.match(addr_match, connection):

            protocol, ip_addr, port_addr = connection.replace("//", "").split(":", 2)

            profile = HardwareProfile.objects.filter(uuid=id)

            needs_totp = request.POST.get("hardware_totp") == "on"

            if not profile.exists():
                raise RuntimeError("Invalid hardware profile requested")  # TODO

            profile.update(
                name=name,
                description=description,
                protocol=protocol,
                ip_addr=ip_addr,
                port_addr=port_addr,
                needs_totp=needs_totp,
            )
        print(needs_totp)

        return redirect("hardware")
