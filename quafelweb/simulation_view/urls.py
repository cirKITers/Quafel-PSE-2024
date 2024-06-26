
from django.urls import include, path

from simulation_view.views import SimulationView

urlpatterns = [
    path('', SimulationView.index, name='view'),
    path('<int:qbit_start>:<int:qbit_end>:<int:depth_start>:<int:depth_end>:<int:evals_start>:<int:evals_end>/', SimulationView.specific, name='view')
]
