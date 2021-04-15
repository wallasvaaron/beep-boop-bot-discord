import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded

from main import list_of_cogs, botsays

list_of_restrictions = []

async def restrictions(ctx):
    print(list_of_restrictions)
    output = '**Role-restricted commands**\n*Command*           *Role(s) with access:*'
    roles = ''
    for i in list_of_restrictions:
        for k in i[1]:
            roles += f'    {ctx.guild.get_role(role_id=k)}\n'
        output += f'\n{i[0]}            {roles}'
    await botsays(ctx, output)

async def is_a_real_cog(ctx,cog): # PASS CTX AS ARGUMENT
    if cog in list_of_cogs:
            return True
    else:
        await botsays(ctx, f'{str.title(cog)} cog doesn\'t exist.\nAvailable cogs: {list_of_cogs}')
        return

# help='Change bot admin settings'
class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    # only people with one these roles can access botadmin commands
    role_ids = [830806207928205312]
    
    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('BotAdmin: ready')

    # command groups
    @commands.group(name='botadmin', invoke_without_command=True, help='Admin commands for the bot: "!botadmin <command>" Has to have the "BotAdmin" role to use these commands.')
    async def botadmin(self, ctx):
        await botsays(ctx, 'Base for bot admin commands: !botadmin <command>')

    @botadmin.group(name='cog', invoke_without_command=True)
    @commands.has_any_role(830806207928205312)
    async def cog(self, ctx):
        await botsays(ctx, 'Base for bot\'s cog (category) commands: !botadmin cog <command>')
    

    # commands
    @cog.command(name='load', help='Loads the given cog: !cog load <cogname>')
    async def load(self, ctx, cog):
        if await is_a_real_cog(ctx, cog):
            try:
                self.bot.load_extension(f'cogs.{self.cog}')
                await botsays(ctx, f'{str.title(self.cog)} cog loaded.')
            except ExtensionAlreadyLoaded:
                await botsays(ctx, f'{str.title(self.cog)} cog already loaded.')
            except:
                await botsays(ctx, f'Couldn\'t load the {str.title(self.cog)} cog.')
        else:
            return

    @cog.command(name='unload', help='Unloads the given cog: !cog unload <cogname>')
    async def unload(self, ctx, cog):
        if await is_a_real_cog(ctx,cog):
            try:
                self.bot.unload_extension(f'cogs.{self.cog}')
                await botsays(ctx, f'{str.title(self.cog)} cog unloaded.')
            except ExtensionNotLoaded:
                await botsays(ctx, f'{str.title(self.cog)} cog already unloaded.')
            except:
                await botsays(ctx, f'Couldn\'t unload the {str.title(self.cog)} cog.')
        else:
            return

    @cog.command(name='reload', help='Reloads the given cog: !cog reload <cogname>')
    async def reload(self, ctx, cog):
        if await is_a_real_cog(ctx, cog):
            try:
                self.bot.unload_extension(f'cogs.{self.cog}')
                self.bot.load_extension(f'cogs.{self.cog}')
                await botsays(ctx, f'{str.title(self.cog)} cog reloaded.')
            except ExtensionNotLoaded:
                try:
                    self.bot.load_extension(f'cogs.{self.cog}')
                    await botsays(ctx, f'{str.title(self.cog)} cog reloaded.')
                except ExtensionAlreadyLoaded:
                    await botsays(ctx, f'Couldn\'t reload the {str.title(self.cog)} cog.')
            except:
                await botsays(ctx, f'Couldn\'t reload the {str.title(self.cog)} cog')
        else:
            return


def setup(bot):
    bot.add_cog(BotAdmin(bot))

