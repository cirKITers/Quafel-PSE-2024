from django.urls import path
import hardware_controller.views as views

urlpatterns = [
  path('', views.HardwareView.manage_profiles, name='hardware'),
  path('add/', views.HardwareView.add_profile),
]