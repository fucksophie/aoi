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
            
            embed = discord.Embed(
                title="Member kicked!",
                description=f"<@!{ctx.author.id}> has kicked <@!{member.id}>!")
            
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
            
            embed = discord.Embed(
                title="Member banned!",
                description=f"<@!{ctx.author.id}> has banned <@!{member.id}>!")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, purge: int):
        """ Purge a bunch of messages
        Usage: purge <number>
        """
        try:
            await ctx.channel.purge(limit=purge+1)
            embed = discord.Embed(
                title="Purged!",
                description=f"Purged {purge} messages!")
            
            await ctx.send(embed=embed, delete_after=3)
        except Exception as e:
            await ctx.send(e)
   
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        """ Warn a user
        Usage: warn <member> <reason>
        """

        embed = discord.Embed(
            title=f"You've been warned.",
            description=f"For `{reason}` in {ctx.guild.name}"
        )
        
        await member.send(embed=embed)

        embed = discord.Embed(title=f"Warned {member.name}!")
        
        await ctx.send(embed=embed)
        

    @warn.error
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