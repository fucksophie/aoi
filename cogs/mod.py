import json
import discord

from discord.ext import commands

config = json.load(open("config.json"))

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        try:
            await member.kick()
            await ctx.send(f"Kicked {member.name}!")
        except Exception as e:
            await ctx.send(e)
    
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        try:
            await member.ban()
            await ctx.send(f"Banned {member.name}!")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, purge: int):
        try:
            await ctx.channel.purge(limit=purge+1)
            await ctx.send(f"Deleted {purge} messages!")
        except Exception as e:
            await ctx.send(e)

def setup(client):
    client.add_cog(Mod(client))