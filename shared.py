# Shared functions for BBC Radio4 in CA project

import datetime as dt
import json

json_location = '/media/pi/Samsung USB/json/'

def set_date():
# Get current year, month & day // used to define URL to be scraped
# and name resulting JSON file, and to set rec start & end times 

    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)

    return year, month, day

def load_json(year, month, day, json_location):
# Load JSON schedule file for today's date
    filename = json_location + year + '-' + month + '-' + day + '.json'
    with open(filename) as file:
        raw_schedule_dict = json.load(file)
    return raw_schedule_dict

def convert_dict_dates(raw_schedule_dict):
# Convert XSD datestamps in schedule dict to datetime objects
    for key in raw_schedule_dict:
            raw_schedule_dict[key]['START_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['START_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
            raw_schedule_dict[key]['END_TIME'] = dt.datetime.strptime(raw_schedule_dict[key]['END_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
    return raw_schedule_dict
