from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def ping(self, ctx):
        t = await ctx.send('Pong!')
        await t.edit(content=f"Pong! Took {(t.created_at).second}ms!")
    
    @commands.command()
    async def eval(self, ctx, arg):
        if ctx.author.id == 384342022955466753:
            evaled = eval(arg)

            if evaled:
                await ctx.send(f"```{evaled}```")
            else:
                await ctx.send("None")
        
def setup(client):
    client.add_cog(Core(client))