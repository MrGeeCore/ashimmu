from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView, View
from django.conf import settings
from django.shortcuts import redirect

from esipy import EsiSecurity


class SecurityView(View):
    security = EsiSecurity(
        redirect_uri=settings.OAUTH_EVEONLINE_CALLBACK,
        client_id=settings.OAUTH_EVEONLINE_KEY,
        secret_key=settings.OAUTH_EVEONLINE_SECRET,
    )


class LoginView(SecurityView):
    def get(self, *args, **kwargs):
        return redirect(self.security.get_auth_uri())


class CallbackView(SecurityView):
    def get(self, request, *args, **kwargs):
        self.security.auth(request.GET['code'])

        user = authenticate(request, **self.security.verify())

        if user is not None:
            login(request, user)

        return redirect('/')
