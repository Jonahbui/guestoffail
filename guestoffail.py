# --------------------------------------------------------------------------------------------------
# Author: Jonah Bui & Chris Nguyen
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

# Provide message to signal that discord bot has successfully connected to the server
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Prefix: ' + str(command_prefix)))
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


@bot.command(name='clear', help='Clears messages in a chat channel; Default = 1')
async def clear(ctx, amount=2):
    # delects message that requested command and 1 addition message if using default of 2
    await ctx.channel.purge(limit=amount)
    await ctx.send('Cleaning message(s)...')
    time.sleep(1)
    await ctx.channel.purge(limit=1)


@bot.command(name='suggest', help='Submit a suggestion/ support ticket')
async def suggest(ctx):
    await ctx.send('Suggestion form: https://forms.gle/aAWDtthnARBi69as8')


@bot.command(name='math', help="Solves a mathematical equation")
async def solve_expression(ctx, message, debug=False):
    # Parse the expression into a list that can be translated into postfix
    input = parse_expression(message, debug)
    postfix = infix_to_postfix(input, debug)

    # Perform calculation on the postfix expression
    value = calculate(postfix, debug)

    # Relay the value back to the user
    await ctx.send(f"{message} = {value}")

# Loads cogs in this folder only
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command(name='load', help='loads cogs after removal')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(str(extension) + ' loaded!')


@bot.command(name='unload', help='unloads cog from bot')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(str(extension) + ' unloaded!')


@bot.command(name='refresh', help='refresh a cog that\'s misbehaving')
async def refresh(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    time.sleep(1)
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(str(extension) + ' reloaded!')

bot.run(TOKEN)
