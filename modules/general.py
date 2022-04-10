"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import datetime
import _helpers.general_functions as funcs

class General(commands.Cog):
    """General commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.command()
    async def about(self,ctx):
        em = discord.Embed(description=f"NOT-cycbot is a mirror of Cycbot which is a custom bot developed exclusively for The Megadrive project. To learn more about Not-cycbot usage, use `{data.secrets.bot_prefix}help.`\nIf you come across a bug or have suggestions for improvement, contact <@!{data.secrets.bot_owner_id}>",color=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        em.set_thumbnail(url="https://i.imgur.com/hb1kjTN.png")
        em.add_field(name="Version",value="`"+data.secrets.bot_version+"`")
        em.add_field(name="Language",value="`"+data.secrets.bot_language+"`")
        em.add_field(name="Prefix",value=f"`{data.secrets.bot_prefix}`")
        em.add_field(name="Default Status",value="Playing `Megadrive`")
        em.add_field(name="Repository Url",value="[Github](https://github.com/jsmsj/NOT-cycbot)")
        em.add_field(name="Bot Library",value="Python : [Py-cord](https://pycord.dev/)")
        em.set_footer(text="Development by jsmsj.")
        await ctx.send(embed=em)

    @commands.command()
    async def invite(self,ctx):
        em = discord.Embed(description="Displays the current invite link for The Megadrive.",colour=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        em.add_field(name="Invite URL",value=f"```\n{data.secrets.server_invite_link}\n```")
        em.set_footer(text=f"{ctx.author.name} • {ctx.author.id} ")
        await ctx.send(embed=em)

    @commands.command()
    async def state(self,ctx):
        em=discord.Embed(
            description="Displays the current state of Cycbot.",
            color=data.secrets.embed_colour,
            timestamp=datetime.datetime.now()
        )
        em.add_field(
            name="Current State",
            value=funcs.give_state_desc()
        )
        em.set_footer(text=f"{ctx.author.name} • {ctx.author.id} ")
        await ctx.send(embed=em)



def setup(bot):
    bot.add_cog(General(bot))
    print("General cog is loaded")