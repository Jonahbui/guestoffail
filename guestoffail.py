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
from dotenv import load_dotenv
from math_expression import infix_to_postfix, calculate, parse_expression

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

@bot.command(name='=', help="Solves a mathematical equation")
async def solve_expression(ctx, message, debug=False):
    # Parse the expression into a list that can be translated into postfix
    input = parse_expression(message, debug)
    postfix = infix_to_postfix(input, debug)

    # Perform calculation on the postfix expression
    value = calculate(postfix, debug)

    # Relay the value back to the user
    await ctx.send(f"{message} = {value}")

bot.run(TOKEN)