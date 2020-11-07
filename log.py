import os
from datetime import datetime

PATH_TO_LOG_FILE = os.getcwd() + "/log.txt"

def log(message):
    with open(PATH_TO_LOG_FILE, 'a') as file:
        file.write(
        	'[{} {}]: {}\n'.format(
            datetime.date(datetime.now()), datetime.time(datetime.now()), message
        ))