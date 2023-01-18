import nextcord
from nextcord.ext import commands
import json
import sqlite3
import random

data = json.load(open("Config.json"))
TOKEN, OWNER, ADMINS, PREFIX = data['TOKEN'], data['OWNER'],data ['ADMINS'], data['PREFIX']
bot = commands.Bot(command_prefix=PREFIX, intents=nextcord.Intents.all(), help_command=None)

servers = [1063591335933775882, 1061083831014268979]
administrators = [ADMINS]
defbank = 100

economy = sqlite3.connect("banking.db")
banker = economy.cursor()

@bot.event 
async def on_ready():
    banker.execute("CREATE TABLE IF NOT EXISTS banking(player INTEGER, wallet INTEGER, bank INTEGER, net INTEGER)")
    economy.commit()
    print("Bot Is Ready")

@bot.slash_command(guild_ids=servers, description="Ask the bot to greet you.")
async def greet(interaction: nextcord.Interaction):
    await interaction.send(f"Greetings, partner.")

@bot.slash_command(guild_ids=servers, description="Create your own bank account!")
async def openaccount(interaction:nextcord.Interaction):
    user = interaction.user
    if banker.execute("SELECT * FROM banking WHERE player=?", [user.id]):
        wallets = banker.execute("SELECT wallet FROM banking WHERE player=?", [user.id]).fetchone()
        banked = banker.execute("SELECT wallet FROM banking WHERE player=?", [user.id]).fetchone()
        await interaction.send(f"{user.mention} has an account;\n userid: {user.id}, wallet: {wallets}, bank: {banked}")
    else:
        await interaction.send(f"{user.mention}, does not have an account.")
@bot.slash_command(guild_ids=servers, description="Check your account balance")
async def balance(interaction:nextcord.Interaction):
    checker = interaction.user
    if banker.execute("SELECT * FROM banking WHERE player = ?", [checker.id]):
        await interaction.send(f"{checker.mention}, this feature is not ready yet.",ephemeral=True)
    else:
        await interaction.send(f"{checker.mention}, you do not have an account yet, run /openaccount to create one now.",ephemeral=True)

bot.run(TOKEN)
