import discord
from discord.ext import commands
from discord import app_commands

import os, dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

from utils.playerbase import PlayerBaseCog
from utils.player import PlayerCog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="><>", intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(PlayerCog())
    await bot.tree.sync()
    print("Hello")

bot.run(TOKEN)