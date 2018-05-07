import random
import string

from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings


def get_random_token():
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(DiscordAuthToken.TOKEN_LENGTH)
    )


class DiscordAuthToken(models.Model):
    TOKEN_LENGTH = 20

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='token',
        primary_key=True
    )

    token = models.CharField(
        max_length=TOKEN_LENGTH,
        default=get_random_token,
        db_index=True
    )


class DiscordUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='discord',
        primary_key=True
    )

    id = models.CharField(max_length=128, db_index=True, unique=True)


class DiscordRole(models.Model):
    id = models.CharField(max_length=128, primary_key=True)

    group = models.ManyToManyField(
        Group,
        related_name='discord_role',
        db_index=True,
    )

    name = models.CharField(max_length=128, db_index=True)
