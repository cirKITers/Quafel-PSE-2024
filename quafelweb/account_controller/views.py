from typing import Callable, Optional

from authlib.integrations.django_client import OAuth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from quafelweb.settings import (
    OPENID_CONF_URL,
    OPENID_SECRET,
    OPENID_CLIENT_ID,
    OPENID_CLIENT_IDENT,
)
from account_controller.models import AdminAccount

OAUTH = OAuth()
OAUTH.register(
    name="openid",
    server_metadata_url=OPENID_CONF_URL,
    client_id=OPENID_CLIENT_ID,
    client_secret=OPENID_SECRET,
    client_kwargs={"scope": "openid email"},
)


class AccountView:

    @staticmethod
    def require_login(view: Callable) -> Callable:

        def _decorator(request: HttpResponse):
            if AccountView.is_logged_in(request):
                return view(request)
            return AccountView.authenticate(request)

        return _decorator

    @staticmethod
    @require_login
    def manage_accounts(request: HttpRequest) -> HttpResponse:
        accounts = AdminAccount.objects.all()

        if search := request.GET.get("search"):
            accounts = [acc for acc in accounts if search in acc.identifier]

        return render(request, "account.html", context={"accounts": accounts })

    @staticmethod
    @require_login
    def add_admin(request) -> HttpResponse:

        if ident := request.POST.get("admin_ident"):
            AdminAccount(identifier=ident).save()

        return redirect(reverse("account"))

    @staticmethod
    @require_login
    def remove_admin(request) -> HttpResponse:
        
        ident = request.POST.get("admin_ident")
        print(AdminAccount.objects.all(), ident)
        if ident and ident != AccountView.get_identifier(request):
            AdminAccount.objects.get(identifier=ident).delete()

        return redirect(reverse("account"))

    @staticmethod
    def authenticate(request: HttpRequest) -> HttpResponse:
        if AccountView.is_logged_in(request):
            redirect_url = request.build_absolute_uri()
            if redirect_url == request.build_absolute_uri(reverse("login")):
                return redirect("/")
        request.session["last_request"] = request.build_absolute_uri()
        return OAUTH.openid.authorize_redirect(
            request, request.build_absolute_uri(reverse("auth_callback"))
        )

    @staticmethod
    def authenticate_callback(request: HttpRequest) -> HttpResponse:
        token = OAUTH.openid.authorize_access_token(request)

        ident = token["userinfo"][OPENID_CLIENT_IDENT]

        if not AdminAccount.objects.filter(identifier=ident).exists():
            return redirect(reverse("denied"))

        request.session["admin_ident"] = token["userinfo"][OPENID_CLIENT_IDENT]
        request.session["logged_in"] = True
        return redirect(request.session.get("last_request", "/"))

    @staticmethod
    def get_identifier(request: HttpRequest) -> Optional[str]:
        if not AccountView.is_logged_in(request):
            return None
        return request.session.get("admin_ident")

    @staticmethod
    def is_logged_in(request: HttpRequest) -> bool:
        return (
            "admin_ident" in request.session
            and AdminAccount.objects.filter(
                identifier=request.session["admin_ident"]
            ).exists()
        )

    @staticmethod
    def denied(request: HttpRequest):
        context = {
            "info_type": "error",
            "header": "No Access",
            "message": "You dont have access to this resource",
            "url_link" : "index"
        }
        return render(request, "info.html", context=context)

    @staticmethod
    def logout(request: HttpRequest):
        del request.session["admin_ident"]
        del request.session["logged_in"]

        return redirect("/")
