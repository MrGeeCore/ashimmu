from django.core.management.base import BaseCommand
from django.conf import settings

from discord_auth.bot import DiscordBot


class Command(BaseCommand):
    help = 'Starts the Discord authentication bot.'

    def handle(self, *args, **options):
        bot = DiscordBot(settings.DISCORD_SERVER_ID)
        bot.run(settings.DISCORD_BOT_SECRET)
