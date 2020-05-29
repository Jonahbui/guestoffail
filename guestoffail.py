# Written with discord.py rewrite version 1.2.5

# --------------------------------------------------------------------------------------------------
# Author: Jonah Bui & Chris Nguyen
# Date: 4/17/2020
# Purpose: a custom discord bot to fulfill the needs of my server
# Current implementations:
#  > A calculator for regular expressions
# To-do List:
# Changelogs:
# Reference code: Brad Solomon (Who's brad?)
# --------------------------------------------------------------------------------------------------
# Note: Chris
# April 26, 2020
# Event cogs have been moved to cogs/Events.py and converted to cog listener functions
# Whenever changing the prefix -which I don't know if you will ever- please make sure to update in =help function and bot's game message in Events.py

import json
import os
import time

import discord
import requests
import youtube_dl
from discord.ext import commands, tasks
from dotenv import load_dotenv

from math_expression import calculate, infix_to_postfix, parse_expression

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


#   NOTICE
#   Scrapy, BeautifulSoup will not work; don't waste your time
#   Need to work with Selenium as the data is embeded in Dyanmic JS
#   Headless browser ref: https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
@bot.command(name='ani', help="Show off your AniList stats!")
async def ani(ctx):
    requested_user = (str(ctx.message.author))[-4:]

    f = open("users.json")
    data = json.load(f)
    f.close()

    if(requested_user in data):
        await ctx.send('You\'re on the list! Currently, this is still WIP so I can\'t show you anything just yet')
    else:
        await ctx.send('You\'re not on the list, what is your AniiList username?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

        new_member = {str(requested_user): str(msg.content)}
        data.update(new_member)

        json_object = json.dumps(data, indent=4)
        with open("users.json", "w") as f:
            f.write(json_object)
        f.close()
        await ctx.send('Added!')
        await ctx.send('You\'re on the list! Currently, this is still WIP so I can\'t show you anything just yet')

#ref: https://stackoverflow.com/questions/56031159/discord-py-rewrite-what-is-the-source-for-youtubedl-to-play-music
@bot.command(name='play')
async def play(ctx, url: str):
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return

    await ctx.send("Getting everything ready, one second")
    print(f'{ctx.message.author} has requested to download a song from the bot')

    voice= discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegAudio('song.mp3'))
    voice.volume = 100
    voice.is_playing()

    
    #
    #   To Jonah: Insert your commands here to play your music (You're going to need ffmpeg to stream your mp3 files to the bot)
    #   Also, stop playback of audio in =leave 
    #

@bot.command(name='leave')
async def leave(ctx):
    for vc in bot.voice_clients:
        if vc.guild == ctx.message.guild:
            await vc.disconnect()
            return
    await ctx.send("I am currently not in a voice channel")

@bot.command(name='secretSauce')
@commands.has_role('[X2]Garbage Man')
async def secretSauce(ctx):
    channel = ctx.author.voice.channel
    while True:
        vc = await channel.connect()
        await vc.disconnect()

@bot.command(name='rename')
async def rename(ctx, channel:discord.VoiceChannel, *, new_name):
    await channel.edit(name=new_name)

# Loads cogs in this folder only
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
