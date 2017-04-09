# coding: utf-8
""" This file is the starting-point for the script(s).
	Documentation is currently only available in Swedish. Located at http://verifierad.nu - which redirects to a Github repository.

	A change-log is kept in the file CHANGELOG.md
"""
from time import sleep
from datetime import datetime
import _privatekeys as privatekeys
import test
import helper

######## set the variables to your chosing
maximum_iterations = 1 #defaults is 200


def mainProcess(maximum_iterations = 200):
	keep_on = True
	time_to_sleep_in_seconds = 30
	iteration_counter = 1

	while (keep_on):
		print('\n========== Iteration {0} =========='.format(iteration_counter))
		iteration_counter += 1

		test_result = test.mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey)
		print(test_result)
		
		if(iteration_counter >= maximum_iterations):
			keep_on = False
			print('\n========== aaaand we\'re finished =========='.format(time_to_sleep_in_seconds))
		else:
			print('\n========== Going to sleep for {0} seconds =========='.format(time_to_sleep_in_seconds))
			sleep(time_to_sleep_in_seconds) #sleeping for n seconds

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
				status_code = test.httpStatusCodeCheck(url, True)
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

def oneOffFromSitemap(url_to_sitemap, check_limit = 50):
	"""Initially only checks a site against Google Pagespeed API
	"""
	urls = set()
	urls = helper.fetchUrlsFromSitemap(url_to_sitemap)
	
	#print(len(urls))
	i = 1
	output_file = ''

	for url in urls:
		if i > check_limit:
			break
		check_page = helper.googlePagespeedCheck(url)
		if bool(check_page):
			for key in check_page:
				output_file = output_file + '{0}, {1}, {2}\n'.format(url, key, check_page[key])
		i = i + 1

	### Writing the report
	file_name = 'rapporter/{0}_{1}_{2}.csv'.format(str(datetime.today())[:10], 'google_pagespeed', helper.getUniqueId())
	helper.writeFile(file_name, output_file)
	print('Report written to disk at {0}'.format(file_name))
"""
If file is executed on itself then call on a definition
"""
if __name__ == '__main__':
	#mainProcess(maximum_iterations)
	#oneOffProcess('exempelfiler/test-urls.txt', 'httpStatusCodeCheck')
	oneOffFromSitemap('http://varberg.se/sitemap.xml', 100)