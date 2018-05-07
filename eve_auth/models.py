import requests
import json
import esipy

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


ESI_APP = esipy.App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
ESI_CLIENT = esipy.EsiClient(
    header={'User-Agent': 'Sharad Heft - Predditors Discord auth'},
)


class EveData(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='eve'
    )

    full_name = models.CharField(max_length=64)
    character_id = models.BigIntegerField()

    class Meta:
        verbose_name = 'EVE Data'
        verbose_name_plural = 'EVE Data'

    def update_groups(self):
        self.__update_affiliation_groups()

    def __update_affiliation_groups(self):
        corp, alliance = self.get_allegiance()

        with transaction.atomic():
            self.user.groups.remove(
                *self.user.groups.filter(
                    Q(name__startswith='corporation_') |
                    Q(name__startswith='alliance_')
                )
            )

            if alliance is not None:
                alliance, _ = Group.objects.get_or_create(name='alliance_%d' % alliance)
                self.user.groups.add(alliance)

            corporation, _ = Group.objects.get_or_create(name='corporation_%d' % corp)
            self.user.groups.add(corporation)

    def get_allegiance(self):
        data = ESI_CLIENT.request(
            ESI_APP.op['post_characters_affiliation'](
                characters=[self.character_id]
            )
        ).data[0]

        return data['corporation_id'], data.get('alliance_id', None)

    def __str__(self):
        return self.full_name
