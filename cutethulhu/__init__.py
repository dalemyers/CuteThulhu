import os
import re
from typing import List

import d20 as dtwenty
import discord
from discord.ext import commands

from dice import d10, d10p

with open("/Users/dalemy/Projects/cutethulhu/cutethulhu/.secret") as secret_file:
    TOKEN = secret_file.read().strip()

bot = commands.Bot(command_prefix='!')


async def get_n_plus_1_rolls(ctx) -> List[int]:
    count_string = ctx.message.content[2:].strip()

    if len(count_string) == 0:
        count = 1
    else:
        try:
            count = int(count_string)
            if count < 1:
                raise ValueError()
        except ValueError:
            await ctx.send(f"'{count_string}' was not a positive integer (number)")
            return None

    values = []

    for i in range(count + 1):
        values.append(d10p.roll())

    return values

async def delete_message(ctx):
    try:
        await ctx.message.delete()
    except:
        pass


@bot.command('b')
async def bonus_roll(ctx):
    await delete_message(ctx)
    values = await get_n_plus_1_rolls(ctx)
    if values is None:
        return
    percentile = min(values)
    unit = d10.roll()
    await ctx.send(f"{ctx.author.mention} rolled `{percentile + unit}` (min({values}) + {unit})")


@bot.command('p')
async def penalty_roll(ctx):
    await delete_message(ctx)
    values = await get_n_plus_1_rolls(ctx)
    if values is None:
        return
    percentile = max(values)
    unit = d10.roll()
    await ctx.send(f"{ctx.author.mention} rolled `{percentile + unit}` (max({values}) + {unit})")


@bot.command('r')
async def roll(ctx):
    message = ctx.message.content[2:].strip()
    await delete_message(ctx)

    if len(message) == 0:
        percentile = d10p.roll()
        unit = d10.roll()
        await ctx.send(f"{ctx.author.mention} rolled `{percentile + unit}`")
    else:
        result = dtwenty.roll(message.lower())
        result_string = str(result).replace('**', '')
        await ctx.send(f"{ctx.author.mention} rolled {result_string}")

bot.run(TOKEN)