#!/usr/bin/env python

# downloader.py - downloading files for bbc_r4_ca project to play

import sys
import datetime as dt
import shared as sh
import subprocess
import os
import logging

def get_record_times(year, month, day, hours_ahead):
# Set recording start & end times, the UK schedule times between which all radio programs will be downloaded, using CLI args --> REMOVED GIVEN SETTING TIMES FROM MAIN.PY
#    rec_start_hour = int(sys.argv[1])
#    rec_start_min = int(sys.argv[2])
#    rec_end_hour = int(sys.argv[3])
#    rec_end_min = int(sys.argv[4])
    rec_start_hour = dt.datetime.now().hour
    rec_start_min = dt.datetime.now().minute
    rec_end_hour = rec_start_hour + hours_ahead
    rec_end_min = rec_start_min
    rec_start_time = dt.datetime(int(year), int(month), int(day), rec_start_hour, rec_start_min, 0, 0)
    rec_end_time = dt.datetime(int(year), int(month), int(day), rec_end_hour, rec_end_min, 0, 0)

    return rec_start_time, rec_end_time

def get_download_list(schedule_dict, rec_start_time, rec_end_time, audio_dir):
# Read PIDs between recording start & end times, check if alreday downloaded, if not add to download_list
    download_list = []
    for key in schedule_dict:
        start_time = schedule_dict[key]['START_TIME']
        end_time = schedule_dict[key]['END_TIME']
        pid = schedule_dict[key]['PID']
        if (start_time <= rec_start_time and end_time > rec_start_time) or (start_time > rec_start_time and start_time < rec_end_time):
            file_path = os.path.join(audio_dir,pid+'.m4a')
            print(file_path)
            exists = os.path.isfile(file_path)
            if exists:
                print('File already downloaded:'+pid)
            else:
                download_list.append(pid)
                print('Added to download list: '+schedule_dict[key]['NAME']+' '+pid)
    print(str(len(download_list))+' programs to download:')
    print(download_list)
    return download_list

def init_download(download_list, audio_dir):
# Tell get_iplayer to record PIDs
    download_str = ','.join(download_list)
    for path in sh.execute(['get_iplayer', '--type=radio', '--pid='+download_str, '--file-prefix=<pid>', '--radiomode=good', '--output='+audio_dir, '--force', '--overwrite']):
        print(path)
    # TO DO: Add error/output logging
    return

# Main -->
def downloader(hours_ahead, audio_dir, json_dir):
    year, month, day = sh.set_date()
    logging.debug('Current date set')
#    rec_start_time = dt.datetime(int(year), int(month), int(day), rec_start_hour, rec_start_min, 0, 0)
#    rec_end_time = dt.datetime(int(year), int(month), int(day), rec_end_hour, rec_end_min, 0, 0)
    rec_start_time, rec_end_time = get_record_times(year, month, day, hours_ahead)
    logging.debug('Got record times')
    raw_schedule_dict = sh.load_json(year, month, day,json_dir)
    logging.debug('JSON imported')
    schedule_dict = sh.convert_dict_dates(raw_schedule_dict)
    logging.debug('Dict times converted: %s records',str(len(schedule_dict)))
    download_list = get_download_list(schedule_dict, rec_start_time, rec_end_time, audio_dir)
    logging.debug('Download list compiled')
    init_download(download_list, audio_dir)
    logging.debug('Downloads completed')
    return
# Check success of downloads?
