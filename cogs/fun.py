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
        await ctx.channel.send("NOOT NOOT")
        await ctx.channel.send_file("Noot_Noot.jpg")


    @commands.command(pass_context=True)
    async def pong(ctx):
        await ctx.channel.send(":ping_pong:  http://www.ponggame.org/")

    @commands.command(pass_context=True)
    async def rpost(ctx):
        

def setup(client):
    client.add_cog(fun(client))
