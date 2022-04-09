"""Imports"""
import discord
from discord.ext import commands
import data.secrets

class Moderation(commands.Cog):
    """Moderation commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.command()
    @commands.has_role(data.secrets.moderator_role_id)
    async def purge(self, ctx, amount=10):
        """Deletes n number of messages from any channel. There are no limits or date restrictions for this function - use with caution. Default 10."""
        await ctx.message.add_reaction('✅')
        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleared Messages')
        await ctx.channel.purge(limit=1)

def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Moderation cog is loaded")