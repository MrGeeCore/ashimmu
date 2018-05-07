from django.urls import path

import discord_auth.views


app_name = 'discord_auth'


urlpatterns = [
    path('', discord_auth.views.TokenView.as_view(), name='token'),
]
