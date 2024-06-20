
from django.urls import path, include
urlpatterns = [
    path('account/', include("admin.account.urls")),
]