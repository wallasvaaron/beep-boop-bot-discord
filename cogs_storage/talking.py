import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import after_invoke
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.utils import get

async def botsays(ctx, input):

    await ctx.send(input) #, delete_after=20)


class Talking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def displayembed(self,ctx):
        embed = discord.Embed(
            title='Title',
            description = 'This is a description.',
            colour = discord.Colour.blue()
        )

        embed.set_footer(text='This is a footer.')
        embed.set_image(url='https://www.bwallpaperhd.com/wp-content/uploads/2020/08/GamescomCologne-1600x900.jpg')
        embed.set_thumbnail(url='https://www.bwallpaperhd.com/wp-content/uploads/2020/08/GamescomCologne-1600x900.jpg')
        embed.set_author(name='Author Name', icon_url='https://th.bing.com/th/id/OIP.01F8VXJ3WhhLSTETX_Za2QHaEK?pid=ImgDet&rs=1')
        embed.add_field(name='Field Name', value='field value', inline=False)
        embed.add_field(name='Field Name', value='field value', inline=True)
        embed.add_field(name='Field Name', value='field value', inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Talking(bot))