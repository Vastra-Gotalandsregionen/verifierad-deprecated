# coding: utf-8
import sys
import json
import html
import urllib
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
#from bs4.dammit import EntitySubstitution
import helper
import _privatekeys as privatekeys

def googlePagespeedCheck(check_url, strategy='mobile'):
	"""Checks the Pagespeed Insights with Google 
	In addition to the 'mobile' strategy there is also 'desktop' aimed at the desktop user's preferences

	attributes: check_url, strategy
	"""
	check_url = check_url.strip()
	print('URL to be checked against Google Pagespeed API: {0}'.format(check_url))
	
	#urlEncodedURL = parse.quote_plus(check_url)	# making sure no spaces or other weird characters f*cks up the request, such as HTTP 400
	pagespeed_api_request = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={}&strategy={}&key={}'.format(check_url, strategy, privatekeys.googlePageSpeedApiKey)
	print('HTTP request towards GPS API: {}'.format(pagespeed_api_request))

	responsecontents = ""
	get_content = ""

	try:
		q = urllib.request.Request(pagespeed_api_request)
		q.add_header('User-agent', "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
		a = urllib.request.urlopen(q, timeout=30)
		get_content = a.read()
		#print(get_content)
		#get_content = helper.httpRequestGetContent(pagespeed_api_request)
		get_content = BeautifulSoup(get_content, "html.parser")
		get_content = str(get_content.encode("ascii"))
		#print(get_content)
	except:	# breaking and hoping for more luck with the next URL
		print('Error! Unfortunately the request for URL "{0}" timed out, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
	#json_content = ''
	#try:
	get_content = get_content[2:][:-1] #removes two first chars and the last one
	get_content = get_content.replace('\\n', '\n').replace("\\'", "\'") #.replace('"', '"') #.replace('\'', '\"')
	get_content = get_content.replace('\\\\"', '\\"').replace('""', '"')
	
	json_content = json.loads(get_content)
	#except:	# breaking and hoping for more luck the next iteration
	#	print('Fudge! An error occured:\n{0}'.format(sys.exc_info()[0]))
	#	return pagespeedScore
	return_dict = {}

	pagespeed_score = json_content['ruleGroups']['SPEED']['score']
	return_dict['pagespeed_score'] = pagespeed_score
	usability_score = json_content['ruleGroups']['USABILITY']['score']
	return_dict['usability_score'] = usability_score

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
	stats_otherresponsebytes = json_content['pageStats']['otherResponseBytes']
	return_dict['stats_otherresponsebytes'] = stats_otherresponsebytes
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

	for key in return_dict:
		print(key, ' corresponds to ', return_dict[key])

	return return_dict

googlePagespeedCheck('http://vgregion.se')