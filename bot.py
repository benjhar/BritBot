# Role by SomeGuy

import discord
import json
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio
import os
import time
#import strawpoll
#import youtube_dl

players = {}
#api = strawpoll.API()
command_prefix='£'
bot = commands.Bot(command_prefix)
bot.remove_command("help")
os.chdir(r"/home/pi/Desktop/Documents/Coding/Python/Discord/Role")

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        color=0x33abc6
    )

    embed.add_field(name="help", value="Returns this message.", inline=False)
    embed.add_field(name="ping", value="Returns ':ping_pong: pong!!'", inline=False)
    embed.add_field(name="whois", value="Returns info on the given user", inline=False)
    embed.add_field(name="noot", value="Returns an image of pingu.", inline=False)
    embed.add_field(name="whami", value="Returns info on you.", inline=False)
    #embed.add_field(name="say", value="Returns the text you entered", inline=False)
    #embed.add_field(name="stpoll", value="Returns info on a strawpoll", inline=False)

    await bot.send_message(author, embed=embed)
    await bot.send_message(ctx.message.channel, "A list of commands has been sent to your DMs")

@bot.event
async def on_ready():
    print("Ready when you are.")
    print("I am running on " + bot.user.name)
    print("With the ID: " + bot.user.id)
    print("\n \n")
    await bot.change_presence(game=discord.Game(name=command_prefix + "help"))

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="User")
    await bot.add_roles(member, role)
    with open("users.json","r") as file:
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

@bot.event
async def on_message(message):
    try:
        if message.content.startswith('£'):
            await bot.process_commands(message)
        with open("users.json","r") as file:
            data = ""
            for line in file:
                data += line
            if data == "":
                users = {}
            else:
                users = json.loads(data)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message.channel)

        with open("users.json", "w") as file:
            file.write(json.dumps(users))

        async def update_data(users, user):
            if not user.id in users:
                users[user.id] = {}
                users[user.id]["experience"] = 0
                users[user.id]["level"] = 1

        async def add_experience(users, user, exp):
            users[user.id]["experience"] += exp

        async def level_up(users, user, channel):
            experience = users[user.id]["experience"]
            lvl_start = users[user.id]["level"]
            lvl_end = int(experience ** (1/4))
            users[user.id]["level"] = lvl_end

        if lvl_start < lvl_end:
            await bot.send_message(channel, "{} has leveled up to level {}".format(user.mention, lvl_end))
    except Exception as e:
        print(e)



@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: pong!!")


@bot.command(pass_context=True)
async def whois(ctx, user: discord.Member):
    try:
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find:", color=0xff2ddf)
        embed.add_field(name="Name", value=user.name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Status", value=user.status, inline=False)
        embed.add_field(name="Highest role", value=user.top_role, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await bot.say(embed=embed)
    except:
        await bot.say("Invalid Input")

@bot.command(pass_context=True)
async def whoami(ctx):
    author = ctx.message.author
    
    embed = discord.Embed(title="{}'s info".format(author), description="Here's what I could find:", color=0xff2ddf)
    embed.add_field(name="Name", value=author, inline=False)
    embed.add_field(name="ID", value=author.id, inline=False)
    embed.add_field(name="Status", value=author.status, inline=False)
    embed.add_field(name="Highest role", value=author.top_role, inline=False)
    embed.add_field(name="Joined at", value=author.joined_at, inline=False)
    embed.set_thumbnail(url=author.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def pong(ctx):
    try:
        await bot.say(":ping_pong:  http://www.ponggame.org/")
    except:
        await bot.say("Invalid Input")
@bot.command(pass_context=True)
async def noot(ctx):
    try:
        await bot.say("NOOT NOOT")
        await bot.send_file(ctx.message.channel, "Noot_Noot.jpg")
    except:
        await bot.say("Invalid Input")

"""
@bot.command(pass_context=True)
async def say(ctx):
    try:
        content = ctx.message.content[len(command_prefix + 'say'):].strip()
        if '@' in content:
            pass
        else:
            await bot.say(content)
    except:
        await bot.say("Invalid Input")

"""
@bot.command(pass_context=True)
async def stpoll(ctx):
    try:
        content = ctx.message.content[len(command_prefix + 'stpoll'):].strip()
        poll = strawpoll.get_poll(content.strawpy.id)
        options = content.strawpoll.options
        votes = content.strawpoll.votes

        embed = discord.Embed(title='{}\'s status'.format(content), description='Here\'s what I have:', color=0x6441a5)
        embed.add_field(name='Title', value=content, inline=False)
        embed.add_field(name='ID', value=content.strawpoll.id, inline=False)
        embed.add_field(name='Options', value=options, inline=False)
        embed.add_field(name='Votes', value=votes, inline=False)

        await bot.say(embed=embed)
    except Exception as e:
        await bot.say("Invalid Input: " + str(e))

@bot.command(pass_context=True)
async def play(ctx, url):
    try:
        server = ctx.message.server
        voice_client = bot.voice_client_in(server)
        player = await bot.voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()
    except:
        await bot.say("Invalid Input")

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

bot.run("YOUR_BOTS_TOKEN")
