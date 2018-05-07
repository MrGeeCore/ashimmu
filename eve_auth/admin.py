from django.contrib import admin

from eve_auth.models import EveData


class EveDataAdmin(admin.ModelAdmin):
    list_display = ('character_id', 'user', 'full_name')
    fields = ('character_id', 'user', 'full_name')

admin.site.register(EveData, EveDataAdmin)
