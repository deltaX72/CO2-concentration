import json, os

def download_archieve(url: str, http_user: str, http_password: str, output_directory: str):
    os.system(f"wget '{url}' --http-user='{http_user}' --http-passwd='{http_password}' -P '{output_directory}'")

def cmd_download(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	year = year_from
	month = month_from

	while True:
		if month > 12:
			year += 1
			month = 1
		month_mask = ""
		if month < 10 and month > 0:
			month_mask = "0"
		month_mask += str(month)
		
		file_mask = 'SWIRL2CO2/{}/SWIRL2CO2_{}{}_{}.tar'.format(
			str(year), str(year), month_mask, version
		)
		if os.path.exists("{}/{}/{}".format(os.getcwd(), settings["directories"]["archieves"], file_mask)):
			print('Archieve already exists! Skipped')
		else:
			mask = "https://data2.gosat.nies.go.jp/wgetdata/GU/{}".format(file_mask)

			download_archieve(mask, settings["user"], settings["password"], settings["directories"]["archieves"])
			print(f"[{year}-{month_mask}] Done!\n\n")
		if year == year_to and month == month_to:
			break

		month += 1

with open("db_terminal_settings.json", 'r') as file:
	settings = json.load(file)

print("Input period: year_from, month_from, year_to, month_to, version")
line = str(input()).split()
cmd_download(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])

# def funno(file):
# 	try:
# 		with not open(file, 'r'):
# 			print('file yes')
# 	except FileNotFoundError:
# 		print('file no')