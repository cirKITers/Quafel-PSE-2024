import itertools
import json
import math
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulatorProfile, SimulationRun


class SimulationRequestView:


  @AccountView.require_login
  def default(request):

    context = dict()
    # Create all possible envs

    for conf in ["qubits", "depth", "shots"]:
      conf_range = set(SimulationRun.objects.values_list(conf, flat=True)) or { 0 }

      context[conf + "_min"] = min_v = int(request.GET.get(conf + "_min") or min(conf_range))
      context[conf + "_max"] = max_v = int(request.GET.get(conf + "_max") or max(conf_range))

      context[conf + "_increment"] = increment = max(int(request.GET.get(conf + "_increment") or 1), 1)
      
      context[conf + "_increment_type"] = inc_type = request.GET.get(conf + "_increment_type") or "linear"

      if inc_type == "linear" or increment == 1:
        context[conf + "_values"] = list(range(min_v, max_v + 1, increment))
      else:
        context[conf + "_values"] = [int(increment ** i) for i in range(int(math.log(min_v, increment)), int(math.log(max_v, increment) + 1))]  
      print(context[conf + "_values"])

    conf_filter = {
      "qubits__in" : context["qubits_values"],
      "depth__in" : context["depth_values"],
      "shots__in" : context["shots_values"],
    }

    
    envs = list()
    for hp, sp in itertools.product(HardwareProfile.objects.all(), SimulatorProfile.objects.all()):
      name = f"ENV::{hp.uuid}::{sp.name}" 
               
      finished_runs = SimulationRun.objects.filter(hardware=hp.uuid, simulator=sp.name, **conf_filter).count()
      selected = bool(request.GET.get(name, False)) if not "check_all" in request.GET else True

      envs.append((hp, sp, finished_runs, name, selected))
    
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
    
    print(request.POST)
    return HttpResponse(request, "Hello World")


  @AccountView.require_login
  def claim_results(request):
    ...
