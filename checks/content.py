# coding: utf-8
""" WARNING! Just a preview! 
Content checker

This check performs content analysis.

No API key required. But uses readability if not  - https://pypi.python.org/pypi/readability
"""
import sys
import subprocess
from datetime import datetime

from bs4 import BeautifulSoup

import helper


def content_check(check_url, strategy='mobile'):
    """
    Checks the Pagespeed Insights with Google 
    In addition to the 'mobile' strategy there is also 'desktop' aimed at the desktop user's preferences
    Returns a dictionary of the results.

    attributes: check_url, strategy
    """
    check_url = check_url.strip()
    return_dict = {}

    try:
        get_content = helper.httpRequestGetContent(check_url)
        soup = BeautifulSoup(get_content, "html.parser")
        # soup = soup.encode("ascii")

        pagetitle = soup.title.string
        return_dict['pagetitle'] = pagetitle
        pagetitle_length = len(pagetitle)
        return_dict['pagetitle_length'] = pagetitle_length
        num_links = len(soup.find_all('a'))
        return_dict['num_links'] = num_links

        # checking images
        num_images = len(soup.find_all('img'))
        return_dict['num_images'] = num_images

        images = soup.find_all('img')
        i = 0
        for image in images:
            if image.get('alt') is not None:
                i = i + 1
            # print(image.get('alt')) # for debugging

        num_images_without_alt = num_images - i
        return_dict['num_images_without_alt'] = num_images_without_alt

        try:
            meta_desc = soup.findAll(attrs={"name":"description"})[0]['content']
            return_dict['meta_desc'] = meta_desc
            meta_desc_length = len(meta_desc)
            return_dict['meta_desc_length'] = meta_desc_length
        except IndexError:
            return_dict['meta_desc'] = ''
            return_dict['meta_desc_length'] = 0
            pass
        except:
            print('Meta desc check for URL \'{0}\' failed, reason: {1}'.format(check_url, sys.exc_info()[0]))

        # checking readability
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()

        file_name = 'tmp/{0}_{1}_{2}.txt'.format(str(datetime.today())[:10], 'contentCheck',
                                                       helper.getUniqueId())
        helper.writeFile(file_name, visible_text)
        # readability = os.system('readability {0}'.format(file_name))
        readability = subprocess.check_output(['readability', file_name])
        readability = readability.decode("utf-8")

        helper.delete_file(file_name)
        # helper.writeFile('tmp/readability-output.txt', readability) # uncomment if you'd like to see the readability output

        for line in readability.split('\n'):
            # first_entry = line.split(':')[0].strip()
            try:
                return_dict[line.split(':')[0].strip()] = line.split(':')[1].strip()
            except:
                pass

            # print(meta_desc)

    except:  # breaking and hoping for more luck with the next URL
        print('Error! Unfortunately the request for URL "{0}" failed, message:\n{1}'.format(check_url, sys.exc_info()[0]))
        pass

    return return_dict


# För svenska
# Under 25  Barnböcker.
# 25 till 30  Enkla texter.
# 30 till 40  Normaltext / skönlitteratur.
# 40 till 50  Sakinformation, till exempel Wikipedia.
# 50 till 60  Facktexter.
# Över 60 Svåra facktexter / forskning / avhandlingar.

# för engelska
# https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests