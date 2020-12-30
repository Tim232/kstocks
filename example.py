from kstocks import Stocks
from discord.ext import commands

bot = commands.Bot(command_prefix="!!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


stocks = Stocks()


@bot.command()
async def kospi(ctx):
    source = await stocks.KOSPI()
    await ctx.send(source)


@bot.command()
async def kosdaq(ctx):
    source = await stocks.KOSDAQ()
    await ctx.send(source)


bot.run("token")
