import discord
import data.secrets
import datetime
from discord.ui import View,Button
import json
from collections import OrderedDict

async def give_starboard_embed_view(message:discord.Message):
    em = discord.Embed(color=data.secrets.embed_colour,timestamp=datetime.datetime.now(),description=message.content)
    em.set_author(name=message.author.name+message.author.discriminator,icon_url=message.author.display_avatar)
    button = Button(label="Jump to Original Message", style=discord.ButtonStyle.link,url=message.jump_url)
    view = View()
    view.add_item(button)
    return em,view

async def give_star_details_for_member(bot:discord.Bot,member:discord.Member):
    async with bot.star_db.cursor() as cursor:
        await cursor.execute("SELECT * FROM stats WHERE mem_id = ?",(member.id,))
        fetched_data = await cursor.fetchone()
        if not fetched_data: return "NO DATA"
        
        s_r = fetched_data[1]
        s_g = fetched_data[2]
        idols = json.loads(fetched_data[3])
        beta_orbiters = json.loads(fetched_data[4])

        await cursor.execute("SELECT channel_id,messageid,numstars FROM stars WHERE msgauthorid = ? ORDER BY numstars DESC LIMIT 3",(member.id,))
        fetched_data = await cursor.fetchall()
        top_msgs = []
        if len(fetched_data) == 0:
            s_m = 0
        else:
            s_m = len(fetched_data)
            for i in fetched_data:
                msg = await bot.get_channel(i[0]).fetch_message(i[1])
                top_msgs.append((msg.id,msg.jump_url,i[2]))


        details = {
            "starred messages" : s_m,
            "stars received" : s_r,
            "stars given" : s_g,
            "top messages" : top_msgs,
            "idols" : idols,
            "beta orbiters" : beta_orbiters
        }
        return details

def pretty_ms_sort(l):
    return l[2]

def give_top_pretty_msg(top_mess):
    top_mess.sort(key=pretty_ms_sort,reverse=True)
    final = ""
    if len(top_mess) >=3:
        top_mess = top_mess[:3]
        final += f"🥇 [{top_mess[0][0]}]({top_mess[0][1]}) ({top_mess[0][2]} stars.)\n"
        final += f"🥈 [{top_mess[1][0]}]({top_mess[1][1]}) ({top_mess[1][2]} stars.)\n"
        final += f"🥉 [{top_mess[2][0]}]({top_mess[2][1]}) ({top_mess[2][2]} stars.)"
    elif len(top_mess) ==2:
        top_mess = top_mess[:2]
        final += f"🥇 [{top_mess[0][0]}]({top_mess[0][1]}) ({top_mess[0][2]} stars.)\n"
        final += f"🥈 [{top_mess[1][0]}]({top_mess[1][1]}) ({top_mess[1][2]} stars.)"
    else:
        top_mess = top_mess[0]
        final += f"🥇 [{top_mess[0]}]({top_mess[1]}) ({top_mess[2]} stars.)"

    return final

def useful_mention(bot:discord.Bot,id):
    id = int(id)
    user:discord.Member = bot.get_user(id)
    if not user:
        return f"<@!{id}>"
    return user.mention

def give_idols_beta_pretty(bot:discord.Bot,dic):
    dic2=OrderedDict(sorted(dic.items(),key= lambda x:x[1],reverse=True))
    final = ""
    keys = list(dic2.keys())
    if len(keys) >=3:
        keys = keys[:3]
        final += f"🥇 {useful_mention(bot,keys[0])} ({dic2[keys[0]]} stars.)\n"
        final += f"🥈 {useful_mention(bot,keys[1])} ({dic2[keys[1]]} stars.)\n"
        final += f"🥉 {useful_mention(bot,keys[2])} ({dic2[keys[2]]} stars.)"
    elif len(keys) == 2 :
        keys = keys[:2]
        final += f"🥇 {useful_mention(bot,keys[0])} ({dic2[keys[0]]} stars.)\n"
        final += f"🥈 {useful_mention(bot,keys[1])} ({dic2[keys[1]]} stars.)"
    else:
        keys = keys[0]
        final += f"🥇 {useful_mention(bot,keys)} ({dic2[keys]} stars.)"

    return final

async def give_star_details_for_server(bot:discord.Bot):
    async with bot.star_db.cursor() as cursor:
        await cursor.execute("SELECT numstars FROM stars")
        fetched_data = await cursor.fetchall()
        if not fetched_data: return "NO DATA"
        total_messages = len(fetched_data)
        total_stars = 0
        for i in fetched_data:
            total_stars += i[0]
        
        await cursor.execute("SELECT mem_id,received FROM stats ORDER BY received DESC LIMIT 3")
        recvd = await cursor.fetchall()
        final__r = ""
        if len(recvd) >=3:
            recvd = recvd[:3]
            final__r += f"🥇 {useful_mention(bot,recvd[0][0])} ({recvd[0][1]} stars.)\n"
            final__r += f"🥈 {useful_mention(bot,recvd[1][0])} ({recvd[1][1]} stars.)\n"
            final__r += f"🥉 {useful_mention(bot,recvd[2][0])} ({recvd[2][1]} stars.)"
        elif len(recvd) ==2:
            recvd = recvd[:2]
            final__r += f"🥇 {useful_mention(bot,recvd[0][0])} ({recvd[0][1]} stars.)\n"
            final__r += f"🥈 {useful_mention(bot,recvd[1][0])} ({recvd[1][1]} stars.)"
        else:
            recvd = recvd[0]
            final__r += f"🥇 {useful_mention(bot,recvd[0])} ({recvd[1]} stars.)"

        await cursor.execute("SELECT mem_id,given FROM stats ORDER BY given DESC LIMIT 3")
        given = await cursor.fetchall()
        final__g = ""
        if len(given) >=3:
            given = given[:3]
            final__g += f"🥇 {useful_mention(bot,given[0][0])} ({given[0][1]} stars.)\n"
            final__g += f"🥈 {useful_mention(bot,given[1][0])} ({given[1][1]} stars.)\n"
            final__g += f"🥉 {useful_mention(bot,given[2][0])} ({given[2][1]} stars.)"
        elif len(given) ==2:
            given = given[:2]
            final__g += f"🥇 {useful_mention(bot,given[0][0])} ({given[0][1]} stars.)\n"
            final__g += f"🥈 {useful_mention(bot,given[1][0])} ({given[1][1]} stars.)"
        else:
            given = given[0]
            final__g += f"🥇 {useful_mention(bot,given[0])} ({given[1]} stars.)"

        await cursor.execute("SELECT channel_id,messageid,numstars FROM stars ORDER BY numstars DESC LIMIT 3")
        fetched_data = await cursor.fetchall()
        top_msgs = []
        for i in fetched_data:
            msg = await bot.get_channel(i[0]).fetch_message(i[1])
            top_msgs.append((msg.id,msg.jump_url,i[2]))

        details = {
            "total stars" : total_stars,
            "total messages" : total_messages,
            "received" : final__r,
            "given" : final__g,
            "top msg" : top_msgs
        }
        return details
