import discord
import json
import os
import random

from discord.ext import commands

config = json.load(open("config.json"))
client = commands.Bot(command_prefix=config["prefix"])

client.help_command = commands.MinimalHelpCommand()

@client.event
async def on_ready():
    print(f"{client.user.name} | Running")
    await client.change_presence(activity=discord.Game(name="with camping equipment | <help"))

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(config["token"])