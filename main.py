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

@bot.slash_command(guild_ids=servers, description="Withdraw an ammount from your bank")
async def withdraw(interaction:nextcord.Interaction, amount: int):
    checkAccount(ctx=interaction)
    pbank = banker.execute("SELECT bank FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    pbank = pbank[0]
    if amount >= pbank+1:
        await interaction.send(f"{interaction.user.mention} you currently do not have enough money in your bank for this transaction.")
    else:
        pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
        pwallet = pwallet[0]
        pwallet += amount
        banker.execute("UPDATE banking SET wallet=? WHERE player=?", [pwallet, interaction.user.id])
        pbank = pbank - amount
        banker.execute("UPDATE banking SET bank=? WHERE player=?", [pbank, interaction.user.id])
        economy.commit()
        bankrem = banker.execute("SELECT bank FROM banking WHERE player=?", [interaction.user.id]).fetchone()
        bankrem = bankrem[0]
        await interaction.send(f"{interaction.user.mention} has withdrawn {amount} {currency}.\nRemaining bank balance is: {bankrem} {currency}")

@bot.slash_command(guild_ids=servers, description="Withdraw an ammount from your bank")
async def deposit(interaction:nextcord.Interaction, amount: int):
    checkAccount(ctx=interaction)
    pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    pwallet = pwallet[0]
    if amount >= pwallet+1:
        await interaction.send(f"{interaction.user.mention} you currently do not have enough money in your wallet for this transaction.")
    else:
        pbank = banker.execute("SELECT bank FROM banking WHERE player=?", [interaction.user.id]).fetchone()
        pbank = pbank[0]
        pbank += amount
        banker.execute("UPDATE banking SET bank=? WHERE player=?", [pbank, interaction.user.id])
        pwallet = pwallet - amount
        banker.execute("UPDATE banking SET wallet=? WHERE player=?", [pwallet, interaction.user.id])
        economy.commit()
        walletrem = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
        walletrem = walletrem[0]
        await interaction.send(f"{interaction.user.mention} has deposited {amount} {currency} into their bank account.\nRemaining wallet balance is: {walletrem} {currency}")

@bot.slash_command(guild_ids=servers, description=f"Work to earn some {currency}!")
async def work(interaction:nextcord.Interaction):
    checkAccount(ctx=interaction)
    earned = random.randint(10, 200)
    await interaction.send(f"{interaction.user.mention} has worked hard and earned {earned} {currency}!")
    pwallet = banker.execute("SELECT wallet FROM banking WHERE player=?", [interaction.user.id]).fetchone()
    totalwallet = pwallet[0]
    totalwallet += earned
    banker.execute("UPDATE banking SET wallet=? WHERE player=?", [totalwallet, interaction.user.id])
    economy.commit()

@bot.slash_command(guild_ids=servers, description="The bot's shop.")
async def shop(interaction: nextcord.Interaction, page: int):
    checkAccount(ctx=interaction)
    minpages = 1
    maxpages = 1
    if page >= maxpages+1 or page <= minpages-1:
        await interaction.send(f"{interaction.user.mention} you may not select a page that does not yet exist.",ephemeral=True)
    else:
        if page == 1:
            await interaction.send(f"Shop: Page {page}/{maxpages}\n1. :fortune_cookie:-Fortune Cookie")

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
        await interaction.send(f"{interaction.user.mention} <:Kalashnikov47:1065609179173244998><:HEADSHOT:1065758421510524958> {target.mention}")

bot.run(TOKEN)
