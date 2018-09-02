# Shared functions for BBC Radio4 in CA project

import datetime as dt
import json

json_dir = 'json/'

def set_date():
# Get current year, month & day // used to define URL to be scraped
# and name resulting JSON file, and to set rec start & end times 

    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)

    return year, month, day

def save_json(schedule_dict, year, month, day):
# Dump schedule dict as a JSON file named with given date (usu today's date)
    global json_dir
    with open(json_dir + year + '-' + month + '-' + day + '.json', 'w') as file:
        json.dump(schedule_dict, file, indent=4, sort_keys=True, separators=(',',': '))

def load_json(year, month, day):
# Load JSON schedule file for given date
    global json_dir
    filename = json_dir + year + '-' + month + '-' + day + '.json'
    with open(filename) as file:
        raw_schedule_dict = json.load(file)
    return raw_schedule_dict

def convert_dict_dates(raw_schedule_dict):
# Convert XSD datestamps in schedule dict to datetime objects
    for key in raw_schedule_dict:
        raw_schedule_dict[key]['START_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['START_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
        raw_schedule_dict[key]['END_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['END_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
    return raw_schedule_dict
    
def execute(command):
# Execute subprocess, returning STDOUT line by line to br printed for debugging
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)
