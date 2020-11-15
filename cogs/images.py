import json
import requests
import discord
import sys

from discord.ext import commands

config = json.load(open("config.json"))

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def character(self, ctx, arg=None):
        allCharacters = requests.get("https://anime.rovi.me/list").json()["characters"]

        if arg in allCharacters:
                character = requests.get(f"https://anime.rovi.me/random?character={arg}").json()
                
                embed = discord.Embed()
                embed.set_image(url=character["url"])

                await ctx.send(embed=embed)
        else:
            await ctx.send(f"List of allowed characters: {', '.join(allCharacters)}.")


def setup(client):
    apiList = requests.get("https://api.chewey-bot.top/endpoints").json()["data"]
    cog = Images(client)
    
    for name in apiList:
        @commands.command(name=name)
        async def temp(self, ctx):
                data = requests.get(f"https://api.chewey-bot.top/{ctx.command.name}?auth={config['chewey']}").json()
                embed = discord.Embed()
                embed.set_image(url=data["data"])

                await ctx.send(embed=embed)

        temp.cog = cog

        client.add_command(temp)

    client.add_cog(cog)