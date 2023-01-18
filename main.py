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

#@bot.before_invoke
#async def accountcheck():
#    await print("A command has been used.")

#@bot.after_invoke
#async def accountupdate():
#   await print("A command has been used.")

@bot.slash_command(guild_ids=servers, description="Ask the bot to greet you.")
async def greet(interaction: nextcord.Interaction):
    await interaction.send(f"Hello, {interaction.user.mention}.")

@bot.slash_command(guild_ids=servers, description="Create your own bank account!")
async def openaccount(interaction:nextcord.Interaction):
    user = interaction.user
    a = banker.execute("SELECT * FROM banking WHERE player=?", [user.id]).fetchone()
    if a:
        networth = banker.execute("SELECT net FROM banking WHERE player=?", [user.id]).fetchone()
        await interaction.send(f"{user.mention} You currently have an account with this bot.\nYour current total balance is: {networth}", ephemeral=True)
    else:
        await interaction.send(f"{user.mention} An account has been created for you.")
        banker.execute("INSERT INTO banking VALUES(?, ?, ?, ?)", [user.id, 0, defbank, defbank])
        economy.commit()

@bot.slash_command(guild_ids=servers, description="Check your account balance")
async def balance(interaction:nextcord.Interaction):
    checker = interaction.user
    a = banker.execute("SELECT * FROM banking WHERE player=?", [checker.id]).fetchone()
    if a:
        pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [checker.id]).fetchone()
        pbank = banker.execute("SELECT bank FROM banking WHERE player=?", [checker.id]).fetchone()
        await interaction.send(f"{checker.mention}'s balance:\nWallet: {pwallet}\nBank: {pbank}")
    else:
        await interaction.send(f"{checker.mention} you must create an account for yourself using /openaccount to be able to use my commands.")

bot.run(TOKEN)
