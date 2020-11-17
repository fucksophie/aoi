import json
import discord

from discord.ext import commands

config = json.load(open("config.json"))

class Mod(commands.Cog):
    """ Simple moderation commands, in most bots """
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        """ Kick a user 
        Usage: kick <member>
        """
        try:
            await member.kick()
            
            embed = discord.Embed()

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        """ Ban a user 
        Usage: ban <member>
        """
        try:
            await member.ban()
            await ctx.send(f"Banned {member.name}!")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, purge: int):
        """ Purge a bunch of messages
        Usage: purge <number>"""
        try:
            await ctx.channel.purge(limit=purge+1)
            await ctx.send(f"Deleted {purge} messages!")
        except Exception as e:
            await ctx.send(e)
    
    @purge.error
    @ban.error
    @kick.error
    async def _(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument!")
        else:
            await ctx.send(f"Uh oh! `{error}`!")

def setup(client):
    client.add_cog(Mod(client))