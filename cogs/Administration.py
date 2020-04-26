import discord
from discord.ext import commands, tasks

import time


class administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help="Check the ping to the bot")
    async def ping(self, ctx):
        await ctx.send(f'Current ping:  {round(self.bot.latency * 1000)}ms')

    @commands.command(name='clear', help='Clears messages in a chat channel; Default = 1')
    async def clear(self, ctx, amount=2):
        '''delects message that requested command and 1 addition message if using default of 2'''

        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleaning message(s)...')
        time.sleep(1)
        await ctx.channel.purge(limit=1)

    @commands.command(name='contact', help='Submit a suggestion/ support ticket')
    async def contact(self, ctx):
        await ctx.send('Suggestion form: https://forms.gle/aAWDtthnARBi69as8')

    @commands.command(pass_context=True)
    async def help(self, ctx):
        '''Custom help command'''

        author = ctx.message.author

        embed = discord.Embed(colour=discord.Color.green())
        embed.set_author(name='Available commands:')
        embed.add_field(name='=info', value="Show server statistics", inline=False)
        embed.add_field(name='=contact', value='Submit suggestions/ support tickets here', inline=False)
        embed.add_field(name='=ping', value='Check your ping to the bot', inline=False)
        embed.add_field(name='=clear #number',value='Clear chat | Default: 1 message', inline=False)

        embed.add_field(name='=math #expression', value='Calculator to solve basic math problems', inline=False)
        embed.add_field(name='=Ani', value='Boast your Anilist stats to the server!', inline=False)

        await ctx.send(author, embed=embed)

    # Bot information stat tracker
    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Shows server info"""

        server = ctx.message.guild
        roles = str(len(server.roles))
        emojis = str(len(server.emojis))
        channels = str(len(server.channels))

        embeded = discord.Embed(title=server.name, description='Server Info', color=discord.Color.green())
        embeded.set_thumbnail(url=server.icon_url)
        embeded.add_field(name="Created on:", value=server.created_at.strftime('%d %B %Y at %H:%M UTC+3'), inline=False)
        embeded.add_field(name="Server ID:", value=server.id, inline=False)
        embeded.add_field(name="Users on server:", value=server.member_count, inline=True)
        embeded.add_field(name="Server owner:", value=server.owner, inline=True)
        embeded.add_field(name="Server Region:", value=server.region, inline=True)

        embeded.add_field(name="Role Count:", value=roles, inline=True)
        embeded.add_field(name="Emoji Count:", value=emojis, inline=True)
        embeded.add_field(name="Channel Count:", value=channels, inline=True)

        embeded.add_field(name="Bot created by:", value="Chris Nguyen & Jonah Bui", inline=False)

        await ctx.send(embed=embeded) 


def setup(bot):
    bot.add_cog(administration(bot))
