import json
import discord
from discord.ext import commands

config = json.load(open("config.json"))

class Core(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def ping(self, ctx):
        t = await ctx.send('Pong!')
        await t.edit(content=f"Pong! Took {(t.created_at).second}ms!")
    
    @commands.command()
    async def eval(self, ctx, arg):
        if ctx.author.id == config["owner"]:
            evaled = eval(arg)

            if evaled:
                await ctx.send(f"```{evaled}```")
            else:
                await ctx.send("None")
    
    @commands.command()
    async def reload(self, ctx, arg):
        if ctx.author.id == config["owner"]:
            self.client.reload_extension(arg)
            await ctx.send(f"Reloaded {arg}")

def setup(client):
    client.add_cog(Core(client))