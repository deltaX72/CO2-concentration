import json
import os
# from h5_conv import read_data
import h5py
# import log

settings = {}

def read_data(dataset: h5py.File):
    data = []

    length = len(dataset['scanAttribute']['time'])
    for i in range(length):
        date_and_time = dataset['scanAttribute']['time'][i].split()
        data.append({
            "date": str(date_and_time[0].decode()),
            "time": str(date_and_time[1].decode()),
            "lat": str(dataset['Data']['geolocation']['latitude'][i]),
            "lon": str(dataset['Data']['geolocation']['longitude'][i]),
            "con": str(dataset['Data']['mixingRatio']['XCO2'][i])
        })
    
    return data

def load_into_file(path: str, filename: str, data: list):
    with open(path + filename, 'w') as file:
        for i in data:
            for d in i:
                line = "{} {} {} {} {}\n".format(d["date"], d["time"], d["lat"], d["lon"], d["con"])
                file.write(line)

def download_archieve(url: str, http_user: str, http_password: str, output_directory: str):
    os.system(f"wget '{url}' --http-user='{http_user}' --http-passwd='{http_password}' -P '{output_directory}'")

def unpack(path_to_archieve: str, output_directory: str):
    os.system(f"tar -xf '{path_to_archieve}' -C '{output_directory}'")

def cmd_download(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	year = year_from
	month = month_from

	while True:
		if month > 12:
			year += 1
			month = 1
		month_mask = ""
		if month < 10 and month > 0:
			month_mask = "0" + str(month)
		else:
			month_mask = str(month)
		mask = "https://data2.gosat.nies.go.jp/wgetdata/GU/SWIRL2CO2/{}/SWIRL2CO2_{}{}_{}.tar".format(
			str(year), str(year), month_mask, version
		)

		download_archieve(mask, settings["user"], settings["password"], settings["directories"]["archieves"])
		print(f"\n\n[{year}-{month_mask}] done!")
		if year == year_to and month == month_to:
			break

		month += 1

def cmd_unpack(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	year = year_from
	month = month_from

	while True:
		if month > 12:
			year += 1
			month = 1
		month_mask = ""
		if month < 10 and month > 0:
			month_mask = "0" + str(month)
		else:
			month_mask = str(month)
		mask = "SWIRL2CO2_{}{}_{}".format(str(year), month_mask, version)
		unpack("{}/{}.tar".format(settings["directories"]["archieves"], mask), settings["directories"]["buffer"])
		os.system(f'mv ./{settings["directories"]["buffer"]}/SWIRL2CO2 ./{settings["directories"]["buffer"]}/{mask}')

		print(f"[{year}-{month_mask}] done!")
		if year == year_to and month == month_to:
			break

		month += 1

def cmd_upload(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	year = year_from
	month = month_from
	
	while True:
		if month > 12:
			year += 1
			month = 1
		month_mask = ""
		if month < 10 and month > 0:
			month_mask = "0" + str(month)
		else:
			month_mask = str(month)
		mask = "SWIRL2CO2_{}{}_{}".format(str(year), month_mask, version)

		path = "{}/{}/{}/".format(os.getcwd(), settings["directories"]["buffer"], mask)
		if not os.path.isdir(path):
			if year == year_to and month == month_to:
				break
		else:
			month_data = []
			for f in sorted(os.listdir(path)):
				if f == ".directory":
					continue
				print(f"file = {f}")
				datafile = h5py.File(path + f, 'r')

				data = read_data(datafile)
				l = len(data)
				print(f"year = {year}, month = {month_mask}, size = {l}")
				month_data.append(data)
				
				datafile.close()
			path = "{}/{}/".format(os.getcwd(), settings["directories"]["json"])
			if not os.path.isdir(path):
				os.system(f"mkdir {path}")
			load_into_file(path, "{}{}_{}.txt".format(str(year), month_mask, version), month_data)
		
		print(f"\n\n[{year}-{month_mask}] done!")
		if year == year_to and month == month_to:
			break

		month += 1

def cmd_insert(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	os.system("g++ -o db db.cpp `mariadb_config --cflags --libs`")
	os.system(f"./db {year_from} {month_from} {year_to} {month_to} {version}")

def run():
	print("Input \"help\" command to get list of all commands.")

	while True:
		cmd = str(input("-->> "))
		if cmd == "help":
			print("download - download archieves from the site")
			print("unpack - unpack downloaded archieves")
			print("tofile - read h5 file and convert to json")
			print("insert - insert data to database")
		elif cmd == "download":
			print("Input period: year_from, month_from, year_to, month_to, version")
			line = str(input()).split()
			cmd_download(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])
		elif cmd == "unpack":
			print("Input period: year_from, month_from, year_to, month_to, version")
			line = str(input()).split()
			cmd_unpack(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])
		elif cmd == "tofile":
			print("Input period: year_from, month_from, year_to, month_to, version")
			line = str(input()).split()
			cmd_upload(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])
		elif cmd == "insert":
			print("Input period: year_from, month_from, year_to, month_to, version")
			line = str(input()).split()
			cmd_insert(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])
		elif cmd == "quit" or cmd == "q":
			break
		else:
			print("Unknown command!")

with open("db_terminal_settings.json", 'r') as file:
	settings = json.load(file)

run()

# index = 0
# for url in settings["urls"]:
# 	download_archieve(url, settings["user"], settings["password"], settings["directories"]["archieves"])
	
	# r = requests.get(url, allow_redirects=True)
	# lines = url.split("/")
	# open(f'{settings["directories"]["archieves"]}/{lines[len(lines) - 1]}.txt', "wb").write(r.content)
	# index += 1
