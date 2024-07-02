from django.http import HttpResponse
from django.shortcuts import render

import plotly.express as px
from random import randint
from simulation_data.simulation import SimulationEnv, HardwareProfile, SimulatorProfile
import pandas as pd

class SimulationView:

  @staticmethod
  def graph(data : pd.DataFrame) -> str:
    return px.line(data, labels=["Qubits", "Evaluations"]).to_html(full_html=False)

  def index(request):
    # Generate the plot
    # Pass the plot to the HTML template
    envs = [
      SimulationEnv(hardware=HardwareProfile(name='GPU-Cluster'), simulator=SimulatorProfile(name='Quiver', version='v0.17')),
      SimulationEnv(hardware=HardwareProfile(name='GPU-Cluster'), simulator=SimulatorProfile(name='Qalle', version='v0.17'))
    ]  

    df = pd.DataFrame(data={ env.simulator.name : [randint(0, 100) for _ in range(16)] for env in envs })

    graph = SimulationView.graph(df)

    context = { 
      'graph_div' : graph,
      'environments' : envs
    }

    return render(request, "simulation.html", context=context)
  
  def specific(request, qbit_start, qbit_end, depth_start, depth_end, evals_start, evals_end):
      ...


  def render_view(request, sim_envs : list[SimulationEnv], sim_confs : dict[str, list[int]]):
  
    context = { 'environments' : sim_envs }

    return render(request, 'simulation.html', context)
