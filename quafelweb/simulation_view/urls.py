
from django.urls import include, path
from django.views.generic.base import RedirectView
from simulation_view.views import SimulationView

urlpatterns = [
    path('', RedirectView.as_view(url='view', permanent=False), name='index'),
    path('view/', SimulationView.index, name='view'),
    path('view/<int:qbit_start>:<int:qbit_end>:<int:depth_start>:<int:depth_end>:<int:evals_start>:<int:evals_end>/', SimulationView.specific, name='view')
]
