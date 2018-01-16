import hashlib
import os

import logging
logger = logging.getLogger('scraper')

CACHE_DIR = 'cache'
CACHE_DIR = 'cache'

def binary(fun):
    def wrapper(url):
        url_hash = hashlib.md5(url.encode('utf8')).hexdigest()
        cache_filepath = os.path.join(CACHE_DIR, url_hash)
        
        if not os.path.exists(cache_filepath):
            content = fun(url)
            logger.info("Writing binary file to '%s'", cache_filepath)
            with open(cache_filepath, 'wb') as fh:
                fh.write(content)
            return content
        else:
            logger.info("Found cached file '%s'", cache_filepath)
            with open(cache_filepath, 'rb') as fh:
                content = fh.read()
            return content
    return wrapper

def page(fun):
    def wrapper(url):
        url_hash = hashlib.md5(url.encode('utf8')).hexdigest()
        cache_filepath = os.path.join(CACHE_DIR, url_hash)
        if os.path.exists(cache_filepath):
            with open(cache_filepath) as fh:
                return fh.read()
        content = fun(url)
        with open(cache_filepath, 'w') as fh:
            fh.write(content.decode('utf8'))
        return content
    return wrapper

