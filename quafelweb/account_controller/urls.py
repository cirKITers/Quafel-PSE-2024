from django.urls import path

from account_controller import views

urlpatterns = [
    path("", views.AccountView.manage_accounts, name="account"),
    path("add/", views.AccountView.add_admin),
    path("delete/", views.AccountView.remove_admin),
    path("login/", views.AccountView.authenticate, name="login"),
    path("logout/", views.AccountView.logout, name="logout"),
    path("auth/", views.AccountView.authenticate_callback, name="auth_callback"),
    path("denied/", views.AccountView.denied, name="denied"),
]
