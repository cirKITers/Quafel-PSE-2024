from django.http import HttpResponse
from django.shortcuts import render

import plotly.express as px
from random import randint
from simulation_data.simulation import SimulationEnv, HardwareProfile
from simulation_data.models import SimulatorProfile, SimulationRun
import pandas as pd
import itertools




class SimulationView:

  @staticmethod
  def graph(data : pd.DataFrame) -> str:
    return px.line(data, labels=["Qubits", "Evaluations"]).to_html(full_html=False)

  @staticmethod
  def index(request):
    # Generate the plot
    # Pass the plot to the HTML template
    hardware_profiles = [hp for hp in HardwareProfile.objects.all() if hp.name == (request.GET.get("hardware_filter") or hp.name)]
    simulators = [sp for sp in SimulatorProfile.objects.all() if sp.name == (request.GET.get("simulator_filter") or sp.name)]
    
    # Produce all possible environments
    envs = [SimulationEnv(hp, sp) for hp, sp in itertools.product(hardware_profiles, simulators)]


    # Existing envs
    hps = set(SimulationRun.objects.values_list("hardware_profile", flat=True).distinct())
    sps = set(SimulationRun.objects.values_list("simulator_name", flat=True).distinct())

    # Filter for existing envs
    envs = [env for env in envs if env.hardware.uuid in hps and env.simulator.id in sps]

    
    max_qbits = 6

    # Get all runs existed
    env_to_run_map = [
      (env, SimulationRun.objects.filter(
        simulator_name=env.simulator.id, 
        hardware_profile=env.hardware.uuid,
        qbits__in=set(range(1, max_qbits + 1))
      )) for env in envs
    ]

    data = pd.DataFrame()
    
    for env, runs in env_to_run_map: 
      results = [0] * max_qbits
      for run in runs:
        results[run.qbits - 1] = run.durations

      data[env.hardware.name + " " + env.simulator.name] = results




    context = { 
      'environments' : envs,
      'hardware_profiles' : HardwareProfile.objects.all(),
      'simulator_profiles' : SimulatorProfile.objects.all(),
      'graph' : SimulationView.graph(data)
    }

    return render(request, "simulation.html", context=context)
