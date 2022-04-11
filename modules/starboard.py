# IDEA:
# 1. Check for a reaction with ⭐ as its content. This reaction should not be on bot messages. 
# 2. Check the author of the reaction. if it is the message author then do not count it.
# 3. if the true reaction count > 10 then do the following:
# 4. if the message id exists in db, then update its star count, else insert it into db
# 5. then update the message in starboard channel with correct number of stars.
# In the stars.db (stars) store the following : 
# msgauthorid (the id of message author) , messageid (the message sent by author) , starboardmsgid (the message sent by bot in starboard) , number of stars on message
# In the stars.db (star_stats) sore the following : 
# msg_author_id (author of message) , no. of stars (tuple) , starrer_userid (tuple)
# both no. of stars and starrer_userid will have same indexing

"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import _helpers.starboard_functions as s_funcs

class Starboard(commands.Cog):
    """Starboard commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        emoji = payload.emoji
        starrer_user_id = payload.user_id
        message_id = payload.message_id

        if self.bot.is_ready() and channel_id in data.secrets.allowed_channel_ids:
            if emoji.name == "⭐":
                async with self.bot.star_db.cursor() as cursor:
                    await cursor.execute("SELECT * FROM stars WHERE channel_id = ? AND messageid = ?",(channel_id,message_id,))
                    fetched_data = await cursor.fetchone()
                    message = await self.bot.get_channel(channel_id).fetch_message(message_id)
                    emb,view = await s_funcs.give_starboard_embed_view(message)
                    starboard_chan = self.bot.get_channel(data.secrets.starboard_channel_id)
                    if not message.author.bot and starrer_user_id != message.author.id:
                        temp_lst = [(rxn.emoji,rxn.me) for rxn in message.reactions]
                        num_of_stars = message.reactions[temp_lst.index(("⭐",True))].count
                        if (emoji.name,True) in temp_lst:
                            if not fetched_data:
                                msgid = 0
                                await cursor.execute("INSERT INTO stars (channel_id,msgauthorid,messageid,starboardmsgid,numstars) VALUES (?,?,?,?,?)",(channel_id,message.author.id,message_id,msgid,num_of_stars,))
                            else:
                                await cursor.execute("SELECT starboardmsgid FROM stars WHERE channel_id = ? AND messageid = ?",(channel_id,message_id,))
                                ftch_data = await cursor.fetchone()
                                msg_fetched_id = ftch_data[0]
                                if num_of_stars >= data.secrets.minimum_stars_required and msg_fetched_id==0:
                                    msg = await starboard_chan.send(content=f"**🌟 {num_of_stars} {message.channel.mention}**",embed=emb,view=view)
                                    await cursor.execute(f"UPDATE stars SET starboardmsgid={msg.id},numstars={num_of_stars} WHERE channel_id={message.channel.id} AND messageid={message.id}")
                                else:
                                    if msg_fetched_id !=0:
                                        starbrd_msg = await starboard_chan.fetch_message(msg_fetched_id)
                                        await cursor.execute(f"UPDATE stars SET numstars={num_of_stars} WHERE channel_id={message.channel.id} AND messageid={message.id}")
                                        await starbrd_msg.edit(content=f"**🌟 {num_of_stars} {message.channel.mention}**",embed=emb,view=view)
                await self.bot.star_db.commit()





def setup(bot):
    bot.add_cog(Starboard(bot))
    print("Starboard cog is loaded")