
from django.urls import path
from admin.account import views

urlpatterns = [
    path('account/', views.AccountManager.index),
]