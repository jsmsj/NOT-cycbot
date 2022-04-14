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
from datetime import datetime
import discord
from discord.ext import commands
import data.secrets
import _helpers.starboard_functions as s_funcs
import json

from discord.ui import Button,View

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
                            ### for stars db
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
                            ### for stats db
                            await cursor.execute("SELECT * FROM stats WHERE mem_id= ?",(starrer_user_id,))
                            fetched_data = await cursor.fetchone()
                            if not fetched_data:
                                await cursor.execute("INSERT INTO stats (mem_id,received,given,idols,beta) VALUES (?,?,?,?,?)",(starrer_user_id,0,0,json.dumps({}),json.dumps({}),))

                            await cursor.execute("SELECT * FROM stats WHERE mem_id= ?",(message.author.id,))
                            fetched_data = await cursor.fetchone()
                            if not fetched_data:
                                await cursor.execute("INSERT INTO stats (mem_id,received,given,idols,beta) VALUES (?,?,?,?,?)",(message.author.id,0,0,json.dumps({}),json.dumps({}),))
                            
                            #
                            await cursor.execute("SELECT given,idols FROM stats WHERE mem_id= ?",(starrer_user_id,))
                            fetched_data = await cursor.fetchone()
                            given = fetched_data[0] + 1
                            idol_dict = json.loads(fetched_data[1])
                            if str(message.author.id) not in idol_dict:
                                idol_dict[str(message.author.id)] = 0
                            new = idol_dict[str(message.author.id)] + 1
                            idol_dict[str(message.author.id)] = new
                            dumped = json.dumps(idol_dict)
                            # await cursor.execute(f"UPDATE stats SET given={given}, idols={dumped} WHERE mem_id={starrer_user_id}")
                            await cursor.execute(f"UPDATE stats SET given=? , idols=? WHERE mem_id=?",(given,dumped,starrer_user_id,))
                            #

                            await cursor.execute("SELECT received,beta FROM stats WHERE mem_id= ?",(message.author.id,))
                            fetched_data = await cursor.fetchone()
                            received = fetched_data[0] + 1
                            beta_dict = json.loads(fetched_data[1])
                            if str(starrer_user_id) not in beta_dict:
                                beta_dict[str(starrer_user_id)] = 0
                            new = beta_dict[str(starrer_user_id)] + 1
                            beta_dict[str(starrer_user_id)] = new
                            dumped = json.dumps(beta_dict)

                            await cursor.execute(f"UPDATE stats SET received=? , beta=? WHERE mem_id=?",(received,dumped,message.author.id,))

                            
                        
                await self.bot.star_db.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel_id = payload.channel_id
        emoji = payload.emoji
        starrer_user_id = payload.user_id
        message_id = payload.message_id
        if self.bot.is_ready() and channel_id in data.secrets.allowed_channel_ids:
            if emoji.name == "⭐":
                async with self.bot.star_db.cursor() as cursor:
                    message = await self.bot.get_channel(channel_id).fetch_message(message_id)

                    if not message.author.bot and starrer_user_id != message.author.id:
                        temp_lst = [(rxn.emoji,rxn.me) for rxn in message.reactions]
                        num_of_stars = message.reactions[temp_lst.index(("⭐",True))].count
                        if (emoji.name,True) in temp_lst:
                            ### for stats db

                            await cursor.execute("SELECT * FROM stats WHERE mem_id= ?",(starrer_user_id,))
                            fetched_data = await cursor.fetchone()
                            if not fetched_data:
                                await cursor.execute("INSERT INTO stats (mem_id,received,given,idols,beta) VALUES (?,?,?,?,?)",(starrer_user_id,0,0,json.dumps({}),json.dumps({}),))

                            await cursor.execute("SELECT * FROM stats WHERE mem_id= ?",(message.author.id,))
                            fetched_data = await cursor.fetchone()
                            if not fetched_data:
                                await cursor.execute("INSERT INTO stats (mem_id,received,given,idols,beta) VALUES (?,?,?,?,?)",(message.author.id,0,0,json.dumps({}),json.dumps({}),))

                            await cursor.execute("SELECT given,idols FROM stats WHERE mem_id= ?",(starrer_user_id,))
                            fetched_data = await cursor.fetchone()
                            given = fetched_data[0] - 1
                            idol_dict = json.loads(fetched_data[1])
                            if str(message.author.id) not in idol_dict:
                                idol_dict[str(message.author.id)] = 0
                            new = idol_dict[str(message.author.id)] - 1
                            idol_dict[str(message.author.id)] = new
                            dumped = json.dumps(idol_dict)
                            # await cursor.execute(f"UPDATE stats SET given={given}, idols={dumped} WHERE mem_id={starrer_user_id}")
                            await cursor.execute(f"UPDATE stats SET given=? , idols=? WHERE mem_id=?",(given,dumped,starrer_user_id,))
                            #

                            await cursor.execute("SELECT received,beta FROM stats WHERE mem_id= ?",(message.author.id,))
                            fetched_data = await cursor.fetchone()
                            received = fetched_data[0] - 1
                            beta_dict = json.loads(fetched_data[1])
                            if str(starrer_user_id) not in beta_dict:
                                beta_dict[str(starrer_user_id)] = 0
                            new = beta_dict[str(starrer_user_id)] - 1
                            beta_dict[str(starrer_user_id)] = new
                            dumped = json.dumps(beta_dict)

                            await cursor.execute(f"UPDATE stats SET received=? , beta=? WHERE mem_id=?",(received,dumped,message.author.id,))

                await self.bot.star_db.commit()
            


    
    @commands.command()
    async def stars(self,ctx,member:discord.Member=None):
        if member:
            details = await s_funcs.give_star_details_for_member(self.bot,member)
            if details == "NO DATA":
                em = discord.Embed(title="Error",color=data.secrets.embed_colour,timestamp=datetime.now(),description=f"No entry found in `Starboard` for {member.mention}.\n\nPlease check the username/user ID, or try reacting with some stars in the content channels and try again.")
                return await ctx.send(embed=em)
            
            starred_msgs = details["starred messages"]
            stars_recvd = details["stars received"]
            stars_given = details["stars given"]
            top_mess = details["top messages"]
            idols = details["idols"]
            beta = details["beta orbiters"]


            em = discord.Embed(color=data.secrets.embed_colour,timestamp=datetime.now())
            em.add_field(name="Starred Messages",value=starred_msgs)
            em.add_field(name="Stars Received",value=stars_recvd)
            em.add_field(name="Stars Given",value=stars_given)
            if len(top_mess) >0:
                em.add_field(
                    name="Top Messages",
                    value=s_funcs.give_top_pretty_msg(top_mess),
                    inline=False
                )
            if len(idols) > 0 :
                pretty_idols = s_funcs.give_idols_beta_pretty(self.bot,idols)
                em.add_field(
                    name="Idols",
                    value=pretty_idols
                )
            if len(beta) > 0:
                em.add_field(
                    name="Beta Orbiters",
                    value=s_funcs.give_idols_beta_pretty(self.bot,beta)
                )
            
            em.set_author(name=member.name,icon_url=member.display_avatar)
            em.set_footer(text="Powered by NOT-cycbot • Tracking ⭐'s Since April 14th, 2022")

            await ctx.send(embed=em)
        else:
            
            details = await s_funcs.give_star_details_for_server(self.bot)
            if details == "NO DATA":
                em = discord.Embed(title="Error",color=data.secrets.embed_colour,timestamp=datetime.now(),description=f"There arent any starred messages in this server.\n\nTry reacting with some stars in the content channels and try again.")
                return await ctx.send(embed=em)

            total_stars = details["total stars"]
            total_msg = details["total messages"]
            top_receivers = details["received"]
            top_givers = details["given"]
            top_msgs = details["top msg"]
            
            em = discord.Embed(title=f"{ctx.guild.name}'s Starboard Statistics",color=data.secrets.embed_colour,description=f"{total_stars} total stars in {total_msg} total messages.")
            if len(top_receivers) >0:
                em.add_field(name="Top Star Receivers",value=top_receivers,inline=False)
            if len(top_givers)>0:
                em.add_field(name="Top Star Givers",value=top_givers,inline=False)
            if len(top_msgs) >0:
                em.add_field(
                    name="Top Messages",
                    value=s_funcs.give_top_pretty_msg(top_msgs),
                    inline=False
                )
            em.set_footer(text="Powered by NOT-cycbot • Tracking ⭐'s Since April 14th, 2022")
            # starboard_chan= self.bot.get_channel(data.secrets.starboard_channel_id)
            # button = Button(label="⭐ Jump to StarBoard", style=discord.ButtonStyle.link,url=starboard_chan.jump_url)
            # view = View()
            # view.add_item(button)

            await ctx.send(embed=em) # ,view=view

            




def setup(bot):
    bot.add_cog(Starboard(bot))
    print("Starboard cog is loaded")