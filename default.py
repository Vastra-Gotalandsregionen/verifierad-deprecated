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

		test.mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey)
		
		if(iteration_counter >= maximum_iterations):
			keep_on = False
			print('\n========== aaaand we\'re finished =========='.format(time_to_sleep_in_seconds))
		else:
			print('\n========== Going to sleep for {0} seconds =========='.format(time_to_sleep_in_seconds))
			sleep(time_to_sleep_in_seconds) #sleeping for n seconds

def oneOffProcess(file):
	""" Inspects a textfile, assuming there's URLs in there, one URL per line.
	
	attributes: file path to open
	"""
	f = open(file, 'r')

	urlsInTextfile = []
	iteration_counter = 1
	keep_on = True;

	output_file = ""

	while keep_on:		
		url = f.readline()
		mess_to_console = '{0}. {1}'.format(iteration_counter, url)
		
		if len(url) < 7:		# break while if line is shorter than seven characters, for instance is http:// or https:// assumed as a prefix
			keep_on = False
		elif not url.endswith('.pdf'):
			status_code = test.httpStatusCodeCheck(url)
			print('{0} has a status code: {1}'.format(mess_to_console, status_code).replace('\n', ''))

			output_file += '{0}, {1}\n'.format(url.replace('\n', ''), status_code)

			urlsInTextfile.append(url)
			iteration_counter += 1
		
	f.close()

	### Writing the report
	file_name = 'rapporter/{0}_httpStatusCodeCheck_{1}.csv'.format(str(datetime.today())[:10], helper.getUniqueId())
	helper.writeFile(file_name, output_file)

	print('The report has now been written to a file named: {0}'.format(file_name))


"""
If file is executed on itself then call definition mobileFriendlyCheck()
"""
if __name__ == '__main__':
	#mainProcess(maximum_iterations)
	oneOffProcess('ÄNDRA-MIG.txt')