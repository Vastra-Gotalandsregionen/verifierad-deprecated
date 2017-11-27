# coding: utf-8
"""
This file is the starting-point for the script(s).
Documentation is currently only available in Swedish at http://verifierad.nu
- which redirects to the official Github repository.

A change-log is kept in the file CHANGELOG.md
"""
from datetime import datetime
import sys

import _privatekeys as privatekeys
import test
import helper
from checks.google_pagespeed import google_pagespeed_check
# from checks.content import content_check, find_string # uncomment this line to try the preview of content checks

# local variables
# url_for_mainProcess = 'http://vgregion.se/'
i = 1  # global iteration counter


def oneOffProcess(file, test_regime='httpStatusCodeCheck'):
    """
    Inspects a textfile, assuming there's URLs in there, one URL per line.
    
    attributes: file path to open
    """
    f = open(file, 'r')

    urlsInTextfile = []
    iteration_counter = 1
    keep_on = True;
    time_to_sleep_in_seconds = 90  # TODO: reda ut varför Mobile Friendly inte orkar testa flera på raken, begränsning?

    output_file = ""
    i = 1

    while keep_on:
        url = f.readline().replace('\n', '')
        mess_to_console = '{0}. {1}'.format(iteration_counter, url)

        if len(url) < 7:  # break if line is shorter than seven characters
            keep_on = False
        elif not url.endswith('.pdf'):
            # depending on which test regime is chosen
            if test_regime == 'httpStatusCodeCheck':
                status_code = test.httpStatusCodeCheck(url, False)
                print('{0} has a status code: {1}'.format(mess_to_console,
                                                          status_code).replace('\n', ''))
                output_file += '{0}, {1}\n'.format(url.replace('\n', ''), status_code)
            elif test_regime == 'sitemapCheck':
                """
                Check the status code of domain.tld/sitemap.xml, assuming URL to only be the domain, not an URI
                """
                if url[-1:] is '/':
                    url = url[:-1]

                url = '{0}/{1}'.format(url, 'sitemap.xml')
                status_code = test.httpStatusCodeCheck(url, False)
                print('{0} has a status code: {1}'.format(mess_to_console,
                                                          status_code).replace('\n', ''))
                is_sitemap = "undefined"
                if str(status_code)[:1] is "2" or str(status_code)[:1] is "3": # checking if status code is either 200 series or 300
                    is_sitemap = helper.is_sitemap(helper.httpRequestGetContent(url))
                    print('Is sitemap: {0}'.format(is_sitemap))
                output_file += '{0}, {1}, {2}\n'.format(url.replace('\n', ''), status_code, is_sitemap)
            elif test_regime == 'urlHarvest':
                """
                Fetches URLs from a page's content
                """
                i = 0
                print('Harvesting URLs from {0}'.format(url))
                try:
                    for found_url in helper.fetchUrlsFromPage(url, 50):
                        output_file += '{0}\n'.format(found_url)
                        i+=1
                except:
                    print('Error! The URL {0} failed.'.format(url))
                    pass
                #print('Found {0} URLs from {1}'.format(i,url))
            elif test_regime == 'googlePageSpeed':
                check_page = google_pagespeed_check(url)
                if bool(check_page):
                    print('{0} has been checked against Google Pagespeed API'.format(
                        mess_to_console))
                    for key in check_page:
                        output_file = output_file + '{0},{1},{2}\n'.format(url, key,
                                                                           check_page[
                                                                               key])
            elif test_regime == 'mobileFriendlyCheck':
                print(url)
                status_message = test.mobileFriendlyCheck(url,
                                                          privatekeys.googleMobileFriendlyApiKey)
                print(
                    "Mobile-friendliness of URL '{0}' were evaluated as: {1}".format(url,
                                                                                     status_message))
                output_file += '{0}, {1}\n'.format(url.replace('\n', ''), status_message)
                sleep(time_to_sleep_in_seconds)  # sleeping for n seconds
            elif test_regime == 'contentCheck':
                print("{0}. Checking content of URL '{1}'.".format(i, url))
                for key, value in content_check(url).items():
                        output_file = output_file + '{0},{1},{2}\n'.format(url, key, value)
                i = i + 1
            elif test_regime == 'findString':
                searching = find_string('piwik', url)
                print("{0}. Checking for string in URL '{1}' - {2}".format(i, url, searching))
                output_file = output_file + '{0},{1}\n'.format(url, searching)
                i = i + 1
            
            # sleep(time_to_sleep_in_seconds)  # sleeping for n seconds

            urlsInTextfile.append(url)
            iteration_counter += 1

    f.close()

    ### Writing the report
    file_name = 'rapporter/{0}_{1}_{2}.csv'.format(str(datetime.today())[:10],
                                                   test_regime, helper.getUniqueId())
    helper.writeFile(file_name, output_file)

    print('The report has now been written to a file named: {0}'.format(file_name))


def oneOffFromSitemap(url_to_sitemap, check_limit,
                      date_limit, naming, test_regime):

    """Initially only checks a site against Google Pagespeed API
    """
    urls = helper.fetchUrlsFromSitemap(url_to_sitemap, date_limit)

    i = 1
    output_file = ''

    for url in urls:
        mess_to_console = '{0}. {1}'.format(i, url[1])
        if i > check_limit:
            break
        try:
            if test_regime == 'googlePageSpeed':
                check_page = google_pagespeed_check(url[1])
                if bool(check_page):
                    print('{0} has been checked against Google Pagespeed API'.format(
                        mess_to_console))
                    for key in check_page:
                        output_file = output_file + '{0},{1},{2}\n'.format(url[1], key,
                                                                           check_page[
                                                                               key])

                    i = i + 1
            elif test_regime == 'httpStatusCodeCheck':
                status_code = test.httpStatusCodeCheck(url[1], False)
                print('{0}. {01} has a status code: {2}'.format(i, mess_to_console, status_code))
                output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''), status_code)
                i = i + 1
            elif test_regime == 'mobileFriendlyCheck':
                status_message = test.mobileFriendlyCheck(url[1],
                                                          privatekeys.googleMobileFriendlyApiKey)
                print("{0}. Mobile-friendliness of URL '{1}' were evaluated as: {2}".format(i, 
                    url[1], status_message))
                output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''),
                                                   status_message)
                i = i + 1
            elif test_regime == 'thirdPartiesCheck':
                status_message = test.thirdPartiesCheck(url[1])
                print("{0}. Third parties of URL '{1}' were evaluated as: {2}".format(i, url[1],
                                                                                 status_message))
                output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''),
                                                   status_message)
                i = i + 1
            elif test_regime == 'contentCheck':
                print("{0}. Checking content of URL '{1}'.".format(i, url[1]))
                for key, value in content_check(url[1]).items():
                        output_file = output_file + '{0},{1},{2}\n'.format(url[1], key, value)
                i = i + 1
        except:
            print('Error! The request for URL "{0}" failed.\nMessage:\n{2}'.format(url[1],
                                                                                   sys.exc_info()[
                                                                                       0]))
            pass
            i = i + 1

    # Writing the report
    file_name = 'rapporter/{0}_{1}_{2}.csv'.format(str(datetime.today())[:10], naming,
                                                   helper.getUniqueId())
    helper.writeFile(file_name, output_file)
    print('Report written to disk at {0}'.format(file_name))


# supposed to support scheduling from bash-scripts or hosts such as PythonAnywhere
                      
def checkSitemapsForNewUrls(file, check_limit, date_limit, test_regime):
    """
    Checking a list of predefined sitemaps for new or updated URLs
    
    Attributes: string file (for the file location on disk)
    """
    f = open(file, 'r')

    for line in f:
        sitemap = line.replace('\n', '')
        sitemap_friendly_name = sitemap.replace('http://', '').replace('https://', '').replace('/', '-')
        print('\nInitiating check of sitemap: {0}'.format(sitemap))
        oneOffFromSitemap(sitemap, check_limit,
                      date_limit, '{0}-{1}'.format(test_regime, sitemap_friendly_name), test_regime)


# iterera runt de URLar som finns och anropa sitemaps
# kolla om det finns material som är mindre än 14 dagar gammalt (i slutändan kör man denna dagligen per sajt, typ)

# bygga ett register över URLars ålder

# om ny URL hittas så läggs den i en textfil som kollas på i slutet av exekveringen

"""
If file is executed on itself then call on a definition
"""
if __name__ == '__main__':
    oneOffProcess('exempelfiler/test-urls.txt', 'sitemapCheck')
    # oneOffFromSitemap('http://www.vgregion.se/sitemap.xml', 2000,
    #                  '2017-02-17T06:19:00+01:00', 'contentCheck', 'contentCheck')
    # checkSitemapsForNewUrls('exempelfiler/sitemaps.txt')
 	# checkSitemapsForNewUrls('exempelfiler/sitemaps.txt', check_limit=99999, date_limit='2017-08-01T06:19:00+01:00', test_regime='contentCheck')
    # for key, value in content_check('http://webbstrategiforalla.se/konferenser/').items():
    #    print("{key}: {value}".format(key=key, value=value))