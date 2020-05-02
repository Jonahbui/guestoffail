import discord
from discord.ext import commands, tasks

class game_template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def game_template(self, ctx):
        server = ctx.message.guild

        embed = discord.Embed(title='INSERT GAME TITLE HERE', description='INSERT GAME DESCRIPTION HERE', color=discord.Color.gold())
        embed.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=server.icon_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("\U0001F44D")

        

def setup(bot):
    bot.add_cog(game_template(bot))