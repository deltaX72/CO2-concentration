import os, json, h5py

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

def convert_to_file(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
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
			print('Loaded!!!!!=============>>>>>>>>>>>>>>>>>>>>>>>>')
		
		print(f"\n\n[{year}-{month_mask}] done!")
		if year == year_to and month == month_to:
			break

		month += 1

def load_into_file(path: str, filename: str, data: list):
    with open(path + filename, 'w') as file:
        for i in data:
            for d in i:
                line = "{} {} {} {} {}\n".format(d["date"], d["time"], d["lat"], d["lon"], d["con"])
                file.write(line)

with open("db_terminal_settings.json", 'r') as file:
	settings = json.load(file)

print("Input period: year_from, month_from, year_to, month_to, version")
line = str(input()).split()
convert_to_file(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])