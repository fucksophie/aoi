
import discord
import shelve
import random
import time
from threading import Lock
from discord.ext import commands

class Levels(commands.Cog):
    """ Leveling system """

    def __init__(self, client):
        self.client = client
        self.mutex = Lock()

    @staticmethod
    def _get_level_xp(n):
        return 5*(n**2)+50*n+100

    @staticmethod
    def _get_level_from_xp(xp):
        remaining_xp = int(xp)
        level = 0
    
        while remaining_xp >= Levels._get_level_xp(level):
            remaining_xp -= Levels._get_level_xp(level)
            level += 1
    
        return level

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild.id != 264445053596991498:
            self.mutex.acquire()
            db = shelve.open("db.shelve")
            if not ctx.author.bot:
                if not str(ctx.author.id) in db:
                    db[str(ctx.author.id)] = {"level": 1, "xp": 1, "time": int(time.time())}
                else:
                    user = db[str(ctx.author.id)]   

                    if int(time.time()) > user["time"] + 60:
                        user["time"] = int(time.time())

                        lvl = Levels._get_level_from_xp(user["xp"])

                        user["xp"] += random.randint(15, 25)
                
                        new_lvl = Levels._get_level_from_xp(user["xp"])

                        if new_lvl != lvl:
                            user["level"] = new_lvl
                            await ctx.channel.send(f"You've leveled up by {new_lvl - lvl}!")

                        db[str(ctx.author.id)] = user
            db.close()
            self.mutex.release()

    @commands.command(aliases=["me"])
    async def profile(self, ctx):
        """ Get your leveling stats """
        self.mutex.acquire()
        db = shelve.open("db.shelve")
        user = db[str(ctx.author.id)]
        
        embed = discord.Embed(title=f"{ctx.author.name}'s Profile")
        embed.add_field(name="Level", value=user["level"], inline=True)
        embed.add_field(name="XP", value=user["xp"], inline=True)
        db.close()
        self.mutex.release()
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Levels(client))