# Shared functions for humphrey

import datetime as dt
import json
import subprocess
import os
import time
import sys
import logging

def set_date():
# Get current year, month & day // used to define URL to be scraped, name resulting JSON file, and to set rec start & end times
    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)
    logging.debug("Date set")
    return year, month, day

def save_json(schedule_dict, year, month, day, json_dir):
# Dump schedule dict as a JSON file named with given date
    with open(json_dir + year + '-' + month + '-' + day + '.json', 'w') as file:
        json.dump(schedule_dict, file, indent=4, sort_keys=True, separators=(',',': '))
    logging.debug("JSON saved")

def load_json(year, month, day, json_dir):
# Load JSON schedule file for given date
    filename = json_dir + year + '-' + month + '-' + day + '.json'
    with open(filename) as file:
        raw_schedule_dict = json.load(file)
    logging.debug("JSON loaded")
    return raw_schedule_dict

def convert_dict_dates(raw_schedule_dict):
# Convert XSD datestamps in schedule dict to datetime objects
    for key in raw_schedule_dict:
        raw_schedule_dict[key]['START_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['START_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
        raw_schedule_dict[key]['END_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['END_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
    logging.debug("Dates converted")
    return raw_schedule_dict

def execute(command):
# Execute subprocess, returning STDOUT line by line to be printed for debugging
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)

def cleanup(file_dir,delete_hours):
# Delete files within a defined folder that are older than a defined number of hours
    now = time.time()
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir,file)
        if os.path.isfile(file_path) and os.stat(file_path).st_mtime < now - (delete_hours * 60 * 60):
            os.remove(file_path)
            logging.info("File removed: %s", str(file_path))
