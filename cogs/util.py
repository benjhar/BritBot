import discord
from discord import Client
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import os
import sys
import strawpy
import tiquations
import re
import requests
import time

command_prefix = "brit "

colour = 0xF4DF42


class util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def whois(self, ctx, user: discord.Member):
        try:
            embed = discord.Embed(
                title=f"{user}'s info",
                description="Here's what I could find:",
                color=colour,
            )
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

    @commands.command(pass_context=True)
    async def whoami(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            title="{}'s info".format(author),
            description="Here's what I could find:",
            color=colour,
        )
        embed.add_field(name="Name", value=author, inline=False)
        embed.add_field(name="ID", value=author.id, inline=False)
        embed.add_field(name="Status", value=author.status, inline=False)
        embed.add_field(name="Highest role", value=author.top_role, inline=False)
        embed.add_field(name="Joined at", value=author.joined_at, inline=False)
        embed.set_thumbnail(url=author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command(name="say")
    @has_permissions(manage_messages=True)
    async def say(self, ctx):
        try:
            message = ctx.message.clean_content[len(command_prefix + "say") :].strip()
            channel = message.split("|")[1][1:]
            channel = get(commands.get_all_channels(), name=channel)
            message = message.split("|")[0]

            await channel.send(message)
        except Exception as e:
            await ctx.channel.send(
                "There was a problem processing the command. Please try again later. If this problem persists please contact `leet_hakker#2582`"
            )
            print(e)

    @say.error
    async def say_error(error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.channel.send(
                f"{ctx.message.author.mention}, you do not have permission to run that command"
            )

    @commands.command(pass_context=True)
    async def getpoll(self, ctx):
        try:
            content = ctx.message.content[len(command_prefix + "getpoll") :].strip()
            poll = strawpy.get_poll(str(content))

            embed = discord.Embed(
                title="{}'s info".format(poll.title),
                description="Here's what I could find:",
                color=colour,
            )
            embed.add_field(name="Options", value=poll.options, inline=False)
            embed.add_field(name="Votes", value=poll.votes, inline=False)
            embed.add_field(name="Results", value=poll.results_url, inline=False)
            embed.set_thumbnail(
                url="https://pbs.twimg.com/profile_images/737742455643070465/yNKcnrSA_400x400.jpg"
            )
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Invalid input")

    @commands.command(pass_context=True)
    async def createpoll(self, ctx):
        content = ctx.message.content[len(command_prefix + "createpoll") :].strip()
        pollTitle = content.split(",")
        strawpy.create_poll(pollTitle[0], pollTitle[1:])
        await ctx.channel.send("Invalid input")

    @commands.command(pass_context=True)
    async def bug(self, ctx):
        content = ctx.message.content.replace("brit bug", "")
        name = content.split("|")[0]
        description = content.split("|")[1]
        author = ctx.message.author
        embed = discord.Embed(
            title=f"Bug report",
            description=f"From user '{author.mention}'",
            color=colour,
        )
        embed.add_field(name=name, value=description, inline=False)
        await self.client.get_channel(566282530530131978).send(embed=embed)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        r = requests.get(
            "https://discordapp.com/api",
            headers={"Authorization": f"Bot:{os.getenv('TOKEN')}"},
        )
        latency = r.elapsed.total_seconds()
        embed = discord.Embed(
            title="Ping", description="Ping data for BritBot", color=colour
        )
        embed.add_field(name=":ping_pong:", value=f"{latency*1000}ms", inline=False)
        message = await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def rem(self, ctx, amount):
        if ctx.message.author.guild_permissions.manage_messages:
            channel = ctx.channel
            messages = []
            async for message in channel.history(limit=int(amount) + 1):
                messages.append(message)
            await channel.delete_messages(messages)
        else:
            await ctx.channel.send(
                f"{ctx.message.author.mention}, you do not have permission to run that command"
            )

    @commands.command(pass_context=True)
    async def tea(self, ctx):
        content = ctx.message.content[len(command_prefix + "tea") :].strip().lower()
        keys = content.split(" ")
        subject = None
        category = None
        country = None
        source = None
        for i in keys:
            if "query:" in i:
                subject = i.replace("query:", "")
            elif "category:" in i:
                category = i.replace("category:", "")
            elif "country:" in i:
                country = i.replace("country:", "")
            elif "source:" in i:
                source = i.replace("source:", "")
        if not subject and not category:
            await ctx.channel.send("I need a query or category to fetch news for.")
            return

        # building query
        if subject and not category:
            query = f"https://newsapi.org/v2/everything?q={subject}"
        elif category:
            query = f"https://newsapi.org/v2/everything?category={category}"
            if subject:
                query += f"&q={subject}"

        if country:
            query += f"&country={country}"
        if source:
            query += f"&source={source}"
        query += f"&apiKey={os.getenv('NEWS_API_TOKEN')}"

        # fetching
        r = requests.get(query).json()
        if r["status"] != "ok":
            print(r["status"])
            await ctx.channel.send(
                f"Could not connect to the API. Response: {r['status']} Please try again later."
            )
        # building embed from response
        embed = discord.Embed(
            title=r["articles"][0]["title"],
            url=r["articles"][0]["url"],
            description=r["articles"][0]["description"],
            color=colour,
        )

        embed.set_thumbnail(url=r["articles"][0]["urlToImage"])
        embed.set_footer(text="Powered by News API; https://newsapi.org")
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(util(bot))
