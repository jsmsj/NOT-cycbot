from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("bot_token")
bot_prefix = os.getenv("bot_prefix")

module_list = os.getenv("modules").replace(" ","").split(",")

error_image_url = os.getenv("error_image_url")

moderator_role_id = int(os.getenv("moderator_role_id"))

