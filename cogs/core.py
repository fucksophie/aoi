import json
import discord

from discord.ext import commands

config = json.load(open("config.json"))

class Core(commands.Cog):
    """ Main commands of the bot """

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ms"])
    async def ping(self, ctx):
        """ Latency of the bot """

        t = await ctx.send('Pong!')
        await t.edit(content=f"Pong! Took {(t.created_at).second}ms!")
    
    @commands.command()
    async def eval(self, ctx, arg):
        """ Eval python """

        if ctx.author.id == config["owner"]:
            evaled = eval(arg)

            if evaled:
                await ctx.send(f"```{evaled}```")
            else:
                await ctx.send("None")
    
    @commands.command(aliases=["r"])
    async def reload(self, ctx, arg):
        """ Reload a single module """

        arg = f"cogs.{arg}"

        if ctx.author.id == config["owner"]:
            self.client.reload_extension(arg)
            await ctx.send(f"Reloaded {arg}")

    @commands.command(aliases=["invite"])
    async def info(self, ctx):
        """ Info about this bot """

        commit_id = open(".git/FETCH_HEAD", "r").read().split()[0]
        discord_py = discord.__version__

        embed = discord.Embed(title=f"{self.client.user.name} Information")
        embed.add_field(name="Commit ID", value=commit_id, inline=True)
        embed.add_field(name="Discord.py Version", value=discord_py, inline=True)
        embed.add_field(name="Owner", value=f"<@!{config['owner']}>", inline=True)
        embed.add_field(name="Support Server", value="[Click here](https://discord.gg/aYX3xmTrWp)", inline=True)
        embed.add_field(name="Invite", value=f"[Click here](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=268561478&scope=bot)", inline=True)
        embed.add_field(name="Source", value="[Click here](https://github.com/lukeacat/aoi/)", inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Core(client))