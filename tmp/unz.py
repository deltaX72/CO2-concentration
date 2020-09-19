#-*- coding: utf-8 -*-

import tarfile
import zipfile


import requests

import os

# url.split('/')[-1]

def get_data(url, name):
	r = requests.get(url, allow_redirects = True)
	# cw = os.getcwd()
	os.mkdir(name.split('.')[0])
	os.chdir(name.split('.')[0])
	open(name, "wb").write(r.content)
	
	if name.endswith(".tar"):
		tar = tarfile.open(name, "r:")
		tar.extractall()
		tar.close()
	elif name.endswith(".tar.gz"):
		tar = tarfile.open(name, "r:gz")
		tar.extractall()
		tar.close()
	elif name.endswith(".zip"):
		temp = zipfile.ZipFile(name, "r")
		temp.extractall()
		temp.close()
	
	os.chdir("..")


get_data("https://download.geonames.org/export/dump/RU.zip", 'RU.zip')
get_data('https://download.geonames.org/export/dump/FR.zip', "FR.zip")

input("END")