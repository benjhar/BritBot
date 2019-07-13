import discord
import json
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio
import os

import tiquations


extensions = ['cogs.programming', 'cogs.util', 'cogs.fun', 'cogs.sound']
categories = ['programming', 'util', 'fun']
commandlist = [
    'blackify',
    'yapfify',
    'pepify',
    'whois',
    'whoami',
    'ping',
    'bug',
    ''
]

players = {}
command_prefix = 'brit '
client = commands.Bot(command_prefix)
client.remove_command("help")
os.chdir(r"C:\\Users\\benha\\Documents\\Coding\\Python\\DiscordBots\\BritBot")
colour = 0x33abc6

async def update_data(users, user):
    if user.id not in users:
        users[user.id] = {}
        users[user.id]["experience"] = 0
        users[user.id]["level"] = 1


async def add_experience(users, user, exp):
    users[user.id]["experience"] += exp


async def level_up(users, user, channel):
    experience = users[user.id]["experience"]
    lvl_start = users[user.id]["level"]
    lvl_end = int(experience**(1 / 4))
    users[user.id]["level"] = lvl_end
    if lvl_start < lvl_end:
        await client.send_message(
            channel, f"{user.mention} has leveled up to level {lvl_end}")


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(color=colour)
    embed.add_field(name="help", value="Returns this message.", inline=False)

    key = ctx.message.content.replace('brit help ', '').lower()
    if key in categories:
        if key == 'programming':
            embed.add_field(
                name='blackify',
                value=
                'input some python code and it will return it formatted using Black',
                inline=False)
            embed.add_field(
                name='yapfify',
                value='returns formatted python code using google yapf',
                inline=False)
            embed.add_field(name='pepify',
                            value='returns code formatted using Autopep8',
                            inline=False)
        elif key == 'util':
            embed.add_field(name="ping",
                            value="Returns ':ping_pong: pong!!'",
                            inline=False)
            embed.add_field(name="whois",
                            value="Returns info on the given user",
                            inline=False)
            embed.add_field(name="whoami",
                            value="Returns info on you.",
                            inline=False)
            embed.add_field(name="say",
                            value="Returns the text you entered",
                            inline=False)
            embed.add_field(name="getpoll",
                            value="Returns info on a strawpoll",
                            inline=False)
        elif key == 'fun':
            embed.add_field(name="noot",
                            value="Returns an image of pingu.",
                            inline=False)
            embed.add_field(name='pong',
                            value='play a game of pong online',
                            inline=False)

        msg = await ctx.message.author.send(embed=embed)
    else:
        await ctx.message.author.send(
            f'{key} is not a valid key. Accepted keys are: Programming, Util and Fun'
        )
    await ctx.message.add_reaction('✉')


@client.event
async def on_ready():
    print("Ready when you are.")
    print(f"I am running on {client.user.name}")
    print(
        f"With the {discord.__version__} version of discord.py. Version info:\n {discord.version_info}"
    )
    print(f"With the ID: {client.user.id}")
    print("\n \n")
    await client.change_presence(activity=discord.Game(name=command_prefix +
                                                       "help"))


@client.event
async def on_message(message):
    try:
        if message.content.startswith(command_prefix):
            await client.process_commands(message)
        with open("users.json", "r") as file:
            data = ""
            for line in file:
                data += line
            if data == "":
                users = {}
            else:
                users = json.loads(data)

            with open("users.json", "w") as file:
                file.write(json.dumps(users))

            await update_data(users, message.author)
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message.channel)
    except Exception as e:
        print(e)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Newbie")
    await client.add_roles(member, role)
    with open("users.json", "r") as file:
        data = ""
        for line in file:
            data = data + line
        if data == "":
            users = {}
        else:
            users = json.loads(data)

    await update_data(users, member)

    with open("users.json", "w") as file:
        file.write(json.dumps(users))

    with open("economy.json", "r") as file:
        data = ""
        for line in file:
            data = data + line
        if data == "":
            users = {}
        else:
            users = json.loads(data)

    await update_data(users, member)

    with open("economy.json", "w") as file:

        file.write(json.dumps(users))

@client.command(pass_context=True)
async def load(ctx):
    """Loads an extension."""
    extension_name = ctx.message.content.replace(f'dev load ', '')
    try:
        client.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.channel.send("{} loaded.".format(extension_name))

@client.command(pass_context=True)
async def unload(ctx):
    """Unloads an extension."""
    extension_name = ctx.message.content.replace(f'dev unload ', '')
    client.unload_extension(extension_name)
    await ctx.channel.send("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')

client.run(os.getenv('TOKEN'))
