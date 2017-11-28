# Shared functions for BBC Radio4 in CA project

import datetime as dt
import json

def set_date():
# Get current year, month & day // used to define URL to be scraped
# and name resulting JSON file, and to set rec start & end times 

    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)

    return year, month, day

def load_json(year, month, day):
# Load JSON schedule file for today's date
    filename = '/media/pi/Samsung USB/json/' + year + '-' + month + '-' + day + '.json'
    with open(filename) as file:
        raw_schedule_dict = json.load(file)
    return raw_schedule_dict

def convert_dict_dates(raw_schedule_dict):
# Convert XSD datestampts to datetime objects // try condition is due to it being an ordered dict and the loop catching already converted keys
# MAYBE DELETE - not necessary, use index numbers as keys - depends on how the player finds the right file
    for key in raw_schedule_dict:
        try:
            datetime_key = dt.datetime.strptime(key[:19], '%Y-%m-%dT%H:%M:%S')
            raw_schedule_dict[datetime_key] = raw_schedule_dict.pop(key)
        except TypeError:
            pass
    return raw_schedule_dict
