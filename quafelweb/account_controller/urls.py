
from django.urls import path
from account_controller import views

urlpatterns = [
    path('', views.AccountView.manage_accounts, name='account'),
    path('login/', views.AccountView.authenticate, name='login'),
    path('logout/', views.AccountView.logout, name='logout'),
    path('auth/', views.AccountView.authenticate_callback, name='auth_callback'),
    path('denied/', views.AccountView.denied, name='denied')
]