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


