#--------------------------------------------------------------------------------------------------
# Author: Jonah Bui
# Date: 4/17/2020
# Purpose: a custom discord bot to fulfill the needs of my server
# Current implementations:
#  > A calculator for regular expressions
# To-do List:
# Changelogs:
# Reference code: Brad Solomon

import os
import time
from dotenv import load_dotenv
from math_expression import infix_to_postfix, calculate, parse_expression
import discord
from discord.ext import commands, tasks

# Load the .env file to obtain the token and name of guild
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Initialize bot
from discord.ext import commands
bot = commands.Bot(command_prefix='=')

# Provide message to signal that discord bot has successfully connected to the server
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord.')

@bot.event
async def on_member_join(ctx, member):
    await ctx.send(f'{member} has joined on the Great Journey...')

@bot.event
async def on_member_remove(ctx, member):
    await ctx.send(f'{member} has abandoned the Great Journey...')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found, please check =help for list of commands')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing arguments, please try again')

@bot.command(name='ping', help="Check the ping to the bot")
async def ping(ctx):
    await ctx.send(f'Current ping:  {round(bot.latency * 1000)}ms')


@bot.command(name='math', help="Solves a mathematical equation")
async def solve_expression(ctx, message, debug=False):
    # Parse the expression into a list that can be translated into postfix
    input = parse_expression(message, debug)
    postfix = infix_to_postfix(input, debug)

    # Perform calculation on the postfix expression
    value = calculate(postfix, debug)

    # Relay the value back to the user
    await ctx.send(f"{message} = {value}")


bot.run(TOKEN)
