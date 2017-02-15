# coding: utf-8
import sys
import json
import html
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

	try:
		get_content = helper.httpRequestGetContent(pagespeed_api_request)
		get_content = BeautifulSoup(get_content, "html.parser")
		get_content = str(get_content.encode("ascii"))
		#print(get_content)
	except:	# breaking and hoping for more luck with the next URL
		print('Error! Unfortunately the request for URL "{0}" timed out, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
	json_content = ''
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
	# fixa nån form av iterering?
	print(json_content['formattedResults']['ruleResults']['AvoidLandingPageRedirects']['ruleImpact'])

	print(return_dict['stats_numberjsresources'])

	return return_dict

googlePagespeedCheck('http://vgregion.se')


#f = open('exempelfiler/mobileFriendlyTest.json', 'r').read()
#print(f)

#array = '{"fruits": ["apple", "banana", "orange"]}'
#data  = json.loads(f)
#print(data['mobileFriendliness'])