import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def noot(self, ctx):
        try:
            await ctx.channel.send("NOOT NOOT")
            await self.client.send_file(ctx.message.channel, "Noot_Noot.jpg")
        except:
            await ctx.channel.send("Invalid Input")


    @commands.command(pass_context=True)
    async def pong(ctx):
        try:
            await ctx.channel.send(":ping_pong:  http://www.ponggame.org/")
        except:
            await ctx.channel.send("Invalid Input")

def setup(client):
    client.add_cog(fun(client))
