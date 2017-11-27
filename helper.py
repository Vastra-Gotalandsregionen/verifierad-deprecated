# coding: utf-8
""" This file is where things are stuffed away. Probably you don't ever need to alter these definitions.
"""
import sys
import os.path
import uuid
import dateutil.parser
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import gzip
import requests
import json
# internal
import _privatekeys as privatekeys

i = 0  # global iterator


def writeFile(file, content):
    """Writes a file at given location

    Attributes: file for location, content for the file's contents
    """
    f = open(file, 'w')
    f.write(content)

    f.close()

def delete_file(file):
    os.remove(file)

def getUniqueId(length=5):
    return str(uuid.uuid1()).replace('-', '')[:length]


def getKey(item):
    return item[0]


def fetchUrlsFromSitemap(url, limit=None):
    """Given a URL of a sitemap or sitemapindex the contained URLs are returned as a list with tuples. Optional to limit the age of URLs.
        
        Attributes: url (string), limit (datetime)
    """
    # Documentation for sitemaps - https://www.sitemaps.org
    found_urls = list()
    sitemap = httpRequestGetContent(url)
    global i
    if limit is not None:
        limit = dateutil.parser.parse(limit).replace(tzinfo=None)  # converts to same format

    if ('<sitemapindex' in str(sitemap)):  # is the sitemap itself an index of sitemaps
        sitemap_content = BeautifulSoup(sitemap, "html.parser")
        for url in sitemap_content.findAll("loc"):
            print("Siteindex found. Including URL:s from sitemap: '{0}'".format(url.text))

            # fetching sitemap
            sitemap_from_index = httpRequestGetContent(url.text)
            sitemap_iteration = BeautifulSoup(sitemap_from_index, "html.parser")

            for lvl1_url in sitemap_iteration.findAll("url"):
                date = None
                if (".pdf" not in lvl1_url.text.lower()) and (
                    ".jpg" not in lvl1_url.text.lower()) and (
                    ".mp4" not in lvl1_url.text.lower()) and (
                    ".mp3" not in lvl1_url.text.lower()) and (
                    ".txt" not in lvl1_url.text.lower()) and (
                    ".png" not in lvl1_url.text.lower()) and (
                    ".gif" not in lvl1_url.text.lower()) and (
                    ".svg" not in lvl1_url.text.lower()) and (
                    ".eps" not in lvl1_url.text.lower()) and (
                    ".doc" not in lvl1_url.text.lower()) and (
                    ".docx" not in lvl1_url.text.lower()) and (
                    ".xls" not in lvl1_url.text.lower()) and (
                    ".js" not in lvl1_url.text.lower()) and (
                    ".css" not in lvl1_url.text.lower()) and (
                    ".xlsx" not in lvl1_url.text.lower()) and (
                    ".ttf" not in lvl1_url.text.lower()) and (
                    ".eot" not in lvl1_url.text.lower()) and (
                    ".bak" not in lvl1_url.text.lower()) and (
                    ".woff" not in lvl1_url.text.lower()) and (
                    "javascript:" not in lvl1_url.text.lower()) and (
                    "tel:" not in lvl1_url.text.lower()) and (
                    "mailto:" not in lvl1_url.text.lower()) and (
                    "#" not in lvl1_url.text.lower()):
                    if lvl1_url.lastmod is not None:
                        date = dateutil.parser.parse(lvl1_url.lastmod.string).replace(tzinfo=None)
                    if limit is not None and date is not None and date > limit:
                        date_and_url = (lvl1_url.lastmod.string, lvl1_url.loc.string)
                        found_urls.append(
                            date_and_url)  # if date (lastmod) is missing the URL will not be checked

        print(
            'Found {0} URLs from multiple sitemaps in the siteindex you provided.'.format(
                len(found_urls)))
        return sorted(found_urls, key=getKey, reverse=True)
    else:
        soup = BeautifulSoup(sitemap, "html.parser")

        for url in soup.findAll("url"):
            date = None
            if url.lastmod is not None:
                date = dateutil.parser.parse(url.lastmod.string).replace(tzinfo=None)
            if limit is not None and date is not None and date > limit:
                date_and_url = (url.lastmod.string, url.loc.string)
                found_urls.append(
                    date_and_url)  # if date (lastmod) is missing the URL will not be checked

    print('Found {0} URLs in the sitemap you provided.'.format(len(found_urls)))
    return sorted(found_urls, key=getKey, reverse=True)


def fetchUrlsFromPage(url, num_limit=None, local_only=True):
    """Given a URL contained URLs are returned as a list with tuples. Optional to number of URLs and if to only include URLs within the local website.
        
        Attributes: url (string), num_limit (integer), local_only (bool)
    """
    main_url = urlparse(url)
    found_urls = list()
    page = httpRequestGetContent(url)
    soup = BeautifulSoup(page, "html.parser")
    i = 0
    
    for the_url in soup.find_all('a', href=True):
        if (".pdf" not in the_url['href'].lower()) and (
                ".jpg" not in the_url['href'].lower()) and (
                ".mp4" not in the_url['href'].lower()) and (
                ".mp3" not in the_url['href'].lower()) and (
                ".txt" not in the_url['href'].lower()) and (
                ".png" not in the_url['href'].lower()) and (
                ".gif" not in the_url['href'].lower()) and (
                ".svg" not in the_url['href'].lower()) and (
                ".eps" not in the_url['href'].lower()) and (
                ".doc" not in the_url['href'].lower()) and (
                ".docx" not in the_url['href'].lower()) and (
                ".xls" not in the_url['href'].lower()) and (
                ".js" not in the_url['href'].lower()) and (
                ".css" not in the_url['href'].lower()) and (
                ".xlsx" not in the_url['href'].lower()) and (
                ".ttf" not in the_url['href'].lower()) and (
                ".eot" not in the_url['href'].lower()) and (
                ".bak" not in the_url['href'].lower()) and (
                ".woff" not in the_url['href'].lower()) and (
                "javascript:" not in the_url['href'].lower()) and (
                "tel:" not in the_url['href'].lower()) and (
                "callto:" not in the_url['href'].lower()) and (
                "mailto:" not in the_url['href'].lower()) and (
                "#" not in the_url['href'].lower()):
                    found_url = urlparse(the_url['href'])

                    if local_only and (len(found_url.netloc) is 0 or found_url.netloc is main_url.netloc):
                        if len(found_url.netloc) is 0:
                            found_url = urljoin(url, found_url.geturl())
                            if found_url not in found_urls:   # making the entries unique
                                found_urls.append(found_url)
                                i+=1

    if num_limit is not None:
        found_urls = found_urls[:num_limit]

    print('Found {0} URLs on the page you provided, returning {1} of them.'.format(i, len(found_urls)))
    return found_urls[:num_limit]


def getGzipedContentFromUrl(url):
    """
    Fetching a gziped file from Internet, unpacks it and returns its contents.
    """
    unique_id = getUniqueId(5)
    file_name = 'tmp/file-{0}.gz'.format(unique_id)

    try:
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        with gzip.open(file_name, 'rb') as f:
            file_content = f.read()

        return file_content
    except SSLError:
        if 'http://' in url: # trying the same URL over SSL/TLS
            return getGzipedContentFromUrl(url.replace('http://', 'https://'))
        else:
            return None
    except:
        print(
            'Error! Unfortunately the request for URL "{0}" either timed out or failed for other reason(s). The timeout is set to {1} seconds.\nMessage:\n{2}'.format(
                url, timeout_in_seconds, sys.exc_info()[0]))
        return None


def httpRequestGetContent(url):
    """Trying to fetch the response content
    Attributes: url, as for the URL to fetch
    """
    if '.gz' in url or '.gzip' in url:
        # the url indicates that it is compressed using Gzip
        return getGzipedContentFromUrl(url)

    timeout_in_seconds = 30

    try:
        a = requests.get(url)

        return a.text
    except requests.exceptions.SSLError:
        if 'http://' in url: # trying the same URL over SSL/TLS
            print('Info: Trying SSL before giving up.')
            return httpRequestGetContent(url.replace('http://', 'https://'))
    except requests.exceptions.ConnectionError:
        print(
            'Connection error! Unfortunately the request for URL "{0}" failed.\nMessage:\n{1}'.format(url, sys.exc_info()[0]))
        pass
    except:
        print(
            'Error! Unfortunately the request for URL "{0}" either timed out or failed for other reason(s). The timeout is set to {1} seconds.\nMessage:\n{2}'.format(url, timeout_in_seconds, sys.exc_info()[0]))
        pass


def is_sitemap(content):
    """Check a string to see if its content is a sitemap or siteindex.

    Attributes: content (string)
    """
    if 'http://www.sitemaps.org/schemas/sitemap/' in content or '<sitemapindex' in content: 
        return True

    return False


"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
    # fetchUrlsFromSitemap('http://webbstrategiforalla.se/sitemap.xml')
    # tmp = fetchUrlsFromSitemap('http://www.varberg.se/sitemap.xml', '2017-02-17T06:19:00+01:00')
    # print(len(tmp))

    # for bla in tmp:
    #    print('{0} lastmod for {1}'.format(bla[0], bla[1]))
    for url in fetchUrlsFromPage('https://www.arbetsformedlingen.se/', 20):
        print(url)

    # httpRequestGetContent('http://vgregion.se')
