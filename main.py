import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

DISCORD_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Готов к труду и обороне!")

bot.run("DISCORD_TOKEN")