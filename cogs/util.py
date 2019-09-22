import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import asyncio
import strawpy


class util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def whois(ctx, user: discord.Member):
        try:
            embed = discord.Embed(title=f"{user}'s info",
                                  description="Here's what I could find:",
                                  color=0xff2ddf)
            embed.add_field(name="Username", value=user, inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.add_field(name="Status", value=user.status, inline=False)
            embed.add_field(name="Highest role",
                            value=user.top_role,
                            inline=False)
            embed.add_field(name="Joined at",
                            value=user.joined_at,
                            inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.channel.send(
                "**There was an error computing your input. Please try again. \nIf this has happened already, you can report a bug using `brit bug`**"
            )

    @commands.command(pass_context=True)
    async def whoami(ctx):
        author = ctx.message.author

        embed = discord.Embed(title="{}'s info".format(author),
                              description="Here's what I could find:",
                              color=0xff2ddf)
        embed.add_field(name="Name", value=author, inline=False)
        embed.add_field(name="ID", value=author.id, inline=False)
        embed.add_field(name="Status", value=author.status, inline=False)
        embed.add_field(name="Highest role",
                        value=author.top_role,
                        inline=False)
        embed.add_field(name="Joined at", value=author.joined_at, inline=False)
        embed.set_thumbnail(url=author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def say(self, ctx, message):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                content = ctx.message.content.replace('dev say', '')
                message = content.split(' | ')[0]
                channel = content.split(' | ')[1]
                channel = get(self.client.get_all_channels(),
                              guild__name=ctx.message.guild.name,
                              name=channel)
                await channel.send(message)
            except Exception as e:
                await ctx.channel.send("Invalid Input")
                raise e
        else:
            await ctx.channel.send(
                f"{ctx.message.author.mention}, you do not have permission to run that command"
            )

    @commands.command(pass_context=True)
    async def getpoll(ctx):
        try:
            content = ctx.message.content[len(command_prefix +
                                              "getpoll"):].strip()
            poll = strawpy.get_poll(str(content))

            embed = discord.Embed(title="{}'s info".format(poll.title),
                                  description="Here's what I could find:",
                                  color=0xf4df42)
            embed.add_field(name="Options", value=poll.options, inline=False)
            embed.add_field(name="Votes", value=poll.votes, inline=False)
            embed.add_field(name="Results",
                            value=poll.results_url,
                            inline=False)
            embed.set_thumbnail(
                url=
                "https://pbs.twimg.com/profile_images/737742455643070465/yNKcnrSA_400x400.jpg"
            )
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Invalid input")

    @commands.command(pass_context=True)
    async def createpoll(ctx):
        content = ctx.message.content.replace('brit createpoll', '')
        pollTitle = content.split('|')
        strawpy.create_poll(pollTitle[0], pollTitle[1:])
        await ctx.channel.send("Invalid input")

    @commands.command(pass_context=True)
    async def bug(self, ctx):
        content = ctx.message.content.replace('brit bug', '')
        name = content.split('|')[0]
        description = content.split('|')[1]
        author = ctx.message.author
        embed = discord.Embed(title=f'Bug report',
                              description=f'From user \'{author.mention}\'',
                              color=colour)
        embed.add_field(name=name, value=description, inline=False)
        await self.client.get_channel(566282530530131978).send(embed=embed)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        embed = discord.Embed(title='Ping',
                              description='Ping data for BritBot',
                              color=colour)
        embed.add_field(name=':ping_pong:',
                        value=f'{round(self.client.latency, 1)}',
                        inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def rem(self, ctx, amount):
        if ctx.message.author.guild_permissions.manage_messages:
            if int(amount) > 99 or int(amount) < 2:
                await ctx.channel.send('Please enter a value between 2 and 99')
            else:
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
    async def addrole(self, ctx):
        role = ctx.message.content.replace('brit addrole ', '')
        role = get(ctx.message.guild.roles, name=role)
        if role:
            await ctx.message.author.add_roles(role)

    @commands.command(pass_context=True)
    async def remrole(self, ctx):
        role = ctx.message.content.replace('brit remrole ', '')
        role = get(ctx.message.guild.roles, name=role)
        if role:
            await ctx.message.author.remove_roles(role)


def setup(client):
    client.add_cog(util(client))
