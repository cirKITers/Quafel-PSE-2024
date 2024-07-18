from django.shortcuts import render

from simulation_data.simulation import SimulationEnv, HardwareProfile
from simulation_data.models import SimulatorProfile, SimulationRun
import itertools




class SimulationView:

  @staticmethod
  def index(request):

    simulators =        [sp for sp in SimulatorProfile.objects.all() if sp.name == (request.GET.get("simulator_filter") or sp.name)]
    hardware_profiles = [hp for hp in HardwareProfile.objects.all()  if hp.name == (request.GET.get("hardware_filter") or hp.name)]
    
    # Existing envs
    hps = set(SimulationRun.objects.values_list("hardware", flat=True).distinct())
    sps = set(SimulationRun.objects.values_list("simulator", flat=True).distinct())

    # Produce all possible environments and apply the filter at the same time
    envs = [SimulationEnv(hp, sp) for hp, sp in itertools.product(hardware_profiles, simulators) if hp.uuid in hps and sp.name in sps ]

    
    context = {
      'environments': envs,
      'hardware_profiles' : HardwareProfile.objects.all(),
      'simulator_profiles' : SimulatorProfile.objects.all(),
    }

    # Simulation configuration
    values = {
      "qubit" : set(SimulationRun.objects.values_list("qubits", flat=True).distinct()) or { 0 },
      "depth" : set(SimulationRun.objects.values_list("depth", flat=True).distinct()) or { 0 },
      "shot" :  set(SimulationRun.objects.values_list("shots", flat=True).distinct()) or { 0 },
    }
    
    selected_range = request.GET.get("selected_conf") or "qubit" # selected range 

    for name in { "qubit", "depth", "shot"}:
      max_v = min(int(request.GET.get(name + "_max") or max(values[name])), max(values[name]))
      min_v = max(int(request.GET.get(name + "_min") or min(values[name])), min(values[name]))
      
      range_v = set(v for v in values[name] if v in range(min_v, max_v + 1)) if selected_range == name else { max_v } 

      context[name + "_values"] = list(sorted(values[name]))
      context[name + "_range"] = range_v
      context[name + "_min"] = min_v
      context[name + "_max"] = max_v
      
    

    # Get all runs existed
    env_to_run_map = [
      (env, SimulationRun.objects.filter(
        simulator=env.simulator.name, 
        hardware=env.hardware.uuid,
        qubits__in=context["qubit_range"],
        depth__in= context["depth_range"],
        shots__in= context["shot_range"],
      )) for env in envs
    ]

    # graph data to save in json for chart.js
    context['graph_data'] = {
      "data" : [
        {
          "label" : env.hardware.name + " " + env.simulator.name,
          "data" :  [run.duration_avg for run in runs]
        }
        for env, runs in env_to_run_map
      ],
      'labels' : list(sorted(context[selected_range + "_range"])),
      'x_axis' : selected_range.capitalize(),
      'y_axis' : "Average duration",
      'scale_type' : 'logarithmic'
    }
      
    return render(request, "simulation.html", context=context)
