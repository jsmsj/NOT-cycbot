from dotenv import load_dotenv
import os
import discord

load_dotenv()

bot_token = os.getenv("bot_token")
bot_prefix = os.getenv("bot_prefix")

module_list = os.getenv("modules").replace(" ","").split(",")

error_image_url = os.getenv("error_image_url")

moderator_role_id = int(os.getenv("moderator_role_id"))

r,g,b = os.getenv("embed_colour").replace(" ","").split(",")

embed_colour = discord.Color.from_rgb(int(r),int(g),int(b))

bot_owner_id = int(os.getenv("bot_owner_id"))

