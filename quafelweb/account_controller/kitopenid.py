from abc import ABC, abstractmethod
from django.dispatch import receiver
from authlib.integrations.django_client import OAuth
from authlib.integrations.django_client import token_update
from django.shortcuts import redirect
from account_controller import authenticate

class KITOpenIDAuth(authenticate.BaseAuthenticator):

  CONF_URL = "https://oidc.scc.kit.edu/auth/realms/kit/.well-known/openid-configuration"

  def __init__(self) -> None:
    self.oauth = OAuth()
    self.oauth.register(
        name='kitopenid',
        server_metadata_url=KITOpenIDAuth.CONF_URL,
        client_id = "quafelweb-pse2024-scc-kit-edu",
        client_secret ="gsIpGaFHNPK6e4cfqDLVkLbSjuzGBi8n",
        client_kwargs={'scope': 'openid email'}
    )

  def authenticate(self, request, auth_callback):
    request.session["last_request"] = request.build_absolute_uri()
    return self.oauth.kitopenid.authorize_redirect(request, auth_callback)

  def authenticate_callback(self, request):
    token = self.oauth.kitopenid.authorize_access_token(request)
    request.session['user_info'] = token['userinfo']
    return redirect(request.session.get("last_request", '/'))

  def get_identifier(self, request):
    if not self.is_logged_in(request): return None
    return request.session.get('user_info')['email']
  
  def is_logged_in(self, request):
    return 'user_info' in request.session
  
    
  @receiver(token_update)
  def on_token_update(self, sender, name, token, refresh_token=None, access_token=None, **kwargs):
      if refresh_token:
        item = self.oauth.find(name=name, refresh_token=refresh_token)
      elif access_token:
          item = self.oauth.find(name=name, access_token=access_token)
      else:
          return

      # update old token
      item.access_token = token['access_token']
      item.refresh_token = token.get('refresh_token')
      item.expires_at = token['expires_at']
      item.save()


authenticate.BaseAuthenticator.RegisterInstance("kitopenid", KITOpenIDAuth())
