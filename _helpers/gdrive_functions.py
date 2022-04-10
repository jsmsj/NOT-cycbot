import re
import urllib.parse as urlparse
from urllib.parse import parse_qs
from _helpers.file_size_check import GoogleDriveSizeCalculate,service
import discord
import random,string
import asyncio,subprocess

def getIdFromUrl(link: str):
    # if len(link) in [33, 19]:
    #     return link
    if "folders" in link or "file" in link:
        regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/(?P<id>[-\w]+)[?+]?/?(w+)?"
        res = re.search(regex,link)
        if res is None:
            raise IndexError("GDrive ID not found.")
        return res.group('id')
    parsed = urlparse.urlparse(link)
    return parse_qs(parsed.query)['id'][0]

async def execute(command):
    cmd = ' '.join(command)
    proc = await asyncio.create_subprocess_shell(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    await proc.wait()
    stdout,stderr = await proc.communicate()
    if stdout:
        return stdout.decode()
    if stderr:
        return stderr.decode()

def get_readable_file_size(size_in_bytes) -> str:
    SIZE_UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)} {SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def make_url(source):
    if "https://" in source or "http://" in source:
        return source
    else:
        if source.startswith("drive.google.com"):
            sour = "https://" + source
            return sour 
        else:
            try:
                source = getIdFromUrl(source)
            except KeyError:
                return "Source id not found"
            sour = "http://drive.google.com/open?id=" + source
            return sour

def file_or_folder_size(gdrive_id):
    calculator = GoogleDriveSizeCalculate(service)
    result = calculator.gdrive_checker(gdrive_id)
    return result["bytes"]

async def gc_size(gdrive_id):
    gdrive_id = "{" + gdrive_id + "}"
    cmd = ["gclone", "size",f"GC:{gdrive_id}","--fast-list"]
    pattern = re.compile(r"\((\d+)")
    out = await execute(cmd)
    testing = out.splitlines()
    if testing[-1] == "Total size: 0 Bytes (0 Bytes)" and testing[0] == "Total objects: 0":
        gdrive_id = gdrive_id[1:-1]
        out = file_or_folder_size(gdrive_id)
        return out
    else:
        matches = re.finditer(pattern,out)
        for match in matches:
            return int(match.group(1))

def get_id(url):
    try:
        source = getIdFromUrl(url)
    except IndexError:
        return f"Source id not found in {url}"
    return source

def random_alphanumeric():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return x

async def send_name(ctx,url):
    calculator = GoogleDriveSizeCalculate(service)
    result = calculator.gdrive_checker(getIdFromUrl(url))
    try:
        main_name = result['name']
    except:
        main_name = ""
    name = f"{main_name} | {ctx.author.name} | {random_alphanumeric()}"
    return name