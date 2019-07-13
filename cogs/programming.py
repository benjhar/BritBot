import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio
import os
import sys
import time
import subprocess
from yapf.yapflib.yapf_api import FormatCode
from autopep8 import fix_code


class programming(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def blackify(ctx):
        content = ctx.message.content.replace('```py',
                                              '').replace('```', '').replace(
                                                  'brit blackify', '')
        with open('blackify.py', 'w') as f:
            f.write(content)

        subprocess.Popen('black blackify.py'.split(), stdout=subprocess.PIPE)

        time.sleep(1)

        with open('blackify.py', 'r') as f:
            text = f.read()

        text = '```py\n' + text + '\n```'
        await ctx.channel.send(text)

    @commands.command(pass_context=True)
    async def yapfify(ctx):
        content = ctx.message.content.replace('```py',
                                              '').replace('```', '').replace(
                                                  'brit yapfify', '')
        formatted = FormatCode(content)
        formatted = '```py\n' + formatted[0] + '\n```'
        time.sleep(1)
        await ctx.channel.send(formatted)

    @commands.command(pass_context=True)
    async def pepify(ctx):
        content = ctx.message.content.replace('```py',
                                              '').replace('```', '').replace(
                                                  'brit pepify', '')
        formatted = fix_code(content)
        formatted = '```py\n' + formatted + '```'
        time.sleep(1)
        await ctx.channel.send(formatted)


def setup(bot):
    bot.add_cog(programming(bot))
