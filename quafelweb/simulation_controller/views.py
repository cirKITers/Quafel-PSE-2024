import functools
import itertools
import json
import math
from operator import mul
import random
from typing import TypedDict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulatorProfile, SimulationRun
from simulation_data.simulation import SimulationEnv



class SimulationRequestView:


  @AccountView.require_login
  def selection(request):

    context = dict()

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
  def submit_request(request):

    
    if request.method == "POST":
      qubits_min = request.POST["qubits_min"]
      qubits_max = request.POST["qubits_max"]
      qubits_interval = request.POST["qubits_increment"]
      qubits_interval_type = request.POST["qubits_increment_type"]

      ...


      selected_envs = [tag.split("::", 2)[1:3] for tag in request.POST if tag.startswith("ENV")]
      selected_envs = [(HardwareProfile.objects.get(uuid=uuid), SimulatorProfile.objects.get(name=name)) for uuid, name in selected_envs]


      auth_data = dict()
      for data, value in request.POST.items():
        if not any(data.startswith(tag) for tag in ["NAME", "PASSWORD", "TOTP"]):
          continue
        tag, hp_uuid = data.split("::", 1)
        hp = HardwareProfile.objects.get(uuid=hp_uuid)
        auth_data[hp] = { **auth_data.get(hp, dict()), tag : value } 
      
      print(auth_data)


    return HttpResponse(dict(request.POST))


  @AccountView.require_login
  def claim_results(request):
    ...