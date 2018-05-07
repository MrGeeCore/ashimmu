import discord
import asyncio
from discord.ext import commands
from collections import defaultdict

from django.contrib.auth.models import User
from django.conf import settings

from discord_auth.models import DiscordAuthToken, DiscordUser, DiscordRole


class DiscordBot(commands.Bot):
    def __init__(self, server):
        super().__init__(command_prefix='!')

        self.add_command(auth)
        self.add_command(sync_roles)
        self.add_command(update_roles)
        # self.loop.create_task(self.purge_loop())

    async def purge_loop(self):
        await self.wait_until_ready()

        self.server = self.get_server(settings.DISCORD_SERVER_ID)

        while not self.is_closed:
            await self.sync_roles()
            await self.update_roles()
            await asyncio.sleep(4 * 60 * 60)

    async def update_member_roles(self, member):
        current_roles = set(member.roles)
        all_roles = list(self.get_server(settings.DISCORD_SERVER_ID).roles)

        managed_roles = {
            r for r in all_roles
            if r.id in (
                DiscordRole
                .objects
                .filter(group__isnull=False)
                .values_list('id', flat=True)
            )
        }

        try:
            user = DiscordUser.objects.get(id=member.id).user
            user.eve.update_groups()

            correct_roles = {
                r for r in all_roles
                if r.id in (
                    user.groups.values_list('discord_role__id', flat=True)
                )
            }
        except DiscordUser.DoesNotExist:
            correct_roles = set()

        add_roles = managed_roles & correct_roles
        remove_roles = managed_roles - correct_roles
        final_roles = (current_roles | add_roles) - remove_roles

        if current_roles != final_roles:
            await self.replace_roles(member, *final_roles)

@commands.command(pass_context=True, hidden=True)
async def sync_roles(ctx):
    ctx.bot.server = ctx.bot.get_server(settings.DISCORD_SERVER_ID)

    all_role_ids = []

    for r in ctx.bot.server.roles:
        _, n = DiscordRole.objects.update_or_create(
            id=r.id,
            defaults={'name': r.name}
        )

        all_role_ids.append(r.id)

    DiscordRole.objects.exclude(id__in=all_role_ids).delete()

    await ctx.bot.send_message(
        ctx.message.channel,
        'Discord role sync complete.'
    )

@commands.command(pass_context=True, hidden=True)
async def update_roles(ctx):
    ctx.bot.server = ctx.bot.get_server(settings.DISCORD_SERVER_ID)

    for x in ctx.bot.server.members:
        await ctx.bot.update_member_roles(x)

    await ctx.bot.send_message(
        ctx.message.channel,
        'Discord purge complete.'
    )


@commands.command(pass_context=True)
async def auth(ctx, token : str = None):
    if token is None:
        await ctx.bot.send_message(
            ctx.message.channel,
            'Please enter a token.'
        )
        return

    try:
        token_obj = DiscordAuthToken.objects.get(token=token)
    except DiscordAuthToken.DoesNotExist:
        await ctx.bot.send_message(
            ctx.message.channel,
            'Sorry, but that token does not exist.'
        )
        return

    token_obj.user.eve.update_groups()

    author = ctx.message.author

    roles = {role.id: role for role in ctx.message.channel.server.roles}
    roles_to_add = [
        roles[i] for i in (
            token_obj
            .user
            .groups
            .filter(discord_role__isnull=False)
            .values_list('discord_role__id', flat=True)
        )
    ]

    await ctx.bot.send_message(
        ctx.message.channel,
        'Token found, belongs to %s.' % (
            token_obj.user.eve.full_name,
        )
    )

    try:
        await ctx.bot.change_nickname(author, token_obj.user.eve.full_name)
        await ctx.bot.update_member_roles(author)
    except discord.errors.Forbidden:
        print("No permissions to modify %s." % author.name)

    try:
        old = (
            DiscordUser
            .objects
            .exclude(user=token_obj.user)
            .get(id=author.id)
        )
        await ctx.bot.send_message(
            ctx.message.channel,
            'Discord account was previously claimed by %s, transfering ownership to you.' % old.user.eve.full_name
        )
        old.delete()
    except DiscordUser.DoesNotExist:
        pass

    DiscordUser.objects.update_or_create(
        user=token_obj.user,
        defaults={
            'id': author.id
        }
    )

    token_obj.delete()
