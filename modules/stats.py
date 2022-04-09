"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import aiosqlite
import _helpers.general_functions as funcs


class Stats(commands.Cog):
    """Stats commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.command()
    async def stats(self,ctx,member:discord.Member=None):
        member = member or ctx.author
        joined_datetime = member.joined_at
        joined_time = joined_datetime.strftime("%a, %d %B %Y. %I:%M %p %Z.")
        desc = await funcs.generate_stats(member.id,self.bot)
        em = discord.Embed(description=f"Contribution statistics for {member.mention}.\n**Member Since:** {joined_time}\n```py\n{desc}\n```",color = data.secrets.embed_colour)
        em.set_author(name=member.name,icon_url=member.display_avatar)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Stats(bot))
    print("Stats cog is loaded")