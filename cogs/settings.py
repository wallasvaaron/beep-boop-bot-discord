import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import after_invoke
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.utils import get

from main import botsays

# help='Change the bot\'s settings'
class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Settings: ready')

    # commands
    @commands.group(name='settings', alisases=['options'], invoke_without_command=True, help='Accesses the settings of the bot: !settings <setting>')
    async def settings(self, ctx):
        await botsays(ctx, 'Change a setting with !settings <setting>.')


def setup(bot):
    bot.add_cog(Settings(bot))