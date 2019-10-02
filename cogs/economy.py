import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import sqlite3


colour = 0xF4DF42
command_prefix = "brit "


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("economy.sqlite")
        self.c = self.db.cursor()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if not ctx.content.startswith(command_prefix):
                self.c.execute(
                    "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                    {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
                )
                balance = self.c.fetchone()
                try:

                    self.c.execute(
                        "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                        {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
                    )
                    self.c.execute(
                        "UPDATE economy SET balance = :balance WHERE guild=:guild AND user=:user",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": balance[0] + 1,
                        },
                    )
                    self.db.commit()
                except:
                    self.c.execute(
                        f"INSERT INTO economy VALUES ({ctx.guild.id}, {ctx.author.id}, {1})"
                    )
                    self.db.commit()

    @commands.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member = None):
        if not user:
            self.c.execute(
                "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
            )
            balance = self.c.fetchone()
            try:
                len(balance)
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Balance",
                    description=f"£{balance[0]}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            except:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Balance",
                    description=f"£0",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
        else:
            self.c.execute(
                "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                {"guild": f"{ctx.guild.id}", "user": f"{user.id}"},
            )
            balance = self.c.fetchone()
            try:
                len(balance)
                embed = discord.Embed(
                    title=f"{user.name}'s Balance",
                    description=f"£{balance[0]}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            except:
                embed = discord.Embed(
                    title=f"{user.name}'s Balance", description=f"£0", color=colour
                )
                await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def transfer(self, ctx):
        amount = float(
            "".join(
                [
                    i
                    for i in ctx.message.clean_content[
                        len(command_prefix + "transfer") :
                    ]
                    .strip()
                    .lower()
                    if i.isdigit() or "." in i
                ]
            )
        )
        print(amount)
        receiver = (
            ctx.message.content[len(command_prefix + "transfer") :]
            .strip()
            .replace(str(amount), "")
        )
        receiver = receiver[3:-1]
        receiver = await MemberConverter().convert(ctx, receiver)

        self.c.execute(
            "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
        )
        send_balance = self.c.fetchone()
        self.db.commit()
        self.c.execute(
            "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{ctx.guild.id}", "user": f"{receiver.id}"},
        )
        receive_balance = self.c.fetchone()
        self.db.commit()
        try:
            len(receive_balance)
        except:
            self.c.execute(
                f"INSERT INTO economy VALUES ({ctx.guild.id}, {receiver.id}, {0})"
            )
            self.db.commit()
        self.c.execute(
            "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{ctx.guild.id}", "user": f"{receiver.id}"},
        )
        receive_balance = self.c.fetchone()
        self.db.commit()
        try:
            len(send_balance)
            if send_balance[0] >= amount:
                self.c.execute(
                    "UPDATE economy SET balance = :balance WHERE guild=:guild AND user=:user",
                    {
                        "guild": f"{ctx.guild.id}",
                        "user": f"{receiver.id}",
                        "balance": receive_balance[0] + round(amount, 2),
                    },
                )
                self.db.commit()
                self.c.execute(
                    "UPDATE economy SET balance = :balance WHERE guild=:guild AND user=:user",
                    {
                        "guild": f"{ctx.guild.id}",
                        "user": f"{ctx.author.id}",
                        "balance": send_balance[0] - round(amount, 2),
                    },
                )
                self.db.commit()
                self.c.execute(
                    "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                    {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
                )
                send_balance = self.c.fetchone()
                embed = discord.Embed(
                    title=f"You now have:",
                    description=f"£{send_balance[0]}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("Insufficient funds!")
                return
        except IndexError:
            await ctx.channel.send("Insufficient funds!")


def setup(client):
    client.add_cog(economy(bot))
