import discord
import json
import os

from discord.ext import commands
from pretty_help import PrettyHelp

config = json.load(open("config.json"))
client = commands.Bot(command_prefix=config["prefix"], help_command=PrettyHelp())

@client.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@client.event
async def on_ready():
    print(f"{client.user.name} | Running")
    await client.change_presence(activity=discord.Game(name=f"with camping equipment | {config['prefix']}help"))

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(config["token"])