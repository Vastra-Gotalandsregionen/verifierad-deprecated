# coding: utf-8
import requests
import json
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

"""
If file is executed for itself
"""
if __name__ == '__main__':
	print(httpStatusCodeCheck('http://vgregion.se', True))
	#print(mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey))