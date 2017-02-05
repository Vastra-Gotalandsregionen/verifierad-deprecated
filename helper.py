# coding: utf-8
""" This file is where things are stuffed away. PRobably you don't ever need to alter these definitions.
"""
import uuid

def writeFile(file, content):
	f = open(file, 'w')
	f.write(content)

	f.close()


def getUniqueId(length = 5):
	return str(uuid.uuid1()).replace('-', '')[:length]