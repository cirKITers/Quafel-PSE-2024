import itertools
import json
import math
import random
from email.policy import default

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from quafel_simulators.base.simulation_request import IncrementType
from quafel_simulators.quafelsubmitter import QuafelSubmitter
from simulation_controller.util.simulation_request import SimulationRequestRange, SimulationRequest
from simulation_controller.util.simulation_request_helper import get_missing_runs_as_ranges
from simulation_data.models import SimulatorProfile, SimulationRun


class SimulationRequestView:

    @AccountView.require_login
    def selection(request):
        context = dict()
        # Create all possible envs

        for conf in ["qubits", "depth", "shots"]:
            conf_range = set(SimulationRun.objects.values_list(conf, flat=True)) or {0}

            context[conf + "_min"] = min_v = int(request.GET.get(conf + "_min") or min(conf_range))
            context[conf + "_max"] = max_v = int(request.GET.get(conf + "_max") or max(conf_range))

            context[conf + "_increment"] = increment = max(int(request.GET.get(conf + "_increment") or 1), 1)

            context[conf + "_increment_type"] = inc_type = request.GET.get(conf + "_increment_type") or "linear"

            if inc_type == "linear" or increment == 1:
                context[conf + "_values"] = list(range(min_v, max_v + 1, increment))
            else:
                context[conf + "_values"] = [int(increment ** i) for i in range(int(math.log(min_v, increment)),
                                                                                int(math.log(max_v, increment) + 1))]
            print(context[conf + "_values"])

        conf_filter = {
            "qubits__in": context["qubits_values"],
            "depth__in": context["depth_values"],
            "shots__in": context["shots_values"],
        }

      if inc_type == "linear" or increment == 1:
        context[conf + "_values"] = list(range(min_v, max_v + 1, increment))
      else:
        context[conf + "_values"] = [int(increment ** i) for i in range(int(math.log(min_v, increment)), int(math.log(max_v, increment) + 1))]  



    conf_filter = {
      "qubits__in" : context["qubits_values"],
      "depth__in" : context["depth_values"],
      "shots__in" : context["shots_values"],
    }
    
    # get selected envs
    envs = list()
    for hp, sp in itertools.product(HardwareProfile.objects.all(), SimulatorProfile.objects.all()):
      if hfilter := request.GET.get("hardware_filter"):
        if hfilter != hp.name: continue

      if sfilter := request.GET.get("simulator_filter"):
        if sfilter != sp.name: continue
      
      name = f"ENV::{hp.uuid}::{sp.name}" 
               
      finished_runs = SimulationRun.objects.filter(hardware=hp.uuid, simulator=sp.name, **conf_filter).count()
      selected = bool(request.GET.get(name, False))

      envs.append([hp, sp, finished_runs, name, selected])
    
    # (un)check all functionality 
    if "check_all" in request.GET:
      value = not all(env[4] for env in envs)
      for env in envs:
        env[4] = value


    # Sort after hardware then simulator
    envs.sort(key=lambda x: x[1].name)
    envs.sort(key=lambda x: x[0].name) 

    context["envs"] = envs
    context["max_amount"] = math.prod(len(context[name + "_values"]) for name in ["qubits", "depth", "shots"])

    context["hardware_profiles"] = HardwareProfile.objects.all()
    context["simulator_profiles"] = SimulatorProfile.objects.all()

    context["selected_hardware"] = set(env[0] for env in envs if env[4])

    return render(request, "simulation.html", context=context)

    @AccountView.require_login
    def select_environments(request):
        data = json.loads(request.body)

        hwps = set(data.get('hwps'))
        hwps_requirements = []
        for hwp in hwps:
            hwp_entry = {}
            # TODO: Check if password or ttop is required

            if random.choice([True, False]):
                hwp_entry['password_required'] = True

            if random.choice([True, False]):
                hwp_entry['totp_required'] = True

            # hwp_entry != {}
            if hwp_entry:
                hwp_entry['hwp'] = hwp
                hwps_requirements.append(hwp_entry)
            else:
                continue

        return JsonResponse({'hwps_requirements': hwps_requirements})

    @AccountView.require_login
    def submit_request(request):
        if request.method == "POST":
            qubits_min = int(request.POST["qubits_min"])
            qubits_max = int(request.POST["qubits_max"])
            qubits_interval = int(request.POST["qubits_increment"])
            qubits_interval_type = IncrementType.get(request.POST["qubits_increment_type"])

            depth_min = int(request.POST["depth_min"])
            depth_max = int(request.POST["depth_max"])
            depth_interval = int(request.POST["depth_increment"])
            depth_interval_type = IncrementType.get(request.POST["depth_increment_type"])

            shots_min = int(request.POST["shots_min"])
            shots_max = int(request.POST["shots_max"])
            shots_interval = int(request.POST["shots_increment"])
            shots_interval_type = IncrementType.get(request.POST["shots_increment_type"])

            envs = [tag.split("::", 2)[1:3] for tag in request.POST if tag.startswith("ENV")]
            selected_envs = [(HardwareProfile.objects.get(uuid=hardware_uuid),
                              SimulatorProfile.objects.get(name=simulator_name))
                             for hardware_uuid, simulator_name in envs]

            auth_data = dict()
            for data, value in request.POST.items():
                if not any(data.startswith(tag) for tag in ["NAME", "PASSWORD", "TOTP"]):
                    continue
                tag, uuid = data.split("::", 1)
                hp = HardwareProfile.objects.get(name=uuid)
                auth_data[hp] = {**auth_data.get(hp, dict()), tag: value}

            range = SimulationRequestRange(
                qubits_min, qubits_max, qubits_interval, qubits_interval_type,
                shots_min, shots_max, shots_interval, shots_interval_type,
                depth_min, depth_max, depth_interval, depth_interval_type,
            )

            for hardware_profile, simulator_profile in selected_envs:
                ranges_for_submission = get_missing_runs_as_ranges(range, hardware_profile, simulator_profile)

                username = auth_data[hardware_profile].get("NAME")
                password = auth_data[hardware_profile].get("PASSWORD")
                totp = auth_data[hardware_profile].get("TOTP")
                if totp == "":
                    totp = None

                for r in ranges_for_submission:
                    simulation_request = SimulationRequest(r, hardware_profile, simulator_profile, username, password, totp)
                    QuafelSubmitter().submit(simulation_request)

        return HttpResponse(request, "Hello World")

@AccountView.require_login
def claim_results(request):
    ...
