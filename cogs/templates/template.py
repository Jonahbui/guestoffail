import discord
from discord.ext import commands, tasks

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inside_template(self, ctx):
        await ctx.send("inside_template")

def setup(bot):
    bot.add_cog(template(bot))