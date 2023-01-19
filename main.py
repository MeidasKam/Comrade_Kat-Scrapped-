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
currency = "Frostbucks"
currency_emoji = ":Kalashnikov47:"

economy = sqlite3.connect("banking.db")
banker = economy.cursor()

@bot.event 
async def on_ready():
    banker.execute("CREATE TABLE IF NOT EXISTS banking(player INTEGER, wallet INTEGER, bank INTEGER, net INTEGER)")
    economy.commit()
    print("Techno kitty kitty")


def checkAccount(ctx):
    a = banker.execute("SELECT * FROM banking WHERE player=?", [ctx.user.id]).fetchone()
    if not a:
        banker.execute("INSERT INTO banking VALUES(?,?,?,?)", [ctx.user.id, 0, defbank, defbank])
        economy.commit()


def updateAccount(ctx):
    pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [ctx.user.id]).fetchone()
    pbank = banker.execute("SELECT bank FROM banking WHERE player=?", [ctx.user.id]).fetchone()
    pnet = pwallet[0] + pbank[0]
    pnet = int(pnet)
    banker.execute("UPDATE banking SET net=? WHERE player=?", [pnet, ctx.user.id])
    economy.commit()

@bot.slash_command(guild_ids=servers, description="Get a list of commands in your dms.")
async def helpme(interaction: nextcord.Interaction):
    await interaction.send(f"{interaction.user.mention}, please check your direct messages.")
    await interaction.user.send(f"The help command is in the works at this moment, stay tuned for the announcement of it being finished!")

@bot.slash_command(guild_ids=servers, description="Check your account balance")
async def balance(interaction:nextcord.Interaction):
    checkAccount(ctx=interaction)
    pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    pbank = banker.execute("SELECT bank FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    await interaction.send(f"{interaction.user.mention}'s balance:\nWallet: {pwallet[0]}\nBank: {pbank[0]}")
    updateAccount(ctx=interaction)

@bot.slash_command(guild_ids=servers, description=f"Work to earn some {currency}!")
async def work(interaction:nextcord.Interaction):
    earned = random.randint(10, 200)
    await interaction.send(f"{interaction.user.mention} has worked hard and earned {earned} {currency}!")
    pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    totalwallet = pwallet[0]
    totalwallet += earned
    banker.execute("UPDATE banking SET wallet=? WHERE player=?", [totalwallet, interaction.user.id])
    economy.commit()

@bot.slash_command(guild_ids=servers, description="Ask the bot to greet you.")
async def greet(interaction: nextcord.Interaction, target: nextcord.Member):
    if interaction.user.id == target.id:
        await interaction.send(f"{interaction.user.mention} has decided to greet themselves.")
    else:
        await interaction.send(f"{interaction.user.mention} sends their greetings to {target.mention}")

@bot.slash_command(guild_ids=servers, description="Shoot someone with an AK")
async def gun(interaction: nextcord.Interaction, target: nextcord.Member):
    if interaction.user.id == target.id:
        await interaction.send(f"{interaction.user.mention} has commited suicide.")
    else:
        await interaction.send(f"{interaction.user.mention} <:Kalashnikov47:1065609179173244998> {target.mention}")

bot.run(TOKEN)
