import discord
import data.secrets
import datetime
from discord.ui import View,Button

async def give_starboard_embed_view(message:discord.Message):
    em = discord.Embed(color=data.secrets.embed_colour,timestamp=datetime.datetime.now(),description=message.content)
    em.set_author(name=message.author.name+message.author.discriminator,icon_url=message.author.display_avatar)
    button = Button(label="Jump to Original Message", style=discord.ButtonStyle.link,url=message.jump_url)
    view = View()
    view.add_item(button)
    return em,view