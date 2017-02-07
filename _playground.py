# coding: utf-8
import sys
import json
from bs4 import BeautifulSoup
import helper
import _privatekeys as privatekeys

def googlePagespeedCheck(check_url, strategy='mobile'):
	"""Checks the Pagespeed Insights with Google 
	In addition to the 'mobile' strategy there is also 'desktop' aimed at the desktop user's preferences

	attributes: check_url, strategy
	"""

	pagespeedScore = ""
	check_url = check_url.strip()
	print('URL to be checked against Google Pagespeed API: {0}'.format(check_url))
	
	#urlEncodedURL = parse.quote_plus(check_url)	# making sure no spaces or other weird characters f*cks up the request, such as HTTP 400
	pagespeed_api_request = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={}&strategy={}&key={}'.format(check_url, strategy, privatekeys.googlePageSpeedApiKey)
	print('HTTP request towards GPS API: {}'.format(pagespeed_api_request))

	responsecontents = ""

	try:
		get_content = helper.httpRequestGetContent(pagespeed_api_request)
		#print(get_content)
	except:	# breaking and hoping for more luck with the next URL
		print('Error! Unfortunately the request for URL "{0}" timed out, message:\n{1}'.format(check_url, sys.exc_info()[0]))
		pass
	json_content = ''
	#try:
	json_content = json.loads(str(get_content))
		#data  = json.loads(f)
	#except:	# breaking and hoping for more luck the next iteration
	#	print('Fudge! An error occured:\n{0}'.format(sys.exc_info()[0]))
	#	return pagespeedScore

	print(json_content['USABILITY'])

googlePagespeedCheck('http://vgregion.se')


#f = open('exempelfiler/mobileFriendlyTest.json', 'r').read()
#print(f)

#array = '{"fruits": ["apple", "banana", "orange"]}'
#data  = json.loads(f)
#print(data['mobileFriendliness'])