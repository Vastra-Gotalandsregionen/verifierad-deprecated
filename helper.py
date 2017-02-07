# coding: utf-8
""" This file is where things are stuffed away. Probably you don't ever need to alter these definitions.
"""

### REQUIREMENTS
# Unfortunately (or not) you have to install Beautiful Soup 4, unless you remove the definition 'fetchUrlsFromSitemap' and also the import statement below. The documentation is found at https://www.crummy.com/software/BeautifulSoup/
### / REQUIREMENTS

import uuid
from bs4 import BeautifulSoup

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
	sitemap = test.httpRequestGetContent(url)

	if('<sitemapindex' in str(sitemap)):	# is the sitemap itself an index of sitemaps
		sitemap_content = BeautifulSoup(sitemap, "html.parser")
		for url in sitemap_content.findAll("loc"):
			print("Sitemap found. Including URL:s from sitemap: '{0}'".format(url.text))

			# fetching sitemap
			sitemap_from_index = test.httpRequestGetContent(url.text)
			sitemap_iteration = BeautifulSoup(sitemap_from_index, "html.parser")

			for lvl1_url in sitemap_iteration.findAll("loc"):
				#print(lvl1_url.text)
				found_urls.add(lvl1_url.text)

		print('Found {0} URLs from multiple sitemaps in the siteindex you provided.'.format(len(found_urls)))
		return found_urls
	else:
		soup = BeautifulSoup(sitemap, "html.parser")

		for url in soup.findAll("loc"):
			#print(url.text)
			found_urls.add(url.text)

	print('Found {0} URLs in the sitemap you provided.'.format(len(found_urls)))
	return found_urls

"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
	fetchUrlsFromSitemap('http://webbstrategiforalla.se/sitemap.xml')