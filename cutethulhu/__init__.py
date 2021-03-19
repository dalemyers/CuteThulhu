import os
import re
from typing import List

import d20 as dtwenty
import discord
from discord.ext import commands

try:
    from .dice import d10, d10p, d100
except ImportError:
    # TODO: Figure out this
    from dice import d10, d10p, d100


bot = commands.Bot(command_prefix="!")


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


@bot.command("b")
async def bonus_roll(ctx):
    await delete_message(ctx)
    values = await get_n_plus_1_rolls(ctx)
    if values is None:
        return
    percentile = min(values)
    unit = d10.roll()
    await ctx.send(
        f"{ctx.author.mention} rolled `{percentile + unit}` (min({values}) + {unit})"
    )


@bot.command("p")
async def penalty_roll(ctx):
    await delete_message(ctx)
    values = await get_n_plus_1_rolls(ctx)
    if values is None:
        return
    percentile = max(values)
    unit = d10.roll()
    await ctx.send(
        f"{ctx.author.mention} rolled `{percentile + unit}` (max({values}) + {unit})"
    )


def skill_parse(string):
    match = re.match(r"(\d{1,2})(?:\s*\+\s*(\d*)?(b|p))?", string.lower())
    if not match:
        return None, None

    skill_str = match.group(1)
    dice_type = match.group(3)

    if dice_type is None:
        extra_count = 0
    else:
        if match.group(2) is None or match.group(2) == "":
            extra_count = 1
        else:
            extra_count = int(match.group(2))

    skill_value = int(skill_str)

    if dice_type == "p":
        extra_count *= -1

    return skill_value, extra_count


@bot.command("s")
async def skill_check(ctx):
    skill_value, extra_count = skill_parse(ctx.message.content[2:].strip())
    await delete_message(ctx)

    if skill_value is None or extra_count is None:
        await ctx.send(f"{ctx.author.mention} Could not parse '{value_string}'")
        return

    if extra_count == 0:
        dice_notation = "1d100"
    elif extra_count > 0:
        dice_notation = f"{extra_count + 1}d%kl1 + 1d10"
    else:
        dice_notation = f"{-extra_count + 1}d%kh1 + 1d10"

    result = dtwenty.roll(dice_notation)

    qualifier = ""

    if (result.total == 100 and skill_value >= 50) or (
        result.total >= 96 and skill_value < 50
    ):
        qualifier = "Fumble"
    elif result.total > skill_value:
        qualifier = "Failure"
    elif result.total == 1:
        qualifier = "Critical Success"
    elif result.total <= (skill_value / 5):
        qualifier = "Extreme Success"
    elif result.total <= (skill_value / 2):
        qualifier = "Hard Success"
    else:
        qualifier = "Success"

    await ctx.send(
        f"{ctx.author.mention} rolls against skill of {skill_value}: {result} [{qualifier}]"
    )


@bot.command("r")
async def roll(ctx):
    message = ctx.message.content[2:].strip()
    await delete_message(ctx)

    if len(message) == 0:
        percentile = d10p.roll()
        unit = d10.roll()
        await ctx.send(f"{ctx.author.mention} rolled `{percentile + unit}`")
    else:
        result = dtwenty.roll(message.lower())
        result_string = str(result).replace("**", "")
        await ctx.send(f"{ctx.author.mention} rolled {result_string}")


def generate_characteristic(ctx, characteristic):
    if characteristic in ["STR", "CON", "DEX", "APP", "POW"]:
        return dtwenty.roll("3d6*5")
    elif characteristic in ["SIZ", "INT", "EDU"]:
        return dtwenty.roll("(2d6+6)*5")
    else:
        return None


@bot.command("gen")
async def gen(ctx):
    message = ctx.message.content[4:].strip()
    await delete_message(ctx)

    characteristic = message.upper()

    output = f"{ctx.author.mention} rolled for"

    if characteristic == "ALL":
        output += ":\n"
        total = 0
        for c in ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU"]:
            result = generate_characteristic(ctx, c)
            total += result.total
            output += f"{c}: {result}\n"
        output += f"**TOTAL:** `{total}`"
    else:
        output += f" {characteristic}: {generate_characteristic(ctx, characteristic)}"

    await ctx.send(output)


def run():
    current_file_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file_path)
    secrets_path = os.path.join(current_folder, ".secret")
    with open(secrets_path) as secret_file:
        token = secret_file.read().strip()
    bot.run(token)


if __name__ == "__main__":
    run()