import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.utils import get

import options.cog_options as cog_options
from main import botsays

# help='Change server admin settings'
class ServerAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    role_ids = []

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('ServerAdmin: ready')

    
    # command groups
    @commands.group(name='admin', aliases=['serveradmin', 'administrator'], invoke_without_command=True, help='Admin commands for the server: "!admin <command>" Has to have the "Administrator" role to use these commands.')
    async def admin(self, ctx):
        await botsays(ctx, 'Base for server admin commands: "!admin <command>"')

    
    @admin.group(name='settings', alisases=['options'], invoke_without_command=True, help='Accesses the settings of the bot: !settings <setting>')
    @commands.has_any_role()
    async def settings(self, ctx):
        await botsays(ctx, 'Changes server settings: !admin settings <setting>.')

    # commands
    @settings.command(name='list')
    async def list(self, ctx):
        await botsays(ctx, cog_options.options)

    @settings.command(name='answering', help='Determines on a range from 0-3 how often the bot answers, 3 being most frequent, 0 not at all: "!settings answering <number from 1 to 5>"  Does not disable asnwers to admin commands.')
    async def answering(self, ctx, value):
        try:
            if int(value)<=3 and int(value)>=0:
                cog_options.options.update({'answering':value})
                await botsays(ctx, f'options-answering: value updated to {value}')
                return
        except:
            await botsays(ctx, f'{value} is not a valid value for the answering-setting. Input an integer between 0 and 3.')
        else:
            await botsays(ctx, f'{value} is not a valid value for the answering-setting. Input an integer between 0 and 3.')
    
    @settings.command(name='listening', help='Determines whether or not the bot listens for commands. Does not disable listening for admin commands.')
    async def listening(self, ctx):
        print('listening')


def setup(bot):
    bot.add_cog(ServerAdmin(bot))