import discord
from discord import colour
from discord.ext import commands
from discord.utils import get
import os


COMMAND_PREFIX = '?'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
# guild = bot.get_guild(441310016100892682)

@bot.event
async def on_ready():
    # change_status.start()
    print(f'\nLogged in as: {bot.user.name}\n')

list_of_cogs = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{str.lower(filename[:-3])}')
        list_of_cogs.append(str.lower(filename[:-3]))

bot.run(os.environ['TOKEN'])