#!/usr/bin/env python

# player.py - player module as part of BBC Radio 4 CA project

import subprocess
import datetime as dt
import time
import RPi.GPIO as GPIO
import shared as sh

audio_dir = 'audio/'
json_dir = 'json/'
schedule_dict = {}
switch_pin = 18

def list_programs(schedule_dict):
# FOR DEBUGGING: list all progs in schedule_dict to check correct file is being played
    i = 1
    while i <= len(schedule_dict):
        print(i, schedule_dict[str(i)]['NAME'],schedule_dict[str(i)]['START_TIME'],schedule_dict[str(i)]['PID'])
        i += 1

def find_audio_file(schedule_dict):
# Find the right audio file to play 
    play_file_index = min(schedule_dict, key = time_diff_past_only)
    play_file = schedule_dict[play_file_index]['PID']+'.m4a'
    return play_file_index, play_file

def find_start_time(schedule_dict, play_file_index):
# Find the time at which to start playing the audio file from
    start_time = dt.datetime.today()-schedule_dict[play_file_index]['START_TIME']
    hours, minutes, seconds = convert_timedelta(start_time)
    start_time_str = "%02d" % (hours)+':'+ "%02d" % (minutes)+':'+ "%02d" % (seconds)    
    return start_time_str

def time_diff_past_only(i):
# Key function to return time difference between a past START_TIME and now (future START_TIMEs effectively ignored by maxing them) 
    if schedule_dict[i]['START_TIME']<dt.datetime.today():
        return dt.datetime.today()-schedule_dict[i]['START_TIME']
    else:
        return dt.timedelta.max

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + (seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

def radio_play(play, json_dir, audio_dir):
    global schedule_dict
    if play == False:
#        list_programs(schedule_dict)
        year, month, day = sh.set_date()
        print('Current date set')
        raw_schedule_dict = sh.load_json(year, month, day, json_dir)
        print('JSON imported')
        schedule_dict = sh.convert_dict_dates(raw_schedule_dict)
        print('Dict times converted:' ,len(schedule_dict), 'records')
        play_file_index, play_file = find_audio_file(schedule_dict)
        print('Found file to play:', play_file)
        start_time_str = find_start_time(schedule_dict, play_file_index)
        print('Found start time:', start_time_str)
        popen = subprocess.Popen(['omxplayer', '-o', 'local', audio_dir+play_file, '--pos='+start_time_str], stdout=subprocess.PIPE, universal_newlines=True)
        play = True
        print('Started playing')
        time.sleep(0.25)
        return play
    else:
        subprocess.call(['killall', 'omxplayer.bin'])
        play = False
        print('Stopped playing')
        time.sleep(0.25)
        return play
 
# Main -->
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#radio = Radio()

play = False
# TO DO: If player is always running the below set up will need to happen more frequently - on play stop? Check if there's a JSON file with today's date on play, if not then scraper.py? 

print('Waiting for button press')

while True:
    GPIO.wait_for_edge(switch_pin, GPIO.FALLING)
    play = radio_play(play, json_dir, audio_dir)
