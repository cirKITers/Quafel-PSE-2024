
from django.urls import path
from account_controller import views

urlpatterns = [
    path('', views.AccountView.manage_accounts),
    path('auth/', views.AccountView.authenticate_callback, name='auth_callback'),
    path('denied/', views.AccountView.denied, name='denied')
]