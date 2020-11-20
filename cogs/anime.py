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

    @commands.command()
    async def anime(self, ctx, *, anime=None):
        """ Show your degenerate friends your degenerate anime.
        Usage: anime <name>
        """
        searches = requests.get(f"https://api.jikan.moe/v3/search/anime?q={anime}").json()
        
        if anime:
            if "status" in searches:
                await ctx.send("Anime doesn't exist.")
            else:
                result = searches["results"][0]

                embed = discord.Embed(title=result["title"], description=result["synopsis"], url=result["url"])

                embed.add_field(name="Airing", value="Airing!" if result["airing"] else "Not airing!", inline=True)
                embed.add_field(name="Score", value=result["score"], inline=True)
                embed.add_field(name="Episodes", value=result["episodes"], inline=True)

                if result["rated"] == "PG-13" or result["rated"] == "PG":
                    embed.set_image(url=result["image_url"])
                else:
                    embed.add_field(name="**NSFW!**", value="Anime detected as NSFW.")

                await ctx.send(embed=embed)
        else:
            await ctx.send("Missing a anime!")

def setup(client):
    client.add_cog(Anime(client))