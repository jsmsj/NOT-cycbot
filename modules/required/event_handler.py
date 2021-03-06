"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import _helpers.gdrive_functions as gd_funcs
import _helpers.general_functions as funcs
from _helpers.errors import send_error
import re

class EventHandler(commands.Cog):
    """EventHandler commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == self.bot.user.id: return
        if message.author.bot: return
        if self.bot.is_ready() and message.channel.id in data.secrets.allowed_channel_ids:
            list_of_urls = funcs.find_all_urls_in_str(message.content)
            if len(list_of_urls) !=0:
                for i in list_of_urls:
                    if "drive.google.com" in i:
                        try:
                            gdrive_id = gd_funcs.getIdFromUrl(i)
                            async with self.bot.link_db.cursor() as cursor:
                                await cursor.execute("SELECT * FROM links WHERE channel_id = ? AND gdrive_id = ?",(message.channel.id,gdrive_id,))
                                fetched_data = await cursor.fetchone()
                                if fetched_data:
                                    await message.reply(f"The Google drive link <http://drive.google.com/open?id={gdrive_id}> has already been posted here before !! Please do not repost the same links.")
                                else:
                                    size = await gd_funcs.gc_size(gdrive_id)
                                    size = int(size)
                                    await cursor.execute("INSERT INTO links (channel_id,message_id,user_id,gdrive_id,object_size) VALUES (?,?,?,?,?)",(message.channel.id,message.id,message.author.id,gdrive_id,size))
                                    await message.add_reaction("???")
                            await self.bot.link_db.commit()
                        except KeyError:
                            pass
                        except Exception as e:
                            await send_error(e,self.bot)
                        
                        





def setup(bot):
    bot.add_cog(EventHandler(bot))
    print("EventHandler cog is loaded")