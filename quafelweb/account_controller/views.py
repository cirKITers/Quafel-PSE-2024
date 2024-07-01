from django.http import HttpRequest, HttpResponse
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect
from django.urls import reverse
from quafelweb.settings import OPENID_CONF_URL, OPENID_SECRET, OPENID_CLIENT_ID, OPENID_CLIENT_IDENT

OAUTH = OAuth()
OAUTH.register(
  name='openid',
  server_metadata_url=OPENID_CONF_URL,
  client_id = OPENID_CLIENT_ID,
  client_secret = OPENID_SECRET,
  client_kwargs={'scope': 'openid email'}
)


class AccountView:

  @staticmethod
  def manage_accounts(request) -> HttpResponse:
    if AccountView.is_logged_in(request):
      return HttpResponse(AccountView.get_identifier(request))
    
    return AccountView.authenticate(request) 
  
  @staticmethod
  def add_admin(request) -> HttpResponse:
    ...

  @staticmethod
  def remove_admin(request) -> HttpResponse:
    ...

  @staticmethod
  def authenticate(request : HttpRequest) -> HttpResponse:
    request.session["last_request"] = request.build_absolute_uri()
    return OAUTH.openid.authorize_redirect(request, request.build_absolute_uri(reverse('auth_callback')))


  @staticmethod
  def authenticate_callback(request : HttpRequest) -> HttpResponse:
    token = OAUTH.openid.authorize_access_token(request)
    request.session['user_info'] = token['userinfo']
    request.session['logged_in'] = True
    return redirect(request.session.get("last_request", '/'))
  
  @staticmethod
  def get_identifier(request : HttpRequest) -> str:
    if not AccountView.is_logged_in(request): return None
    return request.session.get('user_info')[OPENID_CLIENT_IDENT]

  @staticmethod
  def is_logged_in(request : HttpRequest) -> bool:
    return request.session.get('logged_in', False)
  
  @staticmethod
  def denied(request : HttpRequest):
    ...