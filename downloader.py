# downloader.py - downloading files for bbc_r4_ca project to play

import sys
import datetime as dt
import shared as sh
import subprocess

audio_dir = 'audio/'

def get_record_times(year, month, day):
# Set recording start & end times, the UK schedule times between which all radio programs will be downloaded, using CLI args
    rec_start_hour = int(sys.argv[1])
    rec_start_min = int(sys.argv[2])
    rec_end_hour = int(sys.argv[3])
    rec_end_min = int(sys.argv[4])
    rec_start_time = dt.datetime(int(year), int(month), int(day), rec_start_hour, rec_start_min, 0, 0)
    rec_end_time = dt.datetime(int(year), int(month), int(day), rec_end_hour, rec_end_min, 0, 0)

    return rec_start_time, rec_end_time

def get_download_list(schedule_dict, rec_start_time, rec_end_time):
# Read PIDs between recording start & end times, add to download_list
    download_list = []
    for key in schedule_dict:
        start_time = schedule_dict[key]['START_TIME']
        end_time = schedule_dict[key]['END_TIME']
        if (start_time <= rec_start_time and end_time > rec_start_time) or (start_time > rec_start_time and start_time < rec_end_time):
            download_list.append(schedule_dict[key]['PID'])
            print(start_time, end_time, schedule_dict[key]['NAME'], schedule_dict[key]['PID'])
    print(len(download_list), 'programs to download:', download_list)
    return download_list

def init_download(download_list, audio_dir):
# Tell get_iplayer to record PIDs
    download_str = ','.join(download_list)
    for path in sh.execute(['get_iplayer', '--type=radio', '--pid='+download_str, '--file-prefix=<pid>', '--radiomode=good', '--output='+audio_dir, '--force', '--overwrite']):
        print(path, end="")
    # TO DO: Add error/output logging
    return

# Main -->
year, month, day = sh.set_date()
print('Current date set')
rec_start_time, rec_end_time = get_record_times(year, month, day)
print('Got record times')
raw_schedule_dict = sh.load_json(year, month, day)
print('JSON imported')
schedule_dict = sh.convert_dict_dates(raw_schedule_dict)
print('Dict times converted:' ,len(schedule_dict), 'records')
download_list = get_download_list(schedule_dict, rec_start_time, rec_end_time)
print('Download list compiled')
init_download(download_list, audio_dir)
print('Downloads completed')
# Check success of downloads?
