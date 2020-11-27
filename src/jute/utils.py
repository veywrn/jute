from urllib.parse import urlparse


def isURL(location):
    return urlparse(location).scheme != ""
