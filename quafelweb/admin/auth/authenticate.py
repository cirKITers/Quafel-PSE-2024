import json
from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

CONF_URL = "https://oidc.scc.kit.edu/auth/realms/kit/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name='kitopenid',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


class MyBackend(BaseBackend):
  def authenticate(self, request : HttpRequest):
    return oauth.kitopenid.authorize_redirect(request, request.get_raw_uri())
  
  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None