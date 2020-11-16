import json
import discord
from discord.ext import commands

config = json.load(open("config.json"))

class Core(commands.Cog):
    """ Commands that almost every bot has """
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def ping(self, ctx):
        """ Get the latency of the bot. """
        t = await ctx.send('Pong!')
        await t.edit(content=f"Pong! Took {(t.created_at).second}ms!")
    
    @commands.command()
    async def eval(self, ctx, arg):
        """ Eval Python (only Owner) """
        if ctx.author.id == config["owner"]:
            evaled = eval(arg)

            if evaled:
                await ctx.send(f"```{evaled}```")
            else:
                await ctx.send("None")
    
    @commands.command()
    async def reload(self, ctx, arg):
        """ Reload a Single module (only Owner) """
        arg = f"cogs.{arg}"

        if ctx.author.id == config["owner"]:
            self.client.reload_extension(arg)
            await ctx.send(f"Reloaded {arg}")

    @commands.command()
    async def faq(self, ctx):
        """ Frequently Asked Questions """
        await ctx.send(
        "Q: `Music?`\n" + 
        "A: Sorry, but Music will probably never come to this bot. On the system that I'm hosting it on, it is impossible run Music on.\n" +
        "Q: `Why this bot?`\n" +
        "A: I wanted to create a simple multifunctional bot that WORKS, so I did.")

def setup(client):
    client.add_cog(Core(client))