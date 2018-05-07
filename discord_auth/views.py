from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from django.shortcuts import render

from discord_auth.models import DiscordAuthToken


class TokenView(LoginRequiredMixin, View):
    def get(self, request):
        DiscordAuthToken.objects.filter(user=request.user).delete()

        return render(
            request,
            'discord_auth/token.html',
            {
                'token': DiscordAuthToken.objects.create(user=request.user),
            }
        )
