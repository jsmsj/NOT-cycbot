import discord

import data.secrets

async def error_embed(ctx, title, msg):
    embed = discord.Embed(
        title=title,
        description=msg,
        colour=discord.Color.red(),
    )
    embed.set_thumbnail(url=data.secrets.error_image_url)
    try:
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        print(f"Could not send error!\nError: {e}")


async def send_error(error,bot):
    err_channel = bot.get_channel(data.secrets.error_channel)
    error_string = f"An Error occured in bot,\n Error is: \n ```\n{error}\n```\n If you can resolve this on your own well and good, else contact jsmsj#5252 or open an issue at GitHub - https://github.com/jsmsj/NOT-cycbot "
    await err_channel.send(error_string)
