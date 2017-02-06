# coding: utf-8
import sys
import socket
import urllib
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import _privatekeys as privatekeys

### variable defaults
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
timeout_in_seconds = 30 

def mobileFriendlyCheck(request_url, api_key):
	"""	Example of Python talking to Google Search Console URL Testing Tools API.
	Documentation: https://developers.google.com/webmaster-tools/search-console-api/v1/samples

	attributes: 'request_url' for the URL to test, 'api_key' for the API key credentials fetched at Googles API Console
"""
	service_url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'

	params = {
	    'url': request_url,
	    'key': api_key,
	}
	data = urllib.parse.urlencode(params).encode("utf-8")
	content = urllib.request.urlopen(url=service_url, data=data, timeout=90).read()
	print(content)

def httpStatusCodeCheck(url, simulate_404 = False):
	"""Checking for a presumed 404 message

	Attributes: url
	"""
	if(simulate_404):
		url = '{0}/{1}'.format(url, 'sp4m-b34t2-k3b4b?') # changing the URL, trying to provoke a 404 Not Found
		# consider sitemap.xml, robots.txt, humans.txt, etc

	try:
		q = urllib.request.Request(url)
		q.add_header('User-agent', user_agent)
		a = urllib.request.urlopen(q, timeout=timeout_in_seconds)

		return a.code	# returns the status code for HTTP, 200 for Ok, 404 for Not found, etc
	except urllib.error.URLError as e:
		if hasattr(e, 'code'):
			return e.code
		else:
			return '520'
	except socket.timeout:
		return '522'	# not sure which error code to choose, but 520-522 seems reasonable according to https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
	except:
		return '520'

def httpRequestGetContent(url):
	"""Trying to fetch the response content
	Attributes: url, as for the URL to fetch
	"""
	try:
		q = urllib.request.Request(url)
		q.add_header('User-agent', user_agent)
		a = urllib.request.urlopen(q, timeout=timeout_in_seconds)

		return a.read()
	except:	
		print('Error! Unfortunately the request for URL "{0}" either timed out or failed for other reason(s). The timeout is set to {1} seconds.\nMessage:\n{2}'.format(url, timeout_in_seconds, sys.exc_info()[0]))
		pass

"""
If file is executed on itself then call definition mobileFriendlyCheck()
"""
if __name__ == '__main__':
	print('Initiating definition "httpStatusCodeCheck()"')
	#print(httpRequestGetContent("http://gp43789435.se"))
	print(httpStatusCodeCheck("http://www.ersattningsnamnden.se/"))
	#mobileFriendlyCheck('http://www.varberg.se/byggabomiljo/fastigheterlantmateriochkartor/kartor/saanvanderdudigitalavarbergskartan.4.7b99eb041540f79d87d77155.html', privatekeys.googleMobileFriendlyApiKey)