# coding: utf-8
""" This file is the starting-point for the script(s).
	Documentation is currently only available in Swedish. Located at http://verifierad.nu - which redirects to a Github repository.

	A change-log is kept in the file CHANGELOG.md
"""
from datetime import datetime
import sys
import time
import _privatekeys as privatekeys
import test
import helper

# local variables
#url_for_mainProcess = 'http://vgregion.se/'
i = 1 # global iteration counter

def oneOffProcess(file, test_regime = 'httpStatusCodeCheck'):
	""" Inspects a textfile, assuming there's URLs in there, one URL per line.
	
	attributes: file path to open
	"""
	f = open(file, 'r')

	urlsInTextfile = []
	iteration_counter = 1
	keep_on = True;
	time_to_sleep_in_seconds = 90	# TODO: reda ut varför den inte orkar testa flera på raken, begränsning?

	output_file = ""

	while keep_on:		
		url = f.readline().replace('\n', '')
		mess_to_console = '{0}. {1}'.format(iteration_counter, url)
		
		if len(url) < 7:		# break while if line is shorter than seven characters, for instance is http:// or https:// assumed as a prefix
			keep_on = False
		elif not url.endswith('.pdf'):
			# depending on which test regime is chosen
			if test_regime == 'httpStatusCodeCheck':
				status_code = test.httpStatusCodeCheck(url, False)
				print('{0} has a status code: {1}'.format(mess_to_console, status_code).replace('\n', ''))
				output_file += '{0}, {1}\n'.format(url.replace('\n', ''), status_code)
			elif test_regime == 'mobileFriendlyCheck':
				print(url)
				status_message = test.mobileFriendlyCheck(url, privatekeys.googleMobileFriendlyApiKey)
				print("Mobile-friendliness of URL '{0}' were evaluated as: {1}".format(url, status_message))
				output_file += '{0}, {1}\n'.format(url.replace('\n', ''), status_message)
				sleep(time_to_sleep_in_seconds) #sleeping for n seconds

			urlsInTextfile.append(url)
			iteration_counter += 1
		
	f.close()

	### Writing the report
	file_name = 'rapporter/{0}_{1}_{2}.csv'.format(str(datetime.today())[:10], test_regime, helper.getUniqueId())
	helper.writeFile(file_name, output_file)

	print('The report has now been written to a file named: {0}'.format(file_name))

def oneOffFromSitemap(url_to_sitemap, check_limit = 50, date_limit = '2017-02-17T06:19:00+01:00', naming = 'google_pagespeed', test_regime = 'googlePageSpeed'):
	"""Initially only checks a site against Google Pagespeed API
	"""
	#urls = set()
	urls = helper.fetchUrlsFromSitemap(url_to_sitemap, date_limit)
	
	#print(len(urls))
	i = 1
	output_file = ''

	for url in urls:
		mess_to_console = '{0}. {1}'.format(i, url[1])
		if i > check_limit:
			break
		try:
			if test_regime == 'googlePageSpeed':
				check_page = test.googlePagespeedCheck(url[1])
				if bool(check_page):
					print('{0} has been checked against Google Pagespeed API'.format(mess_to_console))
					for key in check_page:
						output_file = output_file + '{0},{1},{2}\n'.format(url[1], key, check_page[key])
					
					i = i + 1
			elif test_regime == 'httpStatusCodeCheck':
				status_code = test.httpStatusCodeCheck(url[1], False)
				print('{0} has a status code: {1}'.format(mess_to_console, status_code))
				output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''), status_code)
				i = i + 1
			elif test_regime == 'mobileFriendlyCheck':
				print(url[1])
				status_message = test.mobileFriendlyCheck(url[1], privatekeys.googleMobileFriendlyApiKey)
				print("Mobile-friendliness of URL '{0}' were evaluated as: {1}".format(url[1], status_message))
				output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''), status_message)
				i = i + 1
			elif test_regime == 'thirdPartiesCheck':
				print(url[1])
				status_message = test.thirdPartiesCheck(url[1])
				print("Third parties of URL '{0}' were evaluated as: {1}".format(url[1], status_message))
				output_file += '{0}, {1}\n'.format(url[1].replace('\n', ''), status_message)
				i = i + 1
		except:
			print('Error! The request for URL "{0}" failed.\nMessage:\n{2}'.format(url[1], sys.exc_info()[0]))
			pass
			i = i + 1

	### Writing the report
	file_name = 'rapporter/{0}_{1}_{2}.csv'.format(str(datetime.today())[:10], naming, helper.getUniqueId())
	helper.writeFile(file_name, output_file)
	print('Report written to disk at {0}'.format(file_name))

# supposed to support scheduling from bash-scripts or hosts such as PythonAnywhere
def checkSitemapsForNewUrls(file):
	""" Checking a list of predefined sitemaps for new or updated URLs
	
	Attributes: string file (for the file location on disk)
	"""
	#iterera runt de URLar som finns och anropa sitemaps
	#kolla om det finns material som är mindre än 14 dagar gammalt (i slutändan kör man denna dagligen per sajt, typ)

	# bygga ett register över URLars ålder

	# om ny URL hittas så läggs den i en textfil som kollas på i slutet av exekveringen

"""
If file is executed on itself then call on a definition
"""
if __name__ == '__main__':
	#oneOffProcess('exempelfiler/swe-gov.txt', 'httpStatusCodeCheck')
	#oneOffFromSitemap('http://www.vgregion.se/sitemap.xml', 100, 'vgregion-httpStatusCodeCheck', 'httpStatusCodeCheck')
	oneOffFromSitemap('http://www.varberg.se/sitemap.xml', 10, '2017-02-17T06:19:00+01:00', 'pagespeed', 'googlePageSpeed')

