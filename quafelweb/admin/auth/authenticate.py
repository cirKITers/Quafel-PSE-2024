import json
from django.urls import reverse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth

CONF_URL = "https://oidc.scc.kit.edu/auth/realms/kit/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name='kitopenid',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
