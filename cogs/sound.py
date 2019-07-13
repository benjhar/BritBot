import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

class sound(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def play(ctx, url):
        try:
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            player = await self.client.voice_client.create_ytdl_player(url)
            players[server.id] = player
            player.start()
        except:
            await ctx.channel.send("Invalid Input")


    @commands.command(pass_context=True)
    async def pause(ctx):
        id = ctx.message.server.id
        players[id].pause()


    @commands.command(pass_context=True)
    async def stop(ctx):
        id = ctx.message.server.id
        players[id].stop()


    @commands.command(pass_context=True)
    async def resume(ctx):
        id = ctx.message.server.id
        players[id].resume()

def setup(client):
    client.add_cog(sound(client))
