import discord
import os
import time

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv('prefix'), description='TotalFreedom bot help command', intents=intents)

extensions = [
    "commands.moderation",
    "commands.server_commands",
    "commands.help",
    "commands.miscellaneous",
    "events"
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Extensions] {extension} loaded successfully")
        except Exception as e:
            print(f"[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Extensions] {extension} didn't load {e}")

bot.run(botToken)
