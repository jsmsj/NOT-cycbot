"""Imports"""
import discord
from discord.ext import commands
import data.secrets
import time
import _helpers.gdrive_functions as gd_funcs
from discord.ui import Button, View

class DriveUtils(commands.Cog):
    """DriveUtils commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        Triggers typing indicator on Discord before every command.
        """
        await ctx.trigger_typing()    
        return

    @commands.command()
    async def clone(self,ctx,source=None):
        destination = data.secrets.default_clone_dest_id
        if not source:
            return await ctx.send(f"Please tell the source link or id.\nFor correct usage run `{data.secrets.bot_prefix}help clone`")
        start_time = time.time()
        source = gd_funcs.make_url(source)
        if source == "Source id not found" :return await ctx.send(f"Id not found in given link")
        name = await gd_funcs.send_name(ctx,source)
        d1 ='"'+"{"+ destination+"}"+"/"+ name + '"'
        sourc = gd_funcs.get_id(source)
        if "Source id not found in" in sourc:
            return await ctx.send(f"Id not found in {source}")
        s1 = "{" + sourc + "}"
        cool = await ctx.reply(
            "***Cloning in progress :)***"
        )
        cmd = ["gclone", "copy", f"GC:{s1}", f"GC:{d1}", "--transfers", "50", "-vP", "--stats-one-line", "--stats=15s", "--ignore-existing", "--drive-server-side-across-configs", "--drive-chunk-size", "128M", "--drive-acknowledge-abuse", "--drive-keep-revision-forever"]
        string = await gd_funcs.execute(cmd)
        final = string[-1989::]
        fin = final.splitlines()[-1].split(",")
        
        logs =f"```ml\n{final}\n```"
        logs_2 =f"```ml\n Copied: {fin[0]}\n Completed: {fin[1]}\n{fin[-1]}\n Speed: {fin[2]}\n```"

        out = "<https://drive.google.com/drive/folders/{}>".format(destination)

        em = discord.Embed(title="**Cloning Complete**",description=logs_2,color=data.secrets.embed_colour)
        em.add_field(name="Link", value=out)
        em.add_field(name="Folder Name",value="`"+name+"`")
        end_time = time.time()
        taken_time = round((end_time-start_time)*1000)
        em.set_footer(text=f"Time taken: {taken_time}ms = {taken_time/1000}s")

        butt1 = Button(
        label="Show Details",
        style=discord.ButtonStyle.green,
        emoji="⭐"
        )

        view = View()
        view.add_item(butt1)

        async def butt1call(interaction:discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("This button is not for you",ephemeral=True)
            else:
                butt1.disabled=True
                butt1.style = discord.ButtonStyle.success
                await interaction.response.edit_message(content=f"{ctx.author.mention}",embed=em,view=view)
                await interaction.followup.send(logs,ephemeral=True) 
        butt1.callback = butt1call

        
        await cool.edit(embed=em,view=view)
        await cool.reply(content=f"{ctx.author.mention}")

    @commands.command()
    async def size(self,ctx,source=None):
        if not source:
            return await ctx.send(f"Source not given.\nFor correct usage run `{data.secrets.bot_prefix}help size`")
        start_time = time.time()
        soure = gd_funcs.make_url(source)
        sour = gd_funcs.get_id(soure)
        if "Source id not found in" in sour:
            return await ctx.send(f"Id not found in {source}")
        s1 = "{" + sour + "}"
        msg = await ctx.reply("***Caclulating size ...***")
        cmd = ["gclone", "size",f"GC:{s1}","--fast-list"]
        out = await gd_funcs.execute(cmd)

        testing = out.splitlines()
        if testing[-1] == "Total size: 0 Bytes (0 Bytes)" and testing[0] == "Total objects: 0":
            out = gd_funcs.get_readable_file_size(gd_funcs.file_or_folder_size(sour))
        em = discord.Embed(title="**Size Calculated**",description=f"```py\n{out}\n```",color=discord.Color.green())
        end_time = time.time()
        taken_time = round((end_time-start_time)*1000)
        em.set_footer(text=f"Time taken: {taken_time}ms = {taken_time/1000}s")
        await msg.edit(embed=em)
        await msg.reply(content=ctx.author.mention)





def setup(bot):
    bot.add_cog(DriveUtils(bot))
    print("DriveUtils cog is loaded")