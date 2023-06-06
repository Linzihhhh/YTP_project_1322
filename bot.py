import discord
from discord.ext import commands
from discord import app_commands

import os, dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

from utils import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="><>", intents=intents)

print(os.path.abspath(os.path.join(os.path.realpath(__file__),"..")))
os.chdir(os.path.abspath(os.path.join(os.path.realpath(__file__),"..")))

@bot.event
async def on_ready():
    await bot.add_cog(PlayerCog())
    await bot.tree.sync()
    print("Hello")

bot.run(TOKEN)