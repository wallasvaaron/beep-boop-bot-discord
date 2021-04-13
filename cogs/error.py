from cogs.botadmin import botsays
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import after_invoke
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.utils import get
import sys

from cogs.talking import botsays


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Error: ready')

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if hasattr(ctx.command, 'on_error'):
    #         return
    #     error = getattr(error, 'original', error)
    #     print(f'\nERROR: {error}')
        
    #     if isinstance(error, commands.CheckFailure):
    #         await botsays(ctx, "You do not have permission to use this command. Type !permissions to see a list of command restrictions.")
    #         return

    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await botsays(ctx, "The command was inputted incorrectly. Type !help <command> to get information on how to use a command.")
    #         return

    #     if isinstance(error, commands.CommandNotFound):
    #         await botsays(ctx, "Command not recognized. Type !help for a list of commands.")
    #         return
        
        

        # ignore all other exception types, but print them to stderr
        # print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

        # last_traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



def setup(bot):
    bot.add_cog(Error(bot))