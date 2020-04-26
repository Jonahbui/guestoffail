# --------------------------------------------------------------------------------------------------
# Author: Jonah Bui & Chris Nguyen
# Date: 4/17/2020
# Purpose: a custom discord bot to fulfill the needs of my server
# Current implementations:
#  > A calculator for regular expressions
# To-do List:
# Changelogs:
# Reference code: Brad Solomon

# --------------------------------------------------------------------------------------------------
# Note: Chris
# April 26, 2020
# Event cogs have been moved to cogs/Events.py and converted to cog listener functions
# Whenever changing the prefix -which I don't know if you will ever- please make sure to update in =help function and bot's game message in Events.py

import os
import json
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

from math_expression import infix_to_postfix, calculate, parse_expression

# Load the .env file to obtain the token and name of guild
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# Initialize bot
command_prefix = '='
bot = commands.Bot(command_prefix=str(command_prefix))
bot.remove_command('help')


@bot.command(name='math', help="Solves a mathematical equation")
async def solve_expression(ctx, message, debug=False):
    # Parse the expression into a list that can be translated into postfix
    input = parse_expression(message, debug)
    postfix = infix_to_postfix(input, debug)

    # Perform calculation on the postfix expression
    value = calculate(postfix, debug)

    # Relay the value back to the user
    await ctx.send(f"{message} = {value}")


@bot.command(name='ani', help="Show off your AniList stats!")
async def ani(ctx):
    requested_user = (str(ctx.message.author))[-4:]

    f = open("users.json")
    data = json.load(f)
    f.close()

    if(requested_user in data):
        await ctx.send('You\'re on the list! Pulling AniiList information...')
    else:
        await ctx.send('You\'re not on the list, what is your AniiList username?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send('You said: ' + str(msg.content))

    # Gets the string to add to users.json
    # msg.conent
    # gets Value from key
    # user = (data["PortableRogue#4458"])
    
# Loads cogs in this folder only
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
