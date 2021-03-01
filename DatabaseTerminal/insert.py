import os

def insert(year_from: int, month_from: int, year_to: int, month_to: int, version: str):
	os.system("g++ -o db db.cpp `mariadb_config --cflags --libs`")
	os.system(f"./db {year_from} {month_from} {year_to} {month_to} {version}")

print("Input period: year_from, month_from, year_to, month_to, version")
line = str(input()).split()
insert(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])