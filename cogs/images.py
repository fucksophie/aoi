import json
import requests
import discord
import sys

from discord.ext import commands

config = json.load(open("config.json"))

async def handleCommand(ctx, name):
    data = requests.get(f"https://api.chewey-bot.top/{name}?auth={config['chewey']}").json()
    embed = discord.Embed(title=name)
    embed.set_image(url=data["data"])

    await ctx.send(embed=embed)

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    test = requests.get("https://api.chewey-bot.top/endpoints").json()["data"]
    cog = Images(client)
    
    for name in test:
        @commands.command(name=name)
        async def temp(self, ctx):
            await handleCommand(ctx, ctx.command.name)

        temp.cog = cog

        client.add_command(temp)

    client.add_cog(cog)