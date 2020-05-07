import discord
from discord.ext import commands, tasks

import time


class administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help="Check the ping to the bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f'Current ping:  {round(self.bot.latency * 1000)}ms')

    @commands.command(name='clear', help='Clears messages in a chat channel; Default = 1')
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_role('[X2]Garbage Man')
    async def clear(self, ctx, amount=2):
        '''delects message that requested command and 1 addition message if using default of 2'''

        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleaning message(s)...')
        time.sleep(1)
        await ctx.channel.purge(limit=1)

    @commands.command(name='contact', help='Submit a suggestion/ support ticket')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def contact(self, ctx):
        await ctx.send('Suggestion form: https://forms.gle/aAWDtthnARBi69as8')

    #Will send a notification to the SERVER OWNER in chat and in DMs
    @commands.command(name='invite', help= "Create an invite link for the server")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def invite(self, ctx):
        invite_link = await ctx.channel.create_invite(max_age = 300)
        owner = ctx.message.guild.owner
        server = ctx.message.guild.name

        await ctx.send(f"An invite link has been created, expires in 5 minutes {owner.mention}")
        await owner.send(f'Someone created an invite link in {server}')
        await ctx.send(invite_link)

    @commands.command(name='refresh', help="refresh a cog that\'s missbehaving")
    @commands.has_role('[X2]Garbage Man')
    async def refresh(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        time.sleep(1)
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(str(extension) + ' reloaded!')

    @commands.command(name='unload', help='unload cog from bot')
    @commands.has_role('[X2]Garbage Man')
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(str(extension) + ' unloaded!') 


#
#
#   This is not working, the user is not getting removed from server
#   Throws a 'Generic error'
#
    @commands.command(name='kick', help='Kicks a user from the server')
    @commands.has_role('[X2]Garbage Man')
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        owner = ctx.message.guild.owner
        server = ctx.message.guild.name

        await ctx.send(f'{member.mention} was kicked from the server, see you later! @here {owner.mention}')
        await owner.send(f'{member} was kicked from {server}')
        await member.kick(reason=reason)

    @commands.command(name='mute', help='Mute a user in a voice channel')
    @commands.has_role('[X2]Garbage Man')
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await member.mute(reason=reason)
        await ctx.send(f'{member} has been muted @here')

    @commands.command(name='load', help='load cog after removal')
    @commands.has_role('[X2]Garbage Man')
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(str(extension) + ' loaded!')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        '''Custom help command'''

        author = ctx.message.author

        embed = discord.Embed(colour=discord.Color.green())
        embed.set_author(name='Available commands:')
        embed.add_field(name='=info', value="Show server statistics", inline=False)
        embed.add_field(name='=contact', value='Submit suggestions/ support tickets here', inline=False)
        embed.add_field(name='=ping', value='Check your ping to the bot', inline=False)
        embed.add_field(name='=invite', value = 'Create an invite link to the server (Cooldown: 60 mins)', inline=False)
        embed.add_field(name='=clear #number',value='Clear chat | Default: 1 message (Role restricted)', inline=False)
        embed.add_field(name='=kick', value='Kick a user (Role restricted)', inline=False)
        embed.add_field(name='=mute', value='Mute a user (Role restricted)', inline=False)

        embed.add_field(name='=math #expression', value='Calculator to solve basic math problems', inline=False)
        embed.add_field(name='=ani', value='Boast your Anilist stats to the server!', inline=False)
        embed.add_field(name='=play', value='Play some of Jonah\'s local audio files', inline=False)
        embed.add_field(name='=leave', value='Stop music playback and bot leaves VC', inline=False)

        embed.add_field(name='=spyfall', value='Start a game instance of Spyfall', inline=False)

        await ctx.send(author, embed=embed)

    # Bot information stat tracker
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        '''Shows server info'''

        server = ctx.message.guild
        roles = str(len(server.roles))
        emojis = str(len(server.emojis))
        channels = str(len(server.channels))

        embeded = discord.Embed(title=server.name, description='Server Info', color=discord.Color.green())
        embeded.set_thumbnail(url=server.icon_url)
        embeded.add_field(name="Created on:", value=server.created_at.strftime('%d %B %Y at %H:%M UTC-6') + '| Rip LNG-1', inline=False)
        embeded.add_field(name="Server ID:", value=server.id, inline=False)
        embeded.add_field(name="Users on server:", value=server.member_count, inline=True)
        embeded.add_field(name="Server owner:", value=server.owner, inline=True)
        embeded.add_field(name="Server Region:", value=server.region, inline=True)

        embeded.add_field(name="Role Count:", value=roles, inline=True)
        embeded.add_field(name="Emoji Count:", value=emojis, inline=True)
        embeded.add_field(name="Channel Count:", value=channels, inline=True)

        embeded.add_field(name="Bot created and maintained by:", value="@Rat Chef#3342, @PortableRogue#4458", inline=False)

        await ctx.send(embed=embeded) 


def setup(bot):
    bot.add_cog(administration(bot))
