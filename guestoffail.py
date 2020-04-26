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

# Provide message to signal that discord bot has successfully connected to the server
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Prefix: ' + str(command_prefix)))
    print(f'{bot.user.name} has connected to Discord.')


@bot.event
async def on_member_join(ctx, member):
    await print(f'{member} has joined on the Great Journey...')


@bot.event
async def on_member_remove(ctx, member):
    await print(f'{member} has abandoned the Great Journey...')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found, please check =help for list of commands')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing arguments, please try again')


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

# Loads cogs in this folder only
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
