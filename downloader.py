# downloader.py - downloading files for bbc_r4_ca project to play

import json
import datetime as dt

def set_date():
# Get current year, month & day // used to define URL to be scraped and name resulting JSON file 
# Repeated in bbc_scraper - need to abstract & import

    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)

    return year, month, day

def get_record_times(year, month, day):
# Parse arguments from CLI cron call, for now hard code
    rec_start_time = dt.datetime(int(year), int(month), int(day), 5, 30, 0, 0)
    rec_end_time = dt.datetime(int(year), int(month), int(day), 10, 0, 0, 0)

    return rec_start_time, rec_end_time

def load_json(year, month, day):
# Load JSON schedule file for today's date
    filename = '/media/pi/Samsung USB/json/' + year + '-' + month + '-' + day + '.json'
    with open(filename) as file:
        raw_schedule_dict = json.load(file)
    return raw_schedule_dict

def convert_dict_dates(raw_schedule_dict):
# Convert XSD datestampts to datetime objects // try condition is due to it being an ordered dict and the loop catching already converted keys
# DELETE - not necessary, use index numbers as keys
    for key in raw_schedule_dict:
        try:
            datetime_key = dt.datetime.strptime(key[:19], '%Y-%m-%dT%H:%M:%S')
            raw_schedule_dict[datetime_key] = raw_schedule_dict.pop(key)
        except TypeError:
            pass
    return raw_schedule_dict

def get_download_list(schedule_dict, rec_start_time, rec_end_time):
# STUB - read PIDs between rec start & end times
    download_list = []
    for key in schedule_dict:
        start_time = dt.datetime.strptime(schedule_dict[key]['START_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
        end_time = dt.datetime.strptime(schedule_dict[key]['END_TIME'][:19], '%Y-%m-%dT%H:%M:%S')
        if (start_time <= rec_start_time and end_time > rec_start_time) or (start_time > rec_start_time and start_time < rec_end_time):
            download_list.append(schedule_dict[key]['PID'])
            print(start_time, end_time, schedule_dict[key]['NAME'], schedule_dict[key]['PID'])
    print(len(download_list))
    print(download_list)
    return download_list

def init_download(download_list):
# STUB - tell get_iplayer to record PIDs
    return

year, month, day = set_date()
print('Current date set')
rec_start_time, rec_end_time = get_record_times(year, month, day)
print('Got record times')
raw_schedule_dict = load_json(year, month, day)
print('JSON imported')
schedule_dict = convert_dict_dates(raw_schedule_dict)
print('Dict times converted:' ,len(schedule_dict), 'records')
download_list = get_download_list(schedule_dict, rec_start_time, rec_end_time)
print('Download list compiled')
init_download(download_list)
print('Downloads started')
# Check success of downloads?
