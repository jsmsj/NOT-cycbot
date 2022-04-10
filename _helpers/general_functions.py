from urlextract import URLExtract
import aiosqlite
import data.secrets

extractor = URLExtract()
extractor.update_when_older(7)

def find_all_urls_in_str(message):
    return extractor.find_urls(message)

def get_readable_file_size(size_in_bytes) -> str:
    SIZE_UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    if size_in_bytes is None:
        return '0 B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 3)} {SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

async def give_contribution_stats(id,bot,byte=False):
    async with bot.link_db.cursor() as cursor:
        await cursor.execute("SELECT object_size FROM links WHERE user_id = ?",(id,))
        fetched_data = await cursor.fetchall()
        total_posts = len(fetched_data)
        total_bytes = 0
        for i in fetched_data:
            total_bytes += i[0]

        readable_size = get_readable_file_size(total_bytes)
    
    if readable_size == 'File too large': return "You are literally a GOD, cause you have posted so much stuff."
    if byte: return f"{readable_size} ({total_bytes} Bytes)"
    return f"{readable_size} in {total_posts} Posts."


def sum_of_links_for_key(d,key):
    val_dict = d[key]
    i = 0
    for v in val_dict.values():
        i+=v
    return i

def num_all_links(d):
    i = 0
    for key in d.keys():
        i+= sum_of_links_for_key(d,key)
    return i


async def generate_stats(id,bot):
    category_number = dict()
    async with bot.link_db.cursor() as cursor:
        for i in data.secrets.allowed_channel_ids:
            await cursor.execute("SELECT message_id FROM links WHERE channel_id = ? AND user_id = ? ",(i,id,))
            fetched_data = await cursor.fetchall()
            channel = bot.get_channel(i)
            try:
                if channel.category.name not in category_number:
                    category_number[channel.category.name] = {}
            except AttributeError:
                category_number["No Category"] = {}
            try:
                if f"#{channel.name}" not in category_number[channel.category.name]:
                    category_number[channel.category.name][f"#{channel.name}"] = len(fetched_data)
            except AttributeError:
                category_number["No Category"][f"#{channel.name}"] = len(fetched_data)

    desc = ".\n"

    iii = 1
    for key,value in category_number.items():  
        desc += f"├── 📁 {key}: {sum_of_links_for_key(category_number,key)}\n"
        ii = 1
        for channel,num_of_links in value.items():
            if ii < len(value.items()):
                desc += f"│   ├── {channel}: {num_of_links}\n"
            else:
                desc += f"│   └── {channel}: {num_of_links}\n"
            ii+=1
        if iii < len(category_number.items()):
            desc += "│\n"
        iii+=1
    
    


    desc += f"\n🔗 Links: {num_all_links(category_number)}.\n"
    contri_stats = await give_contribution_stats(id,bot,True)
    desc += f"💾 Data: {contri_stats}"


    return desc
            

