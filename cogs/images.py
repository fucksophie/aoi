import json
import requests
import discord
import sys
import random

from discord.ext import commands

config = json.load(open("config.json"))

class Images(commands.Cog):
    """ Just completely random images. """
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def xkcd(self, ctx, num: int=None):
        """ Funny nerd comics. 
        Usage: xkcd [num]
        """
        latestComic = requests.get("https://xkcd.com/info.0.json").json()["num"]
              
        if not num:
            comic = requests.get(f"https://xkcd.com/{random.randint(1, latestComic)}/info.0.json").json()

            embed = discord.Embed(title=f"{comic['safe_title']} (R {comic['num']})", description=comic['alt'])
            embed.set_image(url=comic["img"])
                
            await ctx.send(embed=embed)
        else:
            if num >= 1 and num <= latestComic:

                comic = requests.get(f"https://xkcd.com/{num}/info.0.json").json()
                
                embed = discord.Embed(title=f"{comic['safe_title']} ({num})", description=comic['alt'])
                embed.set_image(url=comic["img"])
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Number is either less than 1, or higher than {latestComic}.")
    
    @commands.command()
    async def images(self, ctx, arg=None):
        """ Random wacky images.
        Usage: images [image]
        """
        allImages = requests.get("https://api.chewey-bot.top/endpoints").json()["data"]

        if arg in allImages:
            data = requests.get(f"https://api.chewey-bot.top/{arg}?auth={config['chewey']}").json()

            embed = discord.Embed()
            embed.set_image(url=data["data"])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"List of allowed images: {', '.join(allImages)}.")

def setup(client):
    client.add_cog(Images(client))