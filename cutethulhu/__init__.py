import os
import random
import re

import d20
import discord
from discord.ext import commands

with open("/Users/dalemy/Projects/cutethulhu/cutethulhu/.secret") as secret_file:
    TOKEN = secret_file.read().strip()

random.seed()

#client = discord.Client()
#
#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')
#
#client.run(TOKEN)

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command('r')
async def roll(ctx):
    message = ctx.message.content[2:].strip()

    await ctx.message.delete()

    await ctx.send(d20.roll(message))

bot.run(TOKEN)