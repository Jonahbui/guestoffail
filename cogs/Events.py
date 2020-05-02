from discord.ext import commands
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Prefix: ='))
        print(f'{self.bot.user.name} has connected to Discord.')

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send(f'{member} has joined on the Great Journey...')

    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        await ctx.send(f'{member} has abandoned the Great Journey...')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found, please check =help for list of commands')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing arguments, please try again')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Sorry, you don\'t have rights to use the role')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Please wait until the cooldown has ended (Typically 5 seconds)')

def setup(bot):
    bot.add_cog(Events(bot))