import discord
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import os
import sys

command_prefix = "brit "


class sound(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        try:
            server = ctx.message.server
            voice_bot = bot.voice_client_in(server)
            player = await bot.voice_client.create_ytdl_player(url)
            players[server.id] = player
            player.start()
        except:
            await ctx.channel.send("Invalid Input")

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        id = ctx.message.server.id
        players[id].stop()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()


def setup(client):
    client.add_cog(sound(bot))
