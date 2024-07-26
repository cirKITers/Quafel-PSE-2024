import itertools

from django.shortcuts import render

from simulation_data.models import SimulatorProfile, SimulationRun
from simulation_data.simulation import SimulationEnv, HardwareProfile


class SimulationView:

  @staticmethod
  def index(request):

    # Get all selected simulator and hardware profiles
    simulators =        [sp for sp in SimulatorProfile.objects.all() if sp.name == (request.GET.get("simulator_filter") or sp.name)]
    hardware_profiles = [hp for hp in HardwareProfile.objects.all()  if hp.name == (request.GET.get("hardware_filter") or hp.name)]
    
    # Get existing envs
    hps = set(SimulationRun.objects.values_list("hardware", flat=True))
    sps = set(SimulationRun.objects.values_list("simulator", flat=True))

    # Produce all available environments
    envs = [SimulationEnv(hp, sp) for hp, sp in itertools.product(hardware_profiles, simulators) if hp.uuid in hps and sp.name in sps]
    
    # this context will be passed to the template
    context = {
      "environments": envs,
      "hardware_profiles" : HardwareProfile.objects.all(),
      "simulator_profiles" : SimulatorProfile.objects.all(),
    }

    # Get all possible configurations from existing runs in the database
    values = {
      "qubits" : set(SimulationRun.objects.values_list("qubits", flat=True)) or { 0 },
      "depth" : set(SimulationRun.objects.values_list("depth", flat=True)) or { 0 },
      "shots" :  set(SimulationRun.objects.values_list("shots", flat=True)) or { 0 },
    }
    
  
    selected_range = request.GET.get("selected_conf") or "qubits" 

    for name in ["qubits", "depth", "shots"]:
      max_v = min(int(request.GET.get(name + "_max") or max(values[name])), max(values[name]))
      min_v = max(int(request.GET.get(name + "_min") or min(values[name])), min(values[name]))
      
      range_v = set(v for v in values[name] if v in range(min_v, max_v + 1)) if selected_range == name else { max_v } 

      context[name + "_values"] = list(sorted(values[name]))
      context[name + "_range"] = range_v
      context[name + "_min"] = min_v
      context[name + "_max"] = max_v

    conf_filter = {
      "qubits__gte" : min(context["qubits_range"]),
      "qubits__lte" : max(context["qubits_range"]),

      "depth__gte" : min(context["depth_range"]),
      "depth__lte" : max(context["depth_range"]),
      
      "shots__gte" : min(context["shots_range"]),
      "shots__lte" : max(context["shots_range"]),
    }
      
    # Create a data structure for chart.js
    data = list()
    for env in envs:
      name = env.hardware.name + " " + env.simulator.name
      runs = SimulationRun.objects.filter(
          simulator=env.simulator.name, 
          hardware=env.hardware.uuid, 
          **conf_filter
      )

      data.append({
        "label" : name, 
        "data" : [run.duration_avg for run in runs]
      })
     

    context["graph_data"] = {
      "data" : data,
      "labels" : list(sorted(context[selected_range + "_range"])),
      "x_axis" : selected_range.capitalize(),
      "y_axis" : "Average duration",
      "scale_type" : "logarithmic"
    }
      
    return render(request, "simulation_view.html", context=context)
