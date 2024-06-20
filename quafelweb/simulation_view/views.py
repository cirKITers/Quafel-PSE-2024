
# Create your views here.



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import plotly.express as px
from random import randint

class SimulationView:

    @staticmethod
    def graph(x_label : str, y_label : str, x_data : list, y_data : list) -> str:
      return px.line(x=x_data, y=y_data, labels=[x_label, y_label]).to_html(full_html=False)

    def index(request):
        # Generate the plot
        # Pass the plot to the HTML template
        context = { 'graph_div' : SimulationView.graph("Y", "X", list(range(16)), [randint(0, 100) for _ in range(16)])}
        return render(request, 'index.html', context)
    
    def specific(request, qbit_start, qbit_end, depth_start, depth_end, evals_start, evals_end):
        ...