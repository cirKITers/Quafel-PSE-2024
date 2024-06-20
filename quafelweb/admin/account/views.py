from django.http import HttpResponse
from django.shortcuts import render

from admin.account import authenticate
# Create your views here.

class AccountManager():
  

  def index(req):
    return HttpResponse("Account page")
