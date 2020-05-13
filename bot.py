import discord
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import json
import os
import sys
import tiquations
import sqlite3


extensions = ["cogs.programming", "cogs.util", "cogs.fun", "cogs.sound", "cogs.economy"]
categories = ["programming", "util", "fun", "eco"]
commandlist = [
    "blacken",
    "yapfify",
    "pepify",
    "evaluate",
    "whois",
    "whoami",
    "ping",
    "bug",
    "tea",
    "rem",
    "say",
]
command_prefix = "brit "
players = {}
client = commands.Bot(command_prefix=command_prefix, case_insensitive=True)
client.remove_command("help")
os.chdir(r"yes")


@client.event
async def on_ready():
    print("Ready when you are.")
    print(f"I am running on {client.user.name}")
    print(
        f"With the {discord.__version__} version of discord.py. Version info:\n {discord.version_info}"
    )
    print(f"With the ID: {client.user.id}")
    print("\n \n")
    await client.change_presence(activity=discord.Game(name=command_prefix + "help"))


@client.command(pass_context=True)
async def load(ctx):
    # Loads an extension.
    extension_name = ctx.message.content[len(command_prefix + "load") :].strip()
    extension_name = f"cogs.{extension_name}"
    if not extension_name in extensions:
        await ctx.channel.send("That is not the name of an extension.")
        return
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.channel.send("{} loaded.".format(extension_name))


@client.command(pass_context=True)
async def unload(ctx, message):
    # Unloads an extension.
    extension_name = ctx.message.content[len(command_prefix + "unload") :].strip()
    extension_name = f"cogs.{extension_name}"
    if not extension_name in extensions:
        await ctx.channel.send("That is not the name of an extension.")
        return
    client.unload_extension(extension_name)
    await ctx.channel.send("{} unloaded.".format(extension_name))


@client.command(pass_context=True)
async def reload(ctx):
    # Reloads an extension
    extension_name = ctx.message.content[len(command_prefix + "reload") :].strip()
    extension_name = f"cogs.{extension_name}"
    if not extension_name in extensions:
        await ctx.channel.send("That is not the name of an extension.")
        return
    client.reload_extension(extension_name)
    await ctx.channel.send(f"{extension_name} reloaded")


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(color=0x33ABC6)
    embed.add_field(name="help", value="Returns this message.", inline=False)

    key = ctx.message.content.replace("brit help ", "").lower()
    if key in categories:
        if key == "programming":
            embed.add_field(
                name="blacken",
                value="input some python code and it will return it formatted using Black",
                inline=False,
            )
            embed.add_field(
                name="yapfify",
                value="returns formatted python code using google yapf",
                inline=False,
            )
            embed.add_field(
                name="pepify",
                value="returns code formatted using Autopep8",
                inline=False,
            )
        elif key == "util":
            embed.add_field(
                name="ping", value="Returns ':ping_pong: pong!!'", inline=False
            )
            embed.add_field(
                name="whois", value="Returns info on the given user", inline=False
            )
            embed.add_field(name="whoami", value="Returns info on you.", inline=False)
            embed.add_field(
                name="say", value="Returns the text you entered", inline=False
            )
            embed.add_field(
                name="getpoll", value="Returns info on a strawpoll", inline=False
            )
        elif key == "fun":
            embed.add_field(
                name="noot", value="Returns an image of pingu.", inline=False
            )
            embed.add_field(
                name="pong", value="play a game of pong online", inline=False
            )

        elif key == "eco":
            embed.add_field(
                name="balance", value="Returns your balance in Pounds", inline=False
            )
            embed.add_field(
                name="income",
                value="Returns your weekly income in Pounds",
                inline=False,
            )
            embed.add_field(
                name="daily", value="Collect a daily cash draw.", inline=False
            )
            embed.add_field(
                name="transfer",
                value="Transfer an amount of money to another user.",
                inline=False,
            )
            embed.add_field(
                name="share",
                value="Share an amount of money between multiple users.",
                inline=False,
            )

        msg = await ctx.message.author.send(embed=embed)

    else:
        await ctx.message.author.send(
            f"{key} is not a valid key. Accepted keys are: Programming, Util, Fun and Eco. For example: `brit help util`"
        )
    await ctx.message.add_reaction("✉")


client.run(os.getenv("BRITBOT_DEV_TOKEN"))
