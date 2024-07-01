"""
URL configuration for quafelweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
  
    path('', RedirectView.as_view(url='view', permanent=False), name='index'),
    path('view/', include('simulation_view.urls')),
    path('account/', include('account_controller.urls')),
    path('simulation/', include('simulation_controller.urls')),
    path('hardware/', include('hardware_controller.urls'))
]
