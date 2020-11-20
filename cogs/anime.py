import discord
import requests

from discord.ext import commands

class Anime(commands.Cog):
    """ Fat bastard. """

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def character(self, ctx, arg=None):
        """ Random anime character.
        Usage: character <name>
        """
        allCharacters = requests.get("https://anime.rovi.me/list").json()["characters"]

        if arg in allCharacters:
                character = requests.get(f"https://anime.rovi.me/random?character={arg}").json()
                
                embed = discord.Embed()
                embed.set_image(url=character["url"])

                await ctx.send(embed=embed)
        else:
            await ctx.send(f"List of allowed characters: {', '.join(allCharacters)}.")

def setup(client):
    client.add_cog(Anime(client))