import os

def convert(dirname):
    data = []
    for f in os.listdir(dirname):
        with open(dirname + f, 'r') as file:
            for line in file:
                string = line.split()
                data.append(string)
    return data