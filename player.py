# player.py - player module as part of BBC Radio 4 CA project

# Useful get_iplayer calls
#  get_iplayer --type=radio --channel="Radio 4$" "^Today$" --sort available --listformat="<available> <name> - <pid>"
#  get_iplayer --type=radio --channel="Radio 4$" --available-since=6 --sort available --listformat="<available> <name> - <pid>" --get
#  sudo amixer cset numid=3 1  //  0=auto, 2=headphones, 3=hdmi

import subprocess
import datetime as dt
import time
import RPi.GPIO as GPIO
import shared as sh

def get_press():
# Detect button press to toggle between play and stop states
# TO DO Find a way of capturing button presses that is more CPU efficient
    global play
    while True:
        if GPIO.input(switch_pin) == False:
            play = not play
            time.sleep(0.25)
            return play

def list_programs(schedule_dict):
# FOR DEBUGGING: list all progs in schedule_dict to check correct file is being played
    i = 1
    while i <= len(schedule_dict):
        print(i, schedule_dict[str(i)]['NAME'],schedule_dict[str(i)]['START_TIME'],schedule_dict[str(i)]['PID'])
        i += 1

def find_program(schedule_dict):
# Find the right program file to play 
    play_file_index = min(schedule_dict, key = past_only_time_diff)
    play_file = schedule_dict[play_file_index]['PID']+'.m4a'
    start_time = dt.datetime.today()-schedule_dict[play_file_index]['START_TIME']
    start_time = format_start_time(start_time)
    return play_file,start_time

def past_only_time_diff(i):
# Key function to return time difference between a past START_TIME and now (future START_TIMEs effectively ignored by maxing them) 
    if schedule_dict[i]['START_TIME']<dt.datetime.today():
        return dt.datetime.today()-schedule_dict[i]['START_TIME']
    else:
        return dt.timedelta.max

def format_start_time(timedelta):
    seconds = timedelta.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    # TO DO move below line to def get_start_time() making this a generic timedelta converter function
    formatted_timedelta = "%02d" % (hours)+':'+ "%02d" % (minutes)+':'+ "%02d" % (seconds)
    return formatted_timedelta
               
class Radio:
    def __init__(self):
        pass

    def start(self, play_file, start_time):
        # play_file = '/media/pi/Samsung USB/radio/Drama_Graham_Greene_-_A_Burnt-Out_Case_-_1._Episode_1_b09fxr6b_original.m4a'
        # start_time = '00:10:00'
        # TO DO Error logging on subprocess, prob add def execute() to shared
        self.r = subprocess.Popen(['omxplayer', '-o', 'local', '/media/pi/Samsung USB/radio/'+play_file, '--pos='+start_time], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pass
    
    def stop(self):
        subprocess.call(['killall', 'omxplayer.bin'])
        # TO DO More elegant way of stopping omxplayer than killall!
        pass
    
# Main -->
GPIO.setmode(GPIO.BCM)
switch_pin = 23
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
radio = Radio()
play = False
year, month, day = sh.set_date()
print('Current date set')
raw_schedule_dict = sh.load_json(year, month, day)
print('JSON imported')
schedule_dict = sh.convert_dict_dates(raw_schedule_dict)
print('Dict times converted:' ,len(schedule_dict), 'records')

while True:
    if get_press() == True:
        list_programs(schedule_dict)
        play_file, start_time = find_program(schedule_dict)
        print('Found file to play:', play_file)
        print('Found start time:', start_time)
        radio.start(play_file, start_time)
        print('Started playing')
    else:
        radio.stop()
        print('Stopped playing')
##
##

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + (seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
