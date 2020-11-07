import json
import os
import requests
import wget

settings = {}

with open("settings.json", 'r') as file:
	settings = json.load(file)

def download_archieve(url: str, http_user: str, http_password: str, output_directory: str):
	os.system(f"wget {url} --http-user='{http_user}' --http-passwd='{http_password}' -P '{output_directory}'")

def unpack(path_to_archieve: str, output_directory: str):
    os.system(f"tar -xvf '{path_to_archieve}' -C '{output_directory}'")


# index = 0
for url in settings["urls"]:
	download_archieve(url, settings["user"], settings["password"], settings["directories"]["archieves"])
	
	# r = requests.get(url, allow_redirects=True)
	# lines = url.split("/")
	# open(f'{settings["directories"]["archieves"]}/{lines[len(lines) - 1]}.txt', "wb").write(r.content)
	# index += 1
