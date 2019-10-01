import discord
from discord.ext import commands
from discord.ext.commands import bot, has_permissions, CheckFailure
from discord.utils import get
import asyncio
import sqlite3

colour = 0xF4DF42


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("economy.sqlite")
        self.c = self.db.cursor()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if not ctx.content.startswith("brit "):
                self.c.execute(
                    "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
                    {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
                )
                balance = self.c.fetchone()
                if len(balance) > 0:
                    self.db.commit()
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
                else:
                    self.c.execute(
                        f"INSERT INTO economy VALUES ({ctx.guild.id}, {ctx.author.id}, {1})"
                    )

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        self.c.execute(
            "SELECT balance FROM economy WHERE guild=:guild AND user=:user",
            {"guild": f"{ctx.guild.id}", "user": f"{ctx.author.id}"},
        )
        balance = self.c.fetchone()
        if len(balance) > 0:
            embed = discord.Embed(
                title=f"{ctx.author.name}'s Balance",
                description=f"£{balance[0]}",
                color=colour,
            )
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(economy(bot))
