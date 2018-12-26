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

audio_dir = 'audio/'
switch_pin = 18

# def get_press():
# Detect button press to toggle between play and stop states
# TO DO Find a way of capturing button presses that is more CPU efficient
#    global play
#    while True:
#        if GPIO.input(switch_pin) == False:
#            play = not play
#            time.sleep(0.25)
#            return play

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

def radio_play():
    global play
    global audio_dir
    if play == False:
#        list_programs(schedule_dict)
        play_file_index, play_file = find_audio_file(schedule_dict)
        print('Found file to play:', play_file)
        start_time_str = find_start_time(schedule_dict, play_file_index)
        print('Found start time:', start_time_str)
        popen = subprocess.Popen(['omxplayer', '-o', 'hdmi', audio_dir+play_file, '--pos='+start_time_str], stdout=subprocess.PIPE, universal_newlines=True)
#        for path in sh.execute(['omxplayer', '-o', 'hdmi', audio_dir+play_file, '--pos='+start_time_str]):
#            print(path, end="")
#        radio.start(play_file, start_time_str)
        play = True
        print('Started playing')
        time.sleep(0.25)
        return
    else:
#        for path in sh.execute(['killall', 'omxplayer.bin']):
#            print(path, end="")
#        radio.stop()
        subprocess.call(['killall', 'omxplayer.bin'])
        play = False
        print('Stopped playing')
        time.sleep(0.25)
        return
 
# class Radio:
#    def __init__(self):
#        pass

#    def start(self, play_file, start_time_str):
        # play_file = '/media/pi/Samsung USB/radio/Drama_Graham_Greene_-_A_Burnt-Out_Case_-_1._Episode_1_b09fxr6b_original.m4a'
        # start_time = '00:10:00'
        # TO DO Error logging on subprocess, prob add def execute() to shared
#        global audio_dir
#        self.r = subprocess.Popen(['omxplayer', '-o', 'hdmi', audio_dir+play_file, '--pos='+start_time_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        pass
    
#    def stop(self):
#        subprocess.call(['killall', 'omxplayer.bin'])
        # TO DO More elegant way of stopping omxplayer than killall!
#        pass
    
# Main -->
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#radio = Radio()

play = False
# TO DO: If player is always running the below set up will need to happen more frequently - on play stop? Check if there's a JSON file with today's date on play, if not then scraper.py? 
year, month, day = sh.set_date()
print('Current date set')
raw_schedule_dict = sh.load_json(year, month, day)
print('JSON imported')
schedule_dict = sh.convert_dict_dates(raw_schedule_dict)
print('Dict times converted:' ,len(schedule_dict), 'records')
print('Waiting for button press')

while True:
    GPIO.wait_for_edge(switch_pin, GPIO.FALLING)
    radio_play()
