# Humphry - BBC Radio 4 synced to local time

A project to create a physical radio that plays BBC Radio 4 time-synched to whichever timezone it's in (so long as it's behind the UK).

Built on a Raspberry Pi, uses get_iplayer and omxplayer to download and play the audio respectively, Python scripts scheduled by cron to grab today's schedule and coordinate download and playback.

Note: a first project by a newbie! To help other as new to this as me I include below all setup notes in excruciating detail. I'm assuming you're using a new Pi from scratch.

## Setting up your Raspberry Pi

1. On your development machine download the [latest image of Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/). Use [Etcher](https://www.balena.io/etcher/) to burn the image to your SD card.
2. Since you'll be using your Pi "headless" (i.e. without a monitor connected) you'll need it to auto-connect to your wifi on startup, and then you'll log into it remotely from your development machine via SSH. So in the terminal of your development machine navigate to the /root directory of the SD card, then open the wpa_supplicant.conf file as sudo:
> sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

3. Add your wifi network details to the file (note you can add multiple networks):
>        network={
>               ssid="YourNetworkSSID"
>               psk="Your Network's Passphrase"
>               key_mgmt=WPA-PSK
>        }

Then exit and save by pressing CTRL+X.

4. I've found that SSH hangs unless you add a line to /etc/ssh/ssh_config and /etc/ssh/sshd_config. So open the first of them as sudo:
> sudo nano /etc/ssh/ssh_config

5. Add the following line to the bottom of the configuration file:
> IPQoS 0x00

Then exit and save by pressing CTRL+X.

6. Repeat steps 4 and 5 above for /etc/ssh/sshd_config
7. To tell your Pi to allow SSH you need to create an empty file called "ssh" in the top directory of your boot partition. So in terminal navigate to the /boot partition and create the file:
> touch ssh

8. Now you're ready to start up your Pi. Insert the SD card into Pi and connect it to power. The red power light should be on, and the green activity light should flash a bit.
9. Give your Pi 30 seconds or so to connect to wifi. Then, with your development machine connected to the same wifi network, ping the Pi to check it's connected:
> ping raspberrypi.local

It should return a ping every second or so. Stop it with CTRL+C.
10. Now you can remotely log in to your Pi via SSH:
> ssh pi@raspberrypi.local

When prompted for a password, the default is _raspberry_

11. Once logged in change it immediately to something secure:
> passwd

12. Finally, change the Pi's timezone to match your current location on the Pi's configuration dashboard:
> raspi-config

## Installing dependencies
Assuming you installed Raspbian Lite we need to install a bunch of stuff on your Pi.

1. First, whilst logged into your Pi over SSH, install git:
> sudo apt-get install git

2. Create a clone of this git repo:
> git clone https://github.com/misteridiot/bbc-radio-timeshift.git

3. Navigate to /bbc-radio-timeshift, and then create the folders where the audio files, JSON schedule files and logs will be saved:
> mkdir audio json logs

4. Now install dependencies. Except the requirements file, get_iplayer and omxplayer these are due to weird needs of one module, extruct, so I'll hopefully replace it with something more lightweight in future:
> sudo apt-get install libxml2-dev libxslt-dev python-dev zlib1g-dev python-pip python-lxml python3-lxml omxplayer
> wget http://packages.hedgerows.org.uk/raspbian/install.sh -O - | sh
> pip install -r requirements.txt

## Setting up cron
We want the Pi to automatically download new audio every hour, and for the player script to be running in the background as soon as the Pi boots up. To achieve this we use cron.
1. First you need to change the permissions on the python scripts to allow cron to execute them:
> chmod 755 player.py main.py cron_test.py

2. Open your root crontab:
> sudo crontab -e

3. At the bottom of the file add the following. Since cron is not context aware you need to tell it where all everything is. Under PYTHONPATH I've included the locations of all my Python packages (don't judge me), you need to edit that to match where yours are (or you know, just try the below). The two cron jobs included run the player script on boot, and the main python script (that cleans up old files and downloads new ones) once an hour. Both processes will send logs to cron.log in your logs folder:
>        PATH=/usr/sbin:/usr/bin:/sbin:/bin
>        PYTHONPATH=usr/lib/python2.7:usr/lib/python2.7/plat-arm-linux-gnueabihf:usr/lib/python2.7/lib-tk:/home/pi/.local/lib/python2.7/site-packages

>        @reboot cd /home/pi/bbc-radio-timeshift && /home/pi/bbc-radio-timeshift/player.py 2>&1 | /home/pi/bbc-radio-timeshift/logs/timestamp.sh >> /home/pi/bbc-radio-timeshift/logs/cron.log
>        0 * * * * cd /home/pi/bbc-radio-timeshift && /home/pi/bbc-radio-timeshift/main.py  2>&1 | /home/pi/bbc-radio-timeshift/logs/timestamp.sh >> /home/pi/bbc-radio-timeshift/logs/cron.log

Once you're done Ctrl-X to exit and save.

# Setting up hardware
So all that is to get the software running. For the radio to work you'll need your Pi to be connected to two pieces of hardware:
1. An amp and speaker. I built my own setup from individual parts but assuming you're using a Pi with a regular 3.5m headphone jack audio output, you can connect any regular powered speaker to it.
2. A button. This is to toggle the radio on and off. By default it needs to be connected between GPIO pin 18 and any ground pin (I use one right next to it).
