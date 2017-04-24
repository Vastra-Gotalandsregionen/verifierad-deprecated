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

def googlePagespeedCheck(check_url, strategy='mobile'):
	"""Checks the Pagespeed Insights with Google 
	In addition to the 'mobile' strategy there is also 'desktop' aimed at the desktop user's preferences
	Returns a dictionary of the results.

	attributes: check_url, strategy
	"""
	check_url = check_url.strip()
	
	#urlEncodedURL = parse.quote_plus(check_url)	# making sure no spaces or other weird characters f*cks up the request, such as HTTP 400
	pagespeed_api_request = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={}&strategy={}&key={}'.format(check_url, strategy, privatekeys.googlePageSpeedApiKey)
	print('HTTP request towards GPS API: {}'.format(pagespeed_api_request))

	responsecontents = ""
	get_content = ""

	try:
		get_content = httpRequestGetContent(pagespeed_api_request)
		get_content = BeautifulSoup(get_content, "html.parser")
		get_content = str(get_content.encode("ascii"))
	except:	# breaking and hoping for more luck with the next URL
		print('Error! Unfortunately the request for URL "{0}" timed out, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
	#try:
	get_content = get_content[2:][:-1] #removes two first chars and the last one
	get_content = get_content.replace('\\n', '\n').replace("\\'", "\'") #.replace('"', '"') #.replace('\'', '\"')
	get_content = get_content.replace('\\\\"', '\\"').replace('""', '"')
	
	json_content = ''
	try:
		json_content = json.loads(get_content)
	except: #might crash if checked resource is not a webpage
		print('Error! The URL "{0}" throw an error, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		return
	#except:	# breaking and hoping for more luck the next iteration
	#	print('Fudge! An error occured:\n{0}'.format(sys.exc_info()[0]))
	#	return pagespeedScore
	return_dict = {}
	try:
		# TODO: build error-safe
		pagespeed_score = json_content['ruleGroups']['SPEED']['score']
		return_dict['pagespeed_score'] = pagespeed_score
		#print(pagespeed_score)
		usability_score = json_content['ruleGroups']['USABILITY']['score']
		return_dict['usability_score'] = usability_score
		#print(usability_score)

		### the web page's stats
		stats_numberresources = json_content['pageStats']['numberResources']
		return_dict['stats_numberresources'] = stats_numberresources
		stats_numberresources = json_content['pageStats']['numberResources']
		return_dict['stats_numberresources'] = stats_numberresources
		stats_numberhosts = json_content['pageStats']['numberHosts']
		return_dict['stats_numberhosts'] = stats_numberhosts
		stats_totalrequestbytes = json_content['pageStats']['totalRequestBytes']
		return_dict['stats_totalrequestbytes'] = stats_totalrequestbytes
		stats_numberstaticresources = json_content['pageStats']['numberStaticResources']
		return_dict['stats_numberstaticresources'] = stats_numberstaticresources
		stats_htmlresponsebytes = json_content['pageStats']['htmlResponseBytes']
		return_dict['stats_htmlresponsebytes'] = stats_htmlresponsebytes
		stats_cssresponsebytes = json_content['pageStats']['cssResponseBytes']
		return_dict['stats_cssresponsebytes'] = stats_cssresponsebytes
		stats_imageresponsebytes = json_content['pageStats']['imageResponseBytes']
		return_dict['stats_imageresponsebytes'] = stats_imageresponsebytes
		stats_javascriptresponsebytes = json_content['pageStats']['javascriptResponseBytes']
		return_dict['stats_javascriptresponsebytes'] = stats_javascriptresponsebytes
		try:	
			stats_otherresponsebytes = json_content['pageStats']['otherResponseBytes']
			return_dict['stats_otherresponsebytes'] = stats_otherresponsebytes
		except:
			pass
		stats_numberjsresources = json_content['pageStats']['numberJsResources']
		return_dict['stats_numberjsresources'] = stats_numberjsresources
		stats_numbercssresources = json_content['pageStats']['numberCssResources']
		return_dict['stats_numbercssresources'] = stats_numbercssresources

		### rule results
		# TODO: not all ruleresults are present on all webpages, 'AvoidInterstitials' for instance
		ruleresults_avoidlandingpageredirects = json_content['formattedResults']['ruleResults']['AvoidLandingPageRedirects']['ruleImpact']
		return_dict['ruleresults_avoidlandingpageredirects'] = ruleresults_avoidlandingpageredirects
		ruleresults_minifycss = json_content['formattedResults']['ruleResults']['MinifyCss']['ruleImpact']
		return_dict['ruleresults_minifycss'] = ruleresults_minifycss
		ruleresults_optimizeimages = json_content['formattedResults']['ruleResults']['OptimizeImages']['ruleImpact']
		return_dict['ruleresults_optimizeimages'] = ruleresults_optimizeimages
		ruleresults_avoidplugins = json_content['formattedResults']['ruleResults']['AvoidPlugins']['ruleImpact']
		return_dict['ruleresults_avoidplugins'] = ruleresults_avoidplugins
		ruleresults_leveragebrowsercaching = json_content['formattedResults']['ruleResults']['LeverageBrowserCaching']['ruleImpact']
		return_dict['ruleresults_leveragebrowsercaching'] = ruleresults_leveragebrowsercaching
		ruleresults_prioritizevisiblecontent = json_content['formattedResults']['ruleResults']['PrioritizeVisibleContent']['ruleImpact']
		return_dict['ruleresults_prioritizevisiblecontent'] = ruleresults_prioritizevisiblecontent
		ruleresults_enablegzipcompression = json_content['formattedResults']['ruleResults']['EnableGzipCompression']['ruleImpact']
		return_dict['ruleresults_enablegzipcompression'] = ruleresults_enablegzipcompression
		#ruleresults_avoidinterstitials = json_content['formattedResults']['ruleResults']['AvoidInterstitials']['ruleImpact']
		#return_dict['ruleresults_avoidinterstitials'] = ruleresults_avoidinterstitials
		ruleresults_configureviewport = json_content['formattedResults']['ruleResults']['ConfigureViewport']['ruleImpact']
		return_dict['ruleresults_configureviewport'] = ruleresults_configureviewport
		ruleresults_uselegiblefontsizes = json_content['formattedResults']['ruleResults']['UseLegibleFontSizes']['ruleImpact']
		return_dict['ruleresults_uselegiblefontsizes'] = ruleresults_uselegiblefontsizes
		ruleresults_minimizerenderblockingresources = json_content['formattedResults']['ruleResults']['MinimizeRenderBlockingResources']['ruleImpact']
		return_dict['ruleresults_minimizerenderblockingresources'] = ruleresults_minimizerenderblockingresources
		ruleresults_minifyjavascript = json_content['formattedResults']['ruleResults']['MinifyJavaScript']['ruleImpact']
		return_dict['ruleresults_minifyjavascript'] = ruleresults_minifyjavascript
		ruleresults_mainresourceserverresponsetime = json_content['formattedResults']['ruleResults']['MainResourceServerResponseTime']['ruleImpact']
		return_dict['ruleresults_mainresourceserverresponsetime'] = ruleresults_mainresourceserverresponsetime
		ruleresults_sizetaptargetsappropriately = json_content['formattedResults']['ruleResults']['SizeTapTargetsAppropriately']['ruleImpact']
		return_dict['ruleresults_sizetaptargetsappropriately'] = ruleresults_sizetaptargetsappropriately
		ruleresults_minifyhtml = json_content['formattedResults']['ruleResults']['MinifyHTML']['ruleImpact']
		return_dict['ruleresults_minifyhtml'] = ruleresults_minifyhtml
		ruleresults_sizecontenttoviewport = json_content['formattedResults']['ruleResults']['SizeContentToViewport']['ruleImpact']
		return_dict['ruleresults_sizecontenttoviewport'] = ruleresults_sizecontenttoviewport

		#for key in return_dict:
		#	print(key, ' corresponds to ', return_dict[key])

		return return_dict
	except:
		print('Error! Request for URL "{0}" failed.\nMessage:\n{1}'.format(url, sys.exc_info()[0]))
		return

"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
	#fetchUrlsFromSitemap('http://webbstrategiforalla.se/sitemap.xml')
	#fetchUrlsFromSitemap('https://www.varberg.se/sitemap.xml')
	#httpRequestGetContent('http://vgregion.se')
	googlePagespeedCheck('http://varberg.se')
