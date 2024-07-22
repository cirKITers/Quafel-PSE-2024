
from django.urls import path

from simulation_view.views import SimulationView

urlpatterns = [
    path('', SimulationView.index, name='view'),
]
