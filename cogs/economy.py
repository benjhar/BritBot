import discord
from discord import Client
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter, CommandOnCooldown
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import sqlite3
import os
import numpy as np
import time
import datetime
import random

colour = 0xF4DF42
command_prefix = "brit "


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("economy.sqlite")
        self.c = self.db.cursor()
        self.id = 599589609529147437
        self.wage = 9.61

    @commands.Cog.listener()
    async def on_ready(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS taxes (guild text, tax boolean, rate integer)"
        )
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS economy (guild text, user text, balance integer, week_income integer)"
        )

        await self.tax_loop()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if not ctx.content.startswith(command_prefix):

                balance = self.get_balance(ctx.guild.id, ctx.author.id)
                income = self.get_income(ctx.guild.id, ctx.author.id)

                try:
                    balance = self.get_balance(ctx.guild.id, self.id)
                except:
                    pass

                try:
                    self.c.execute(
                        "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": round(float(balance + self.wage), 2),
                            "week_income": round(float(income), 2),
                        },
                    )
                    self.db.commit()
                except:
                    self.c.execute(
                        "INSERT INTO economy VALUES (guild=:guild, user=:user, balance=:balance, week_income=:income)",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": round(float(balance), 2),
                            "week_income": round(float(income), 2),
                            "daily": 0,
                        },
                    )
                    self.db.commit()

                balance = self.get_balance(ctx.guild.id, ctx.author.id)
                income = self.get_income(ctx.guild.id, ctx.author.id)
                try:
                    self.c.execute(
                        "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": round(float(balance), 2),
                            "week_income": round(float(income + self.wage), 2),
                        },
                    )
                    self.db.commit()

                except:
                    self.c.execute(
                        "INSERT INTO economy VALUES (guild=:guild, user=:user, balance=:balance, week_income=:week_income)",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": round(float(balance), 2),
                            "week_income": round(float(income), 2),
                            "daily": 0,
                        },
                    )
                    self.db.commit()

                brit_balance = self.get_balance(ctx.guild.id, self.id)
                self.c.execute(
                    "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                    {
                        "balance": round(brit_balance - self.wage, 2),
                        "week_income": 0,
                        "guild": f"{ctx.guild.id}",
                        "user": f"{self.id}",
                    },
                )

                self.db.commit()

    @commands.command(pass_context=True)
    async def share(self, ctx):
        users = ctx.message.mentions
        for user in users:
            amount = ctx.message.clean_content.replace(f"@{user.name}", "")
        amount = float("".join([i for i in amount if i.isdigit() or i == "."]))
        per_user = round(amount / len(users), 2)
        send_balance = self.get_balance(ctx.guild.id, ctx.author.id)
        if send_balance >= amount:
            for user in users:
                send_balance = self.get_balance(ctx.guild.id, ctx.author.id)
                receive_balance = self.get_balance(ctx.guild.id, user.id)
                receive_income = self.get_income(ctx.guild.id, user.id)
                try:
                    len(receive_balance)
                except:
                    self.c.execute(
                        f"INSERT INTO economy VALUES ({ctx.guild.id}, {user.id}, {0}, {0})"
                    )
                    self.db.commit()
                self.db.commit()
                if send_balance >= per_user:
                    self.c.execute(
                        "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{user.id}",
                            "balance": receive_balance + round(per_user, 2),
                            "week_income": receive_income + round(per_user, 2),
                        },
                    )
                    self.db.commit()
                    self.c.execute(
                        "UPDATE economy SET balance = :balance WHERE guild=:guild AND user=:user",
                        {
                            "guild": f"{ctx.guild.id}",
                            "user": f"{ctx.author.id}",
                            "balance": send_balance - round(per_user, 2),
                        },
                    )
                    self.db.commit()
                    self.c.execute(
                        "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                        {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
                    )
                    send_balance = self.c.fetchone()

                else:
                    await ctx.channel.send("Insufficient funds!")
                    return

            embed = discord.Embed(
                title=f"You now have:", description=f"£{send_balance[0]}", color=colour
            )
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send("Insufficient funds!")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def daily(self, ctx):
        payout = random.randrange(300.00)
        balance = self.get_balance(ctx.guild.id, ctx.author.id)
        income = self.get_income(ctx.guild.id, ctx.author.id)
        self.c.execute(
            "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
            {
                "balance": balance + payout,
                "week_income": income + payout,
                "guild": f"{ctx.guild.id}",
                "user": f"{ctx.author.id}",
            },
        )
        self.db.commit()
        embed = discord.Embed(
            title="You received", description=f"£{payout}", color=colour
        )
        await ctx.channel.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            retry_after = datetime.timedelta(seconds=error.retry_after)
            embed = discord.Embed(
                title="You cannot claim your daily yet.",
                description=f"You must wait {retry_after} hours",
                color=colour,
            )
            await ctx.channel.send(embed=embed)
        else:
            print(error)

    @commands.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member = None):
        if not user:
            balance = self.get_balance(ctx.guild.id, ctx.author.id)
            if balance:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Balance",
                    description=f"£{balance}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Balance",
                    description=f"£0",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
        else:
            balance = self.get_balance(ctx.guild.id, user.id)
            if balance:
                embed = discord.Embed(
                    title=f"{user.name}'s Balance",
                    description=f"£{balance}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{user.name}'s Balance", description=f"£0", color=colour
                )
                await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def income(self, ctx, user: discord.Member = None):
        if not user:
            income = self.get_income(ctx.guild.id, ctx.author.id)
            if income:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Weekly Income",
                    description=f"£{income}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Weekly Income",
                    description=f"£0",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
        else:
            income = self.get_income(ctx.guild.id, user.id)
            if income:
                embed = discord.Embed(
                    title=f"{user.name}'s Weekly Income",
                    description=f"£{income}",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{user.name}'s Weekly Income",
                    description=f"£0",
                    color=colour,
                )
                await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def transfer(self, ctx):
        receiver = ctx.message.mentions[0]
        amount = int(
            "".join(
                [
                    i
                    for i in ctx.message.clean_content.replace(f"@{receiver.name}", "")
                    if i.isdigit()
                ]
            )
        )

        send_balance = self.get_balance(ctx.guild.id, ctx.author.id)
        receive_balance = self.get_balance(ctx.guild.id, receiver.id)
        receive_income = self.get_income(ctx.guild.id, receiver.id)
        self.db.commit()
        try:
            len(send_balance)
            if send_balance[0] >= amount:
                self.c.execute(
                    "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                    {
                        "guild": f"{ctx.guild.id}",
                        "user": f"{receiver.id}",
                        "balance": receive_balance[0] + round(amount, 2),
                        "week_income": receive_income + round(amount, 2),
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

    async def tax_loop(self):
        while True:
            self.c.execute("SELECT guild FROM taxes")
            guilds = self.c.fetchall()
            guilds = np.unique(np.array(guilds)).tolist()
            for guild in guilds:
                self.c.execute(
                    "SELECT tax FROM taxes WHERE guild =:guild", {"guild": f"{guild}"}
                )
                taxes = self.c.fetchone()
                if taxes[0]:
                    self.c.execute(
                        "SELECT rate FROM taxes WHERE guild =:guild",
                        {"guild": f"{guild}"},
                    )
                    rate = self.c.fetchone()[0]
                    self.c.execute(
                        "SELECT user FROM economy WHERE guild =:guild",
                        {"guild": f"{guild}"},
                    )
                    members = self.c.fetchall()
                    for user in members:
                        balance = self.get_balance(guild, user[0])
                        income = self.get_income(guild, user[0])
                        try:
                            if balance > 0:
                                tax = round(balance * rate, 2)
                                if income > 227.90 and balance >= tax:
                                    new_balance = balance - tax

                                    self.c.execute(
                                        "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                                        {
                                            "balance": new_balance,
                                            "week_income": 0,
                                            "guild": f"{guild}",
                                            "user": f"{user[0]}",
                                        },
                                    )

                                    self.db.commit()

                                    brit_balance = self.get_balance(guild, self.id)
                                    self.c.execute(
                                        "UPDATE economy SET balance = :balance, week_income = :week_income WHERE guild=:guild AND user=:user",
                                        {
                                            "balance": round(
                                                brit_balance + balance * rate, 2
                                            ),
                                            "week_income": 0,
                                            "guild": f"{guild}",
                                            "user": f"{self.id}",
                                        },
                                    )

                                    self.db.commit()
                        except Exception as e:
                            self.c.execute(
                                "UPDATE economy SET week_income = :week_income WHERE guild=:guild AND user=:user",
                                {
                                    "week_income": 0,
                                    "guild": f"{guild}",
                                    "user": f"{user[0]}",
                                },
                            )

                            self.db.commit()
                            print(e)

            await asyncio.sleep(604800)

    def get_balance(self, guild, user):
        self.c.execute(
            "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{guild}", "user": f"{user}"},
        )
        balance = self.c.fetchone()
        try:
            return balance[0]
        except:
            if user == self.id:
                self.c.execute(
                    f"INSERT INTO economy VALUES ({guild}, {user}, {1000000000}, {0})"
                )
                self.db.commit()
            else:
                self.c.execute(
                    f"INSERT INTO economy VALUES ({guild}, {user}, {0}, {0})"
                )
                self.db.commit()
            return self.get_income(guild, user)

    def get_income(self, guild, user):
        self.c.execute(
            "SELECT week_income FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{guild}", "user": f"{user}"},
        )
        income = self.c.fetchone()
        try:
            return income[0]
        except:
            self.c.execute(f"INSERT INTO economy VALUES ({guild}, {user}, {0}, {0})")
            self.db.commit()
            return self.get_income(guild, user)


def setup(client):
    client.add_cog(economy(bot))
