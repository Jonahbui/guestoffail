import discord
from discord.ext import commands, tasks
import asyncio

class spyfall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_status = False

    @commands.command()
    async def spyfall(self, ctx):
        if self.game_status:
            return await ctx.send('A game is currently running, I cannot make another game instance')

        #sends message to see who wants to play, ref: github.com/JohnsonTran; TY :)
        self.game_status = True
        embed = discord.Embed(title='Spyfall', description='One of you is a spy, but who? Upvote to play, Question mark for game instructions', color=discord.Color.gold())
        embed.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url='https://www.spyfall.app/assets/spy_black-28052431b8cb9f75b4740f04710596de668a298483e2c5f0f25401416231c92f.png')
        msg = await ctx.send(embed=embed)
        await ctx.send('@here You have 15 seconds to join the game!')
        await msg.add_reaction("\U0001F44D")
        await msg.add_reaction("\U00002753")
        await asyncio.sleep(15)

        #Need to split up reactions, manage users who needed instructions and players who opted to just play the game
        #after handing pre-game logic, wait for all player confimrations before playing the game
        #Lines below aren't working correctly, Generic error occurs
        #------------------------------------------------------------------------------------------------------------

        #handles game logic pre-game
        #data = await ctx.channel.fetch_message(msg.id)
        #player_reaction = data.reactions[0]
        #players = await data.users().flatten()
        
        #ctx.send('Test reaction users: ')
        #for user in player_reaction:
        #    await ctx.send(user.mention)

def setup(bot):
    bot.add_cog(spyfall(bot))