import json
import discord
import sqlite3
import time
import random

from discord.ext import commands
from .utils import levels

class Levels(commands.Cog):
    """ Leveling system! """
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild.id != 776217501456662589:
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
 
            cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, level INTEGER, xp INTEGER, time INTEGER)")

            cur.execute(f"SELECT * FROM users WHERE id = {ctx.author.id}") 
            user = cur.fetchone()
        
            if user:
                user = list(user)
            
                if int(time.time()) > user[3] + 60:
                    lvl = levels.xpToLevel(user[2])

                    user[2] += random.randint(15, 25)

                    new_lvl = levels.xpToLevel(user[2])

                    if new_lvl != lvl:
                        user[1] = new_lvl

                        await ctx.channel.send(f"LEVEL UP! You're now at level {user[1]}!", delete_after=10)
        
                    cur.execute(f"UPDATE users SET xp = {user[2]}, level = {user[1]}, time = {int(time.time())} WHERE id = {ctx.author.id}")
            else:
                if not ctx.author.bot:
                    cur.execute(f"INSERT INTO users VALUES ({ctx.author.id}, 1, 1, {int(time.time())})")
        
            con.commit()
            cur.close()
            con.close()

    @commands.command()
    async def profile(self, ctx):
        """ Get your Leveling profile! """
        
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        
        cur.execute(f"SELECT * FROM users WHERE id = {ctx.author.id}") 
        user = list(cur.fetchone())

        embed = discord.Embed()
        embed.add_field(name="Level", value=user[1], inline=True)
        embed.add_field(name="XP", value=user[2], inline=True)
        embed.add_field(name="XP until next Level", value=levels.levelToXp(user[1]+1), inline=True)
        
        await ctx.send(embed=embed)

        cur.close()
        con.close()

    @commands.command()
    async def leaderboard(self, ctx):
        """ Get the global leaderboard! """
        
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        
        cur.execute(f"SELECT * FROM users ORDER BY xp DESC LIMIT 10;") 
        leaderboard = list(cur.fetchall())
        embed = discord.Embed()
        
        rank = 0
        for player in leaderboard:
            rank += 1
            user = await self.client.fetch_user(player[0])

            embed.add_field(name=f"#{rank} | {user.name}#{user.discriminator}", value=f"XP: {player[2]} L: {player[1]}")

        await ctx.send(embed=embed)
        
        cur.close()
        con.close()
        
def setup(client):
    client.add_cog(Levels(client))