# coding: utf-8
import sys
import requests
import json
from bs4 import BeautifulSoup
import re  # för thirdpartiescheck
import _privatekeys as privatekeys
import helper


def mobileFriendlyCheck(request_url, api_key):
    """	Example of Python talking to Google Search Console URL Testing Tools API.
    Documentation: https://developers.google.com/webmaster-tools/search-console-api/v1/samples

    attributes: 'request_url' for the URL to test, 'api_key' for the API key credentials fetched at Googles API Console
    """
    try:
        payload = {'url': request_url, 'key': api_key}
        r = requests.post(
            'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run',
            params=payload)
        # print(r.text)
        # print(r.url)
        json_data = json.loads(r.text.replace('\'', '"'))
        # print(str(json_data['mobileFriendliness']))
        return json_data['mobileFriendliness']
    except:
        print('Error! Failed to request API for {0}'.format(request_url))
        return


def httpStatusCodeCheck(url, simulate_404=False, time_out=30.000):
    """Checking HTTP status code, or a presumed 404 message

    Attributes: string url, bool simulate_404, decimal time_out
    """
    if (simulate_404):
        url = '{0}/{1}'.format(url,
                               'sp4m-b34t2-k3b4b?')  # changing the URL, trying to provoke a 404 Not Found
    # consider sitemap.xml, robots.txt, humans.txt, etc

    try:
        r = requests.get(url, timeout=time_out)

        return r.status_code
    except:  # not sure which error code to choose, but 520-522 seems reasonable according to https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        return '520'


def checkForFiles(url, file="robots.txt"):
    """ Used to check a domain for interesting default files

    Attributes: string url, string file
    """
    # interesting files are robots.txt, humans.txt, sitemap.xml
    return_dict = {}

    url = '{0}/{1}'.format(url, file)
    return_dict[url] = httpStatusCodeCheck(url)

    return return_dict


def googlePagespeedCheck(check_url, strategy='mobile'):
    """Checks the Pagespeed Insights with Google 
    In addition to the 'mobile' strategy there is also 'desktop' aimed at the desktop user's preferences
    Returns a dictionary of the results.

    attributes: check_url, strategy
    """
    check_url = check_url.strip()

    # urlEncodedURL = parse.quote_plus(check_url)	# making sure no spaces or other weird characters f*cks up the request, such as HTTP 400
    pagespeed_api_request = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={}&strategy={}&key={}'.format(
        check_url, strategy, privatekeys.googlePageSpeedApiKey)
    # print('HTTP request towards GPS API: {}'.format(pagespeed_api_request))

    responsecontents = ""
    get_content = ""

    try:
        get_content = helper.httpRequestGetContent(pagespeed_api_request)
        get_content = BeautifulSoup(get_content, "html.parser")
        get_content = str(get_content.encode("ascii"))
    except:  # breaking and hoping for more luck with the next URL
        print(
            'Error! Unfortunately the request for URL "{0}" failed, message:\n{1}'.format(
                check_url, sys.exc_info()[0]))
        pass
    # try:
    get_content = get_content[2:][:-1]  # removes two first chars and the last one
    get_content = get_content.replace('\\n', '\n').replace("\\'",
                                                           "\'")  # .replace('"', '"') #.replace('\'', '\"')
    get_content = get_content.replace('\\\\"', '\\"').replace('""', '"')

    json_content = ''
    try:
        json_content = json.loads(get_content)
    except:  # might crash if checked resource is not a webpage
        print('Error! JSON failed parsing for the URL "{0}"\nMessage:\n{1}'.format(
            check_url, sys.exc_info()[0]))
        pass

    return_dict = {}
    try:
        # overall score
        for key in json_content['ruleGroups'].keys():
            # print('Key: {0}, value {1}'.format(key, json_content['ruleGroups'][key]['score']))
            return_dict[key] = json_content['ruleGroups'][key]['score']

        # page statistics
        for key in json_content['pageStats'].keys():
            # print('Key: {0}, value {1}'.format(key, json_content['pageStats'][key]))
            return_dict[key] = json_content['pageStats'][key]

        # page potential
        for key in json_content['formattedResults']['ruleResults'].keys():
            # print('Key: {0}, value {1}'.format(key, json_content['formattedResults']['ruleResults'][key]['ruleImpact']))
            return_dict[key] = json_content['formattedResults']['ruleResults'][key][
                'ruleImpact']
        return return_dict
    except:
        print('Error! Request for URL "{0}" failed.\nMessage:\n{1}'.format(check_url,
                                                                           sys.exc_info()[
                                                                               0]))
        pass


def thirdPartiesCheck(url):
    """Checking third parties used on the URL

    Attributes: string url
    """
    get_content = helper.httpRequestGetContent(url)
    get_content = BeautifulSoup(get_content, "html.parser")

    for findings in get_content.select('img[src*="//"]'):
        print(findings)

    for findings in get_content.select('iframe[src*="//"]'):
        print(findings)
    for findings in get_content.select('link[href*="//"]'):
        print(findings)
    for findings in get_content.select('script[src*="//"]'):
        print(findings)
    for findings in get_content.select('script[src*="//"]'):
        print(findings)
    # komplettera med the usual suspects? Som '//ajax.googleapis.com/' i fritext?
    # inbäddade kartor, videoklipp, teckensnitt?


"""
If file is executed for itself
"""
if __name__ == '__main__':
    # print(httpStatusCodeCheck('http://vgregion.se'))
    # print(mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey))
    print(googlePagespeedCheck('http://varberg.se'))
# thirdPartiesCheck('http://sahlgrenska.se')
