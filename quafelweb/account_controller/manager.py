from typing import Self
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

import account_controller.kitopenid # This needs to be here
from account_controller import authenticate
from account_controller.models import AdminAccount
# Create your views here.

class AccountManager():

  _AUTH : authenticate.BaseAuthenticator = authenticate.BaseAuthenticator.GetInstance("kitopenid") 


  @staticmethod
  def require_login(fn):
    
    def _deco(req):
      if not AccountManager._AUTH.is_logged_in(req):
        return AccountManager._AUTH.authenticate(req, req.build_absolute_uri(reverse('auth')))
      ident = AccountManager._AUTH.get_identifier(req)
      if AdminAccount.objects.contains(AdminAccount(ident)):
        return redirect('denied')
      return fn(req)
    
    return _deco
  
  def access_denied(req):
    return HttpResponse("Access denied")

  @require_login
  def index(req):
    # if openid causes any problems use localhost instead of 127.0.0.1 // localhost is allowed as an return path

    ident = AccountManager._AUTH.get_identifier(req)
    return HttpResponse("Your email is " + ident)
    
    
  def auth_view(req):
    return AccountManager._AUTH.authenticate_callback(req)