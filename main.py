from discord.ext import commands
import discord
import data.secrets
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=data.secrets.bot_prefix, help_command=None, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print("Bot is ready!")


if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # i.e. its not being imported from another python file run this
    for module in data.secrets.module_list:
        bot.load_extension(f"modules.{module}")

    bot.run(data.secrets.bot_token)
