import discord
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import os
import sys
import subprocess
from yapf.yapflib.yapf_api import FormatCode
from autopep8 import fix_code
from io import StringIO
import time
import ast  # For the eval command

command_prefix = "brit "


class programming(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=["bn", "black"])
    async def blacken(self, ctx):
        content = (
            ctx.message.content.replace("```py", "")
            .replace("```", "")
            .replace("brit blacken", "")
        )
        with open("blacken.py", "w") as f:
            f.write(content)

        subprocess.Popen("black blacken.py".split(), stdout=subprocess.PIPE)

        time.sleep(1)

        with open("blacken.py", "r") as f:
            text = f.read()

        text = "```py\n" + text + "\n```"
        await ctx.channel.send(text)

    @commands.command(pass_context=True, aliases=["y", "yp", "yapf"])
    async def yapfify(self, ctx):
        content = (
            ctx.message.content.replace("```py", "")
            .replace("```", "")
            .replace("brit yapfify", "")
        )
        formatted = FormatCode(content)
        formatted = "```py\n" + formatted[0] + "\n```"
        time.sleep(1)
        await ctx.channel.send(formatted)

    @commands.command(pass_context=True, aliases=["pep", "pep8", "p8"])
    async def pepify(self, ctx):
        content = (
            ctx.message.content.replace("```py", "")
            .replace("```", "")
            .replace("brit pepify", "")
        )
        formatted = fix_code(content)
        formatted = "```py\n" + formatted + "```"
        time.sleep(1)
        await ctx.channel.send(formatted)

    # EVALUATION CODE
    def insert_returns(self, body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    @commands.command(aliases=["eval", "e"])
    async def evaluate(self, ctx, *, cmd):
        if ctx.message.author.id == 330404011197071360:
            """
            -evaluate ```py
            a = 1 + 2
            b = a * 2
            await ctx.send(a + b)
            a
            ```

            remember the space between eavluate and ```py
            """
            try:
                fn_name = "_eval_expr"

                cmd = cmd.strip("` ")
                cmd = cmd.strip("py")

                # add a layer of indentation
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

                # wrap in async def body
                body = f"async def {fn_name}():\n{cmd}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                self.insert_returns(body)

                env = {
                    "bot": ctx.bot,
                    "discord": discord,
                    "commands": commands,
                    "ctx": ctx,
                    "__import__": __import__,
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)
                result = await eval(f"{fn_name}()", env)
            except Exception as uwuowo:
                await ctx.message.channel.send(uwuowo)
        else:
            await ctx.message.channel.send(
                "This command is made only accessible to the bot creators."
            )

    # EVALUATION CODE END


def setup(client):
    client.add_cog(programming(bot))
