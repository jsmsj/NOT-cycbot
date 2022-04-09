from urlextract import URLExtract
import aiosqlite

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

async def give_contribution_stats(id,bot):
    async with bot.link_db.cursor() as cursor:
        await cursor.execute("SELECT object_size FROM links WHERE user_id = ?",(id,))
        fetched_data = await cursor.fetchall()
        total_posts = len(fetched_data)
        total_bytes = 0
        for i in fetched_data:
            total_bytes += i[0]

        readable_size = get_readable_file_size(total_bytes)
    
    if readable_size == 'File too large': return "You are literally a GOD, cause you have posted so much stuff."

    return f"{readable_size} in {total_posts} Posts."
