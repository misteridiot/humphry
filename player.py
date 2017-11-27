#bbc_ca.py - BBC Radio 4 in CA

# Useful get_iplayer calls
#  get_iplayer --type=radio --channel="Radio 4$" "^Today$" --sort available --listformat="<available> <name> - <pid>"
#  get_iplayer --type=radio --channel="Radio 4$" --pid=b09fj9qp --metadata
#  get_iplayer --type=radio --channel="Radio 4$" --available-since=6 --sort available --listformat="<available> <name> - <pid>" --get
#  sudo amixer cset numid=3 1  //  0=auto, 2=headphones, 3=hdmi

import json
import subprocess
import datetime as dt
import time
import RPi.GPIO as GPIO

def set_date():
# Get current year, month & day // used to define JSON file to be loaded 
    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)
    return year, month, day

def set_json_filename(year, month, day):
# Define which JSON filename to read using today's date
    filename = '/media/pi/Samsung USB/json/' + year + '-' + month + '-' + day + '.json'
    return filename

def load_json(filename):
# Load JSON schedule file & convert XSD format keys to datetime() objects
    schedule_dict = json.loads(filename)
    for key in schedule_dict:
        schedule_dict[convert_xsd(key)] = schedule_dict.pop(key)
    return schedule_dict

def convert_xsd(xsd):
# Convert xsdDateTime string minus sub-second units into datetime() object
    xsd = xsd[:-6]
    date_time = dt.datetime.strptime(xsd, '%Y-%m-%dT%H:%M:%S')
    return date_time

def find_program(schedule_dict):
# DECIDE HOW TO NAME MEDIA FILES, RETURN THAT NAME - PID & NAME?
    prog = min(schedule_dict, key=lambda d: abs(d - dt.datetime.today())

def find_play_time(schedule_dict):
    

def get_press():
    global play
    while True:
        if GPIO.input(switch_pin) == False:
            play = not play
            time.sleep(0.25)
            return play

class Radio:
    def __init__(self):
        pass

    def start(self, play_file, start_time):
        # play_file = '/media/pi/Samsung USB/radio/Drama_Graham_Greene_-_A_Burnt-Out_Case_-_1._Episode_1_b09fxr6b_original.m4a'
        # start_time = '00:10:00'
        self.r = subprocess.Popen(['omxplayer', '-o', 'local', play_file, '--pos='+start_time], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('Started')
        
    def stop(self):
        subprocess.call(['killall', 'omxplayer.bin'])
        print('Stopped')

    def restart(self):
        self.start()

play = False
GPIO.setmode(GPIO.BCM)
switch_pin = 23
radio = Radio()
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

year, month, day = set_date()
filename = set_json_filename(year, month, day)
schedule_dict = load_json(filename)

while True:
    if get_press() == True:
        play_file = find_program()
        start_time = find_start_time()
        radio.start(play_file, start_time)
    else:
        radio.stop()

##
##

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + (seconds // 3600)
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
