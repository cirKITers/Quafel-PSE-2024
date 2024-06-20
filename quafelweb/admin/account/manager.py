from typing import Self
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

import admin.account.auth.kitopenid # This needs to be here
from admin.account import authenticate
# Create your views here.

class AccountManager():

  _AUTH : authenticate.BaseAuthenticator = authenticate.BaseAuthenticator.GetInstance("kitopenid") 


  @staticmethod
  def require_login(fn):
    
    def _deco(req):
      if not AccountManager._AUTH.is_logged_in(req):
        return AccountManager._AUTH.authenticate(req, req.build_absolute_uri(reverse('auth')))
      # TODO: verify user is in the admin group
      return fn(req)
    
    return _deco

  @require_login
  def index(req):

    ident = AccountManager._AUTH.get_identifier(req)
    return HttpResponse("Your email is " + req.session['user_ident'])
    

  
  def auth_view(req):
    return AccountManager._AUTH.authenticate_callback(req)