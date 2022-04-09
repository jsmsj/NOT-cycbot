import re
import urllib.parse as urlparse
from urllib.parse import parse_qs
from _helpers.file_size_check import GoogleDriveSizeCalculate,service

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


def make_url(source):
    if "https://" in source or "http://" in source:
        return source
    else:
        if source.startswith("drive.google.com"):
            sour = "https://" + source
            return sour 
        else:
            sour = "http://drive.google.com/open?id=" + source
            return sour

def file_or_folder_size(gdrive_id):
    calculator = GoogleDriveSizeCalculate(service)
    result = calculator.gdrive_checker(gdrive_id)
    return result["bytes"]