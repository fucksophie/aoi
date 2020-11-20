import json
import discord
import urllib.parse

from discord.ext import commands

class Fun(commands.Cog):
    """ Commands that don't really have purpose, for fun. """

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def googlethat(self, ctx, *, arg=None):
        """ Google That. 
        Usage: googlethat 
        """
        if arg:
            await ctx.send(f"Google*That*: http://letmegooglethat.com/?q={urllib.parse.quote(arg)}")
        else:
            await ctx.send("Wow, I can't google anything for you if you don't say what to google.")

def setup(client):
    client.add_cog(Fun(client))