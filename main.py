from discord.ext import commands
import discord
import data.secrets
import time
import aiosqlite
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=data.secrets.bot_prefix, help_command=None, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    setattr(bot,"link_db",await aiosqlite.connect(r"data\databases\links.db"))
    async with bot.link_db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS links (channel_id INTEGER, message_id INTEGER, user_id INTEGER, gdrive_id TEXT, object_size INTEGER)")
    await bot.change_presence(activity=discord.Game(name="Megadrive"))
    print("Bot is ready!")

_start_time = time.time()


if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # i.e. its not being imported from another python file run this
    for module in data.secrets.module_list:
        bot.load_extension(f"modules.{module}")
    
    for file in os.listdir(r"modules\required"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"modules.required.{file[:-3]}")

    bot.run(data.secrets.bot_token)
