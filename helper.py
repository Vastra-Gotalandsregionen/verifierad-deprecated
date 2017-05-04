# coding: utf-8
""" This file is where things are stuffed away. Probably you don't ever need to alter these definitions.
"""
import sys
import os.path
import uuid
from bs4 import BeautifulSoup
import gzip
import requests
import json
#internal
import _privatekeys as privatekeys

def writeFile(file, content):
	f = open(file, 'w')
	f.write(content)

	f.close()


def getUniqueId(length = 5):
	return str(uuid.uuid1()).replace('-', '')[:length]

def fetchUrlsFromSitemap(url):
	"""Given a URL of a sitemap or sitemapindex the contained URLs are returned as a set.
		
		Attributes: url
	"""
	# Documentation for sitemaps - https://www.sitemaps.org
	found_urls = set()
	sitemap = httpRequestGetContent(url)

	if('<sitemapindex' in str(sitemap)):	# is the sitemap itself an index of sitemaps
		sitemap_content = BeautifulSoup(sitemap, "html.parser")
		for url in sitemap_content.findAll("loc"):
			print("Sitemap found. Including URL:s from sitemap: '{0}'".format(url.text))

			# fetching sitemap
			sitemap_from_index = httpRequestGetContent(url.text)
			sitemap_iteration = BeautifulSoup(sitemap_from_index, "html.parser")

			for lvl1_url in sitemap_iteration.findAll("loc"):
				#print(lvl1_url.text)
				#extension = os.path.splitext(filename)[1]
				if (".pdf" not in lvl1_url.text.lower()) and (".jpg" not in lvl1_url.text.lower()) and (".mp4" not in lvl1_url.text.lower()) and (".mp3" not in lvl1_url.text.lower()) and (".txt" not in lvl1_url.text.lower()) and (".png" not in lvl1_url.text.lower()) and (".gif" not in lvl1_url.text.lower()) and (".svg" not in lvl1_url.text.lower()) and (".eps" not in lvl1_url.text.lower()) and (".doc" not in lvl1_url.text.lower()) and (".docx" not in lvl1_url.text.lower()) and (".xls" not in lvl1_url.text.lower()) and (".js" not in lvl1_url.text.lower()) and (".css" not in lvl1_url.text.lower()) and (".xlsx" not in lvl1_url.text.lower()) and (".ttf" not in lvl1_url.text.lower()) and (".eot" not in lvl1_url.text.lower()) and (".bak" not in lvl1_url.text.lower()) and (".woff" not in lvl1_url.text.lower()):
					found_urls.add(lvl1_url.text)
		print('Found {0} URLs from multiple sitemaps in the siteindex you provided.'.format(len(found_urls)))
		return found_urls
	else:
		soup = BeautifulSoup(sitemap, "html.parser")

		for url in soup.findAll("loc"):
			#print(url.text)
			if (".pdf" not in url.text.lower()) and (".jpg" not in url.text.lower()) and (".png" not in url.text.lower()) and (".gif" not in url.text.lower()) and (".eps" not in url.text.lower()) and (".svg" not in url.text.lower()) and (".js" not in url.text.lower()) and (".css" not in url.text.lower()) and (".ttf" not in url.text.lower()) and (".txt" not in url.text.lower()) and (".bak" not in url.text.lower()) and (".mp4" not in url.text.lower()) and (".mp3" not in url.text.lower()) and (".woff" not in url.text.lower()):
				found_urls.add(url.text)

	print('Found {0} URLs in the sitemap you provided.'.format(len(found_urls)))
	return found_urls

def getGzipedContentFromUrl(url):
	"""
	Fetching a gziped file from Internet, unpacks it and returns its contents.
	"""
	unique_id = getUniqueId(5)
	file_name = 'tmp/file-{0}.gz'.format(unique_id)

	r = requests.get(url, stream=True)
	with open(file_name, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=128):
			fd.write(chunk)

	with gzip.open(file_name, 'rb') as f:
		file_content = f.read()

	return file_content

def httpRequestGetContent(url):
	"""Trying to fetch the response content
	Attributes: url, as for the URL to fetch
	"""
	if '.gz' in url or '.gzip' in url:
		# the url indicates that it is compressed using Gzip
		return getGzipedContentFromUrl(url)

	try:
		a = requests.get(url)

		return a.text
	except:	
		print('Error! Unfortunately the request for URL "{0}" either timed out or failed for other reason(s). The timeout is set to {1} seconds.\nMessage:\n{2}'.format(url, timeout_in_seconds, sys.exc_info()[0]))
		pass

"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
	#fetchUrlsFromSitemap('http://webbstrategiforalla.se/sitemap.xml')
	#fetchUrlsFromSitemap('https://www.varberg.se/sitemap.xml')
	httpRequestGetContent('http://vgregion.se')
