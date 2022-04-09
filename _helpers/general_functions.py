from urlextract import URLExtract

extractor = URLExtract()
extractor.update_when_older(7)

def find_all_urls_in_str(message):
    return extractor.find_urls(message)

