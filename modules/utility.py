"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import datetime
import time
from main import _start_time

class Utility(commands.Cog):
    """Utility commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.command()
    async def avatar(self,ctx,member:discord.Member=None):
        """Gives you avatar of yourself or any member's"""
        member = member or ctx.author
        memberAvatar = member.display_avatar
        avaEmbed = discord.Embed(title=f"Display Avatar",color=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        avaEmbed.set_image(url=memberAvatar)
        await ctx.reply(embed = avaEmbed)

    @commands.command()
    async def ping(self,ctx):
        em = discord.Embed(description=f"Display Not-cycbot's latency. If you're experiencing a slow response time, contact <@!{data.secrets.bot_owner_id}>",color=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        em.add_field(name="Latency",value=f"```\n🏓 Pong!\nWS / WEBSOCKET: {round(self.bot.latency * 1000 , 1)}ms • REST: ...\n```")
        em.set_footer(text=f"Author: {ctx.author.name} • ID: {ctx.author.id} ")
        before = time.monotonic()
        message = await ctx.send(embed=em)
        difference = (time.monotonic() - before) * 1000
        em.clear_fields()
        em.remove_footer()
        em.add_field(name="Latency",value=f"```\n🏓 Pong!\nWS / WEBSOCKET: {round(self.bot.latency * 1000 , 1)}ms • REST: {round(difference,1)}ms\n```")
        em.set_footer(text=f"{ctx.author.name} • ID: {ctx.author.id} ")
        await message.edit(embed=em)

    @commands.command()
    async def uptime(self,ctx):
        current_time = time.time()
        difference = int(round(current_time - _start_time))
        text = str(datetime.timedelta(seconds=difference))
        em = discord.Embed(description="Displays Not-cycbot's uptime.",color=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        em.add_field(name="Uptime",value=f"```py\n{text}\n```")
        em.set_footer(text=f"{ctx.author.name} • ID: {ctx.author.id} ")
        await ctx.send(embed=em)

    @commands.command()
    async def whois(self,ctx,member:discord.Member=None):
        member = member or ctx.author
        created_datetime = member.created_at
        created_time = created_datetime.strftime("%a, %d %B %Y")
        joined_datetime = member.joined_at
        joined_time = joined_datetime.strftime("%a, %d %B %Y")
        em = discord.Embed(color=data.secrets.embed_colour,timestamp=datetime.datetime.now())
        em.set_author(name=member.name,icon_url=member.display_avatar)
        em.set_footer(text=f"ID: {member.id} ")
        em.set_thumbnail(url=member.display_avatar)
        em.add_field(name="Register Date",value=created_time,inline=True)
        em.add_field(name="Member Since",value=joined_time,inline=True)
        memrole = member.roles
        memrole.pop(0)
        em.add_field(name=f"Roles [{len(memrole)}]",value=' '.join([x.mention for x in memrole]),inline=False)
        em.add_field(name="Contributor Stats",value="TODO")
        await ctx.send(embed=em)

        
    

        
def setup(bot):
    bot.add_cog(Utility(bot))
    print("Utility cog is loaded")