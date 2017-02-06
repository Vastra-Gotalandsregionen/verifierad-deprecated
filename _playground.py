from bs4 import BeautifulSoup
import test

def fetchUrlsFromSitemap(url):
	"""Given a URL of a sitemap or sitemapindex the contained URLs are returned as a set.
		
		Attributes: url
	"""
	found_urls = set()
	sitemap = test.httpRequestGetContent(url)

	if('<sitemapindex' in str(sitemap)):	# is the sitemap itself an index of sitemaps
		#foreach sitemap, hämta sitemap, koka ur urlar
		print("It\'s an index!")
		soup = BeautifulSoup(sitemap, "html.parser")

		for url in soup.findAll("loc"):
			print(url.text)
	else:
		soup = BeautifulSoup(sitemap, "html.parser")

		for url in soup.findAll("loc"):
			print(url.text)

	return found_urls


fetchSitemap('http://webbstrategiforalla.se/page-sitemap.xml')
#http://webbstrategiforalla.se/page-sitemap.xml
#http://webbstrategiforalla.se/sitemap.xml