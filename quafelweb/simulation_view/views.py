import itertools

from django.shortcuts import render

from simulation_data.models import SimulatorProfile, SimulationRun
from simulation_data.simulation import SimulationEnv, HardwareProfile


class SimulationView:

  @staticmethod
  def index(request):

    simulators =        [sp for sp in SimulatorProfile.objects.all()  if sp.name == (request.GET.get("simulator_filter") or sp.name)]
    hardware_profiles = [hp for hp in HardwareProfile.objects.all()   if hp.name == (request.GET.get("hardware_filter") or hp.name)]
    
    # Produce all possible environments
    envs = [SimulationEnv(hp, sp) for hp, sp in itertools.product(hardware_profiles, simulators)]


    # Existing envs
    hps = set(SimulationRun.objects.values_list("hardware", flat=True).distinct())
    sps = set(SimulationRun.objects.values_list("simulator", flat=True).distinct())

    # Filter for existing envs
    envs = [env for env in envs if env.hardware.uuid in hps and env.simulator.name in sps]

    # Simulation configuration
    values = {
    "qubit" : set(SimulationRun.objects.values_list("qubits", flat=True).distinct()) or { 0 },
    "depth" : set(SimulationRun.objects.values_list("depth", flat=True).distinct()) or { 0 },
    "shot" : set(SimulationRun.objects.values_list("shots", flat=True).distinct()) or { 0 },
    }
    
    # retrieve the selected range
    selected_range = request.GET.get("selected_conf") or "qubit"

    def get_range(name : str):
      max_v = max(int(request.GET.get(name + "_max") or 0), min(values[name]))
      min_v = min(int(request.GET.get(name + "_min") or 100000000), max(values[name]))
      
      range_v = set(v for v in values[name] if v in range(min_v, max_v + 1)) if selected_range == name else { min_v } 
      return range_v

    # Get all runs existed
    env_to_run_map = [
      (env, SimulationRun.objects.filter(
        simulator=env.simulator.name, 
        hardware=env.hardware.uuid,
        qubits__in=get_range("qubit"),
        depth__in=get_range("depth"),
        shots__in=get_range("shot"),
      )) for env in envs
    ]




    graph_data = {
      "data" : [
        {
          "label" : env.hardware.name + " " + env.simulator.name,
          "data" :  [run.duration_avg for run in runs]
        }
        for env, runs in env_to_run_map
      ],
    }

    
    graph_data['labels'] = list(sorted(get_range(selected_range)))

    context = {
      'environments' : envs,
      'hardware_profiles' : HardwareProfile.objects.all(),
      'simulator_profiles' : SimulatorProfile.objects.all(),
      'graph_data' : graph_data,
      
      'qubits_values' : list(sorted(values["qubit"])),
      'qubit_max' : max(values["qubit"]),

      'depth_values' : list(sorted(values["depth"])),
      'depth_max' : max(values["depth"]),

      'shot_values' : list(sorted(values["shot"])),
      'shot_max' : max(values["shot"]),
    }

    return render(request, "simulation.html", context=context)
