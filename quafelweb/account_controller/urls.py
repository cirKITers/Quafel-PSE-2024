
from django.urls import path
from account_controller import manager

urlpatterns = [
    path('', manager.AccountManager.index),
    path('auth/', manager.AccountManager.auth_view, name='auth'),
    path('denied/', manager.AccountManager.access_denied, name='denied')
]