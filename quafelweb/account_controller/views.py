

from django.http import HttpResponse


class AccountView:

  def manage_accounts(request) -> HttpResponse:
    ...

  def add_admin(request) -> HttpResponse:
    ...

  def remove_admin(request) -> HttpResponse:
    ...

  def authenticate(request) -> HttpResponse:
    ...

  def authenticate_callback(requests) -> HttpResponse:
    ...
  
  def get_identifier(request) -> str:
    ...

  def is_logged_in(request) -> bool:
    ...