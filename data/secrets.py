from dotenv import load_dotenv
import os
import discord
import _helpers.gdrive_functions as gd_funcs

load_dotenv()

bot_token = os.getenv("bot_token")
bot_prefix = os.getenv("bot_prefix")

module_list = os.getenv("modules").replace(" ","").split(",")

error_image_url = os.getenv("error_image_url")

moderator_role_id = int(os.getenv("moderator_role_id"))

r,g,b = os.getenv("embed_colour").replace(" ","").split(",")

embed_colour = discord.Color.from_rgb(int(r),int(g),int(b))

bot_owner_id = int(os.getenv("bot_owner_id"))

valid_posting_channel_ids_temp = os.getenv("where_to_post_channel_ids").replace(" ","").split(",")

allowed_channel_ids = [int(x) for x in valid_posting_channel_ids_temp]

error_channel = int(os.getenv("send_error_channel_id"))

default_clone_dest_id = gd_funcs.getIdFromUrl(os.getenv("default_clone_destination_id"))

bot_version = "1.0.0" #DONOT CHANGE THESE

bot_language = "English"  #DONOT CHANGE THESE

server_invite_link = os.getenv("server_invite_link") + r"                             "