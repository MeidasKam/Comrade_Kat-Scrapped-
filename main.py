import nextcord
from nextcord.ext import commands
import json
import sqlite3
import random

data = json.load(open("Config.json"))
TOKEN, OWNER, HOME, TESTING, PREFIX = data['TOKEN'], data['OWNER'], data['HOME'], data['TESTING'], data['PREFIX']
bot = commands.Bot(command_prefix=PREFIX, intents=nextcord.Intents.all(), help_command=None)

@bot.event 
async def on_ready():
    print("Bot Is Ready")

bot.run(TOKEN)