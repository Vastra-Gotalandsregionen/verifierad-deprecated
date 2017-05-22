import json
import sys

from bs4 import BeautifulSoup

import _privatekeys as privatekeys
import helper


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
            return_dict[key] = json_content['formattedResults']['ruleResults'][key]['ruleImpact']
        return return_dict
    except:
        print('Error! Request for URL "{0}" failed.\nMessage:\n{1}'.format(check_url,
                                                                           sys.exc_info()[
                                                                               0]))
        pass
