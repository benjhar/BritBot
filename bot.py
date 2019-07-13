import discord
import json
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio
import os
import sys
import time
import strawpy
import tiquations
import subprocess
from yapf.yapflib.yapf_api import FormatCode
from autopep8 import fix_code
from io import StringIO
#import youtube_dl

categories = ['programming', 'util', 'fun']


players = {}
command_prefix = 'brit '
bot = commands.Bot(command_prefix)
bot.remove_command("help")
os.chdir(r"C:\\Users\\benha\\Documents\\Coding\\Python\\DiscordBots\\BritBot")


async def isChannel(ctx):
    return ctx.message.channel in ctx.message.server.channels


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
        await bot.send_message(
            channel, f"{user.mention} has leveled up to level {lvl_end}")


@bot.command(pass_context=True)
async def help(ctx):
	embed = discord.Embed(color=0x33abc6)
	embed.add_field(name="help", value="Returns this message.", inline=False)

	key = ctx.message.content.replace('brit help ', '').lower()
	if key in categories:
		if key == 'programming':
			embed.add_field(
			name='blackify',
			value=
			'input some python code and it will return it formatted using Black',
			inline=False)
			embed.add_field(name='yapfify',
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
			embed.add_field(name="whoami", value="Returns info on you.", inline=False)
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
		await ctx.message.author.send(f'{key} is not a valid key. Accepted keys are: Programming, Util and Fun')
	await ctx.message.add_reaction('✉')


@bot.event
async def on_ready():
    print("Ready when you are.")
    print(f"I am running on {bot.user.name}")
    print(
        f"With the {discord.__version__} version of discord.py. Version info:\n {discord.version_info}"
    )
    print(f"With the ID: {bot.user.id}")
    print("\n \n")
    await bot.change_presence(activity=discord.Game(name=command_prefix +
                                                    "help"))


@bot.event
async def on_message(message):
    try:
        if message.content.startswith(command_prefix):
            await bot.process_commands(message)
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


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Newbie")
    await bot.add_roles(member, role)
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


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.channel.send(":ping_pong: pong!!")


#FUN START
@bot.command(pass_context=True)
async def noot(ctx):
    try:
        await ctx.channel.send("NOOT NOOT")
        await bot.send_file(ctx.message.channel, "Noot_Noot.jpg")
    except:
        await ctx.channel.send("Invalid Input")


"""

"""
#FUN END


#UTIL START
@bot.command(pass_context=True)
async def whois(ctx, user: discord.Member):
    try:
        embed = discord.Embed(title=f"{user}'s info",
                              description="Here's what I could find:",
                              color=0xff2ddf)
        embed.add_field(name="Username", value=user, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Status", value=user.status, inline=False)
        embed.add_field(name="Highest role", value=user.top_role, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.channel.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.channel.send(
            "**There was an error computing your input. Please try again. If this has happened already, you can report a bug using `brit bug`**"
        )


@bot.command(pass_context=True)
async def whoami(ctx):
    author = ctx.message.author

    embed = discord.Embed(title="{}'s info".format(author),
                          description="Here's what I could find:",
                          color=0xff2ddf)
    embed.add_field(name="Name", value=author, inline=False)
    embed.add_field(name="ID", value=author.id, inline=False)
    embed.add_field(name="Status", value=author.status, inline=False)
    embed.add_field(name="Highest role", value=author.top_role, inline=False)
    embed.add_field(name="Joined at", value=author.joined_at, inline=False)
    embed.set_thumbnail(url=author.avatar_url)
    await ctx.channel.send(embed=embed)


@bot.command(pass_context=True)
async def pong():
    try:
        await ctx.channel.send(":ping_pong:  http://www.ponggame.org/")
    except:
        await ctx.channel.send("Invalid Input")


@bot.command(pass_context=True)
async def say(ctx, message):
    if ctx.message.author.server_permissions.manage_messages:
        try:
            await ctx.channel.send("Please now specify the channel")
            channelmessage = await bot.wait_for_message(
                15,
                author=ctx.message.author,
                channel=ctx.message.channel,
                check=isChannel)
            channel = channelmessage.channel
            await bot.send_message(channel, message)
        except Exception as e:
            await ctx.channel.send("Invalid Input")
            raise e
    else:
        await ctx.channel.send(
            f"{ctx.message.author.mention}, you do not have permission to run that command"
        )


@bot.command(pass_context=True)
async def getpoll(ctx):
    try:
        content = ctx.message.content[len(command_prefix + "getpoll"):].strip()
        poll = strawpy.get_poll(str(content))

        embed = discord.Embed(title="{}'s info".format(poll.title),
                              description="Here's what I could find:",
                              color=0xf4df42)
        embed.add_field(name="Options", value=poll.options, inline=False)
        embed.add_field(name="Votes", value=poll.votes, inline=False)
        embed.add_field(name="Results", value=poll.results_url, inline=False)
        embed.set_thumbnail(
            url=
            "https://pbs.twimg.com/profile_images/737742455643070465/yNKcnrSA_400x400.jpg"
        )
        await ctx.channel.send(embed=embed)
    except:
        await ctx.channel.send("Invalid input")


@bot.command(pass_context=True)
async def createpoll(ctx):
    content = ctx.message.content[len(command_prefix + "createpoll"):].strip()
    pollTitle = content.split(",")
    strawpy.create_poll(pollTitle[0], pollTitle[1:])
    await ctx.channel.send("Invalid input")


#UTIL END

#PROGRAMMING START


@bot.command(pass_context=True)
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


@bot.command(pass_context=True)
async def yapfify(ctx):
    content = ctx.message.content.replace('```py',
                                          '').replace('```', '').replace(
                                              'brit yapfify', '')
    formatted = FormatCode(content)
    formatted = '```py\n' + formatted[0] + '\n```'
    time.sleep(1)
    await ctx.channel.send(formatted)


@bot.command(pass_context=True)
async def pepify(ctx):
    content = ctx.message.content.replace('```py',
                                          '').replace('```', '').replace(
                                              'brit pepify', '')
    formatted = fix_code(content)
    formatted = '```py\n' + formatted + '```'
    time.sleep(1)
    await ctx.channel.send(formatted)


#PROGRAMMING END


#SOUND START
@bot.command(pass_context=True)
async def play(ctx, url):
    try:
        server = ctx.message.server
        voice_client = bot.voice_client_in(server)
        player = await bot.voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()
    except:
        await ctx.channel.send("Invalid Input")


@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()


@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()


#SOUND END

bot.run(os.getenv('TOKEN'))
