# coding: utf-8
import sys
import requests
import json
from bs4 import BeautifulSoup
import _privatekeys as privatekeys
import helper

def mobileFriendlyCheck(request_url, api_key):
	"""	Example of Python talking to Google Search Console URL Testing Tools API.
	Documentation: https://developers.google.com/webmaster-tools/search-console-api/v1/samples

	attributes: 'request_url' for the URL to test, 'api_key' for the API key credentials fetched at Googles API Console
	"""
	try:
		payload = {'url': request_url, 'key': api_key}
		r = requests.post('https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run', params=payload)
		#print(r.text)
		#print(r.url)
		json_data  = json.loads(r.text.replace('\'', '"'))
		#print(str(json_data['mobileFriendliness']))
		return json_data['mobileFriendliness']
	except:
		print('Error! Failed to request API for {0}'.format(request_url))
		return

def httpStatusCodeCheck(url, simulate_404 = False, time_out=30.000):
	"""Checking HTTP status code, or a presumed 404 message

	Attributes: string url, bool simulate_404, decimal time_out
	"""
	if(simulate_404):
		url = '{0}/{1}'.format(url, 'sp4m-b34t2-k3b4b?') # changing the URL, trying to provoke a 404 Not Found
		# consider sitemap.xml, robots.txt, humans.txt, etc

	try:
		r = requests.get(url, timeout=time_out)

		return r.status_code
	except:	# not sure which error code to choose, but 520-522 seems reasonable according to https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
		return '520'

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
		get_content = helper.httpRequestGetContent(pagespeed_api_request)
		get_content = BeautifulSoup(get_content, "html.parser")
		get_content = str(get_content.encode("ascii"))
	except:	# breaking and hoping for more luck with the next URL
		print('Error! Unfortunately the request for URL "{0}" failed, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
	#try:
	get_content = get_content[2:][:-1] #removes two first chars and the last one
	get_content = get_content.replace('\\n', '\n').replace("\\'", "\'") #.replace('"', '"') #.replace('\'', '\"')
	get_content = get_content.replace('\\\\"', '\\"').replace('""', '"')
	
	json_content = ''
	try:
		json_content = json.loads(get_content)
	except: #might crash if checked resource is not a webpage
		print('Error! JSON failed parsing for the URL "{0}"\nMessage:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
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
		try:
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
		except:
			print('Error! Request for URL "{0}" failed in a minor way.\nMessage:\n{1}'.format(check_url, sys.exc_info()[0]))
			pass

		#for key in return_dict:
		#	print(key, ' corresponds to ', return_dict[key])

		return return_dict
	except:
		print('Error! Request for URL "{0}" failed.\nMessage:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass

def thirdPartiesCheck(url):
	"""Checking third parties used on the URL

	Attributes: string url
	"""
	

"""
If file is executed for itself
"""
if __name__ == '__main__':
	#print(httpStatusCodeCheck('http://vgregion.se', True))
	#print(mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey))
	print(googlePagespeedCheck('http://varberg.se'))

