# player.py - WIP player module as part of BBC Radio 4 CA project

# Useful get_iplayer calls
#  get_iplayer --type=radio --channel="Radio 4$" "^Today$" --sort available --listformat="<available> <name> - <pid>"
#  get_iplayer --type=radio --channel="Radio 4$" --pid=b09fj9qp --metadata
#  get_iplayer --type=radio --channel="Radio 4$" --available-since=6 --sort available --listformat="<available> <name> - <pid>" --get
#  sudo amixer cset numid=3 1  //  0=auto, 2=headphones, 3=hdmi

import subprocess
import datetime as dt
import time
import RPi.GPIO as GPIO
import shared as sh

def get_press():
# Detect button press to toggle between play and stop states
    global play
    while True:
        if GPIO.input(switch_pin) == False:
            play = not play
            time.sleep(0.25)
            return play

def list_programs(schedule_dict):
    i = 1
    while i <= len(schedule_dict):
        print(i, schedule_dict[str(i)]['NAME'],schedule_dict[str(i)]['START_TIME'])
        i += 1

def find_program(schedule_dict):
# STUB - find the right program file to play 
# DECIDE HOW TO NAME MEDIA FILES, RETURN THAT NAME - PID & NAME?
# Replace lambda with separate function as key
    play_file_index = min(schedule_dict, key = lambda x: dt.datetime.today()-schedule_dict[x]['START_TIME'] if schedule_dict[x]['START_TIME']<dt.datetime.today() else dt.timedelta.max)
    play_file = schedule_dict[play_file_index]['NAME'] # Replace with media filename
    start_time = dt.datetime.today()-schedule_dict[play_file_index]['START_TIME'] # convert this to hr, min, sec for omxplayer
    return play_file,start_time

def find_play_time(schedule_dict):
# STUB - find offset play time of selected file
    return
               
class Radio:
    def __init__(self):
        pass

    def start(self, play_file, start_time):
        # play_file = '/media/pi/Samsung USB/radio/Drama_Graham_Greene_-_A_Burnt-Out_Case_-_1._Episode_1_b09fxr6b_original.m4a'
        # start_time = '00:10:00'
        # --> self.r = subprocess.Popen(['omxplayer', '-o', 'local', play_file, '--pos='+start_time], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pass
    
    def stop(self):
        # --> subprocess.call(['killall', 'omxplayer.bin'])
        pass
    
    def restart(self):
        self.start()

play = False
GPIO.setmode(GPIO.BCM)
switch_pin = 23
radio = Radio()
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
