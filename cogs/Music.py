import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import eyed3
from eyed3.plugins.art import ArtFile, pilImage
from os import listdir
import PIL
from PIL import Image
from io import BytesIO
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError

class songinfo:
    def __init__(self, title, artist, album, album_artist, track_num, cover, dir):
        self.title = title
        self.artist = artist
        self.album = album
        self.album_artist = album_artist
        self.track_num = track_num
        self.cover = cover

async def print_playlist(playlist):
    for x in playlist:
        print(x) 

def get_music_from_directory():
    playlist = {}
    DISCORD_MUSIC_LOCATION = os.getenv("DISCORD_MUSIC_LOCATION")
    if os.path.exists(DISCORD_MUSIC_LOCATION):
        # Get all the songs in a directory that are mp3 files
        for file in listdir(DISCORD_MUSIC_LOCATION):
            try:
                if os.path.isfile(DISCORD_MUSIC_LOCATION+'\\'+file):
                    # Store path to reference mp3 file
                    dir = DISCORD_MUSIC_LOCATION+'\\'+file
                    # Get album author and track name
                    # Use album author as key
                    # Use track name as ordered pair with filename
                    tags = ID3(DISCORD_MUSIC_LOCATION+"\\"+file)
                    image = tags.get("APIC:").data
                    cover = Image.open(BytesIO(image))
                    audiofile = eyed3.load(DISCORD_MUSIC_LOCATION+"\\"+file)
                    song = songinfo(
                        audiofile.tag.title, audiofile.tag.artist, audiofile.tag.album,
                        audiofile.tag.album_artist, audiofile.tag.track_num, cover, dir
                    )
                    if audiofile.tag.artist not in playlist:
                        playlist[audiofile.tag.artist] = []
                        playlist[audiofile.tag.artist].append(song)
                    else:
                        playlist[audiofile.tag.artist].append(song)
                    #image.show()
            except IOError:
                print(f"Error: could not load file {file}\n")
            except AttributeError:
                print(f"Error: album cover not found in {file}\n")
            except ID3NoHeaderError:
                print(f"Error: invalid file format detected")
    return playlist

# Class music inherits the Cog class
class Music(commands.Cog):
    # Constructor
    def __init__(self, bot, playlist):
        self.bot = bot
        self.playlist = playlist

    @commands.command(name='test')
    async def inside_template(self, ctx):
        await ctx.send("inside_template")
        await print_playlist(self.playlist)

# Every cog just have a setup function
def setup(bot):
    playlist = get_music_from_directory()
    bot.add_cog(Music(bot, playlist))
