
from django.urls import path, include
from admin.account import manager

urlpatterns = [
    path('account/', include("admin.account.urls")),
]