import discord
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import os
import sys

command_prefix = "brit "


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # FUN START
    @commands.command(pass_context=True)
    async def noot(self, ctx):
        try:
            await ctx.channel.send("NOOT NOOT")
            await bot.send_file(ctx.message.channel, "Noot_Noot.jpg")
        except:
            await ctx.channel.send("Invalid Input")

    @commands.command(pass_context=True)
    async def pong(self):
        try:
            await ctx.channel.send(":ping_pong:  http://www.ponggame.org/")
        except:
            await ctx.channel.send("uh something really bad happened help")


def setup(client):
    client.add_cog(fun(bot))
