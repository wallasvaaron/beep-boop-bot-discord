import discord
from discord import colour
from discord.ext import commands
from discord.utils import get
import os
import asyncio

# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(initialize())
# loop.run_until_complete(future)
print('check 1')

async def botsays(ctx, input):
    await ctx.send(input) #, delete_after=20)

COMMAND_PREFIX = '?'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
# guild = bot.get_guild(441310016100892682)

print('check 2')

@bot.event
async def on_ready():
    # change_status.start()
    print(f'\nLogged in as: {bot.user.name}\n')

print('check 3')

list_of_cogs = []
def initialize(): 
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{str.lower(filename[:-3])}')
            list_of_cogs.append(str.lower(filename[:-3]))

print('check 4')

bot.run(os.environ['TOKEN'])