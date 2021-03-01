import os, json

def unpack(path_to_archieve: str, output_directory: str):
    os.system(f"tar -xf '{path_to_archieve}' -C '{output_directory}'")

def unpack_archieve(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
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
		dir_mask = "SWIRL2CO2_{}{}_{}".format(str(year), month_mask, version)
		arch_path = "{}/{}/{}.tar".format(os.getcwd(), settings["directories"]["archieves"], dir_mask)

		if os.path.exists(arch_path):
			print("{}/{}/{}".format(os.getcwd(), settings["directories"]["buffer"], dir_mask))
			if os.path.exists("{}/{}/{}".format(os.getcwd(), settings["directories"]["buffer"], dir_mask)):
				print(f'[{year}-{month_mask}] Unpacked archieve already exists! Skipped')
			else:
				unpack(arch_path, settings["directories"]["buffer"])
				# handle mv message
				os.system(f'mv {os.getcwd()}/{settings["directories"]["buffer"]}/SWIRL2CO2 {os.getcwd()}/{settings["directories"]["buffer"]}/{dir_mask}')

				print(f"[{year}-{month_mask}] Done!")
		if year == year_to and month == month_to:
			break

		month += 1

with open("db_terminal_settings.json", 'r') as file:
	settings = json.load(file)

print("Input period: year_from, month_from, year_to, month_to, version")
line = str(input()).split()
unpack_archieve(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])

# а Cock вы меня уBilly