from django.contrib import admin

from discord_auth.models import DiscordAuthToken, DiscordUser, DiscordRole


class DiscordAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    fields = ('user', 'token')


class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')
    fields = ('user', 'id')


class DiscordRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('group', 'name')


admin.site.register(DiscordAuthToken, DiscordAuthTokenAdmin)
admin.site.register(DiscordUser, DiscordUserAdmin)
admin.site.register(DiscordRole, DiscordRoleAdmin)
