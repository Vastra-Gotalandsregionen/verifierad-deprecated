
import urllib
from urllib.request import Request, urlopen
import _privatekeys as privatekeys

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

"""
If file is executed on itself then call definition mobileFriendlyCheck()
"""
if __name__ == '__main__':
	print('Initiating definition "mobileFriendlyCheck(url)"')
	mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey)