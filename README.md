# Humphry - BBC Radio 4 synced to local time

A project to create a physical radio that plays BBC Radio 4 time-synced to whichever timezone it's in (so long as it's behind the UK).

Built on a Raspberry Pi, uses [get_iplayer](https://github.com/get-iplayer/get_iplayer) and [omxplayer](https://github.com/popcornmix/omxplayer) to download and play the audio respectively, Python scripts scheduled by cron to grab today's schedule from the BBC website, coordinate download and playback. [Here's the story behind this project](https://medium.com/@phames/humphry-bbc-radio-4-synced-to-us-local-time-11354249042), including hardware instructions.

Note: this is my first Python project! To help others as new to this as me I include below all setup notes in excruciating detail. Please excuse any errors or omissions.

## Setting up your Raspberry Pi

I'm going to assume you're using a new Pi from scratch.

1. On your development machine download the [latest image of Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/). Use [Etcher](https://www.balena.io/etcher/) to burn the image to your SD card.

2. Since you'll be using your Pi "headless" (i.e. without a monitor connected) you'll need it to auto-connect to your wifi on startup, and then you'll log into it remotely from your development machine via SSH. To achieve this, first navigate to the `/boot` directory of the SD card in the terminal of your development machine, then open a new empty file called `wpa_supplicant.conf`:

```
$ nano wpa_supplicant.conf
```

3. Paste in the following, substituting the placeholders for your own wifi network name and password. When you're done press CTRL+X to exit and save in the `/boot` directory.

```
network={
       ssid="YourNetworkSSID"
       psk="Your Network's Passphrase"
       key_mgmt=WPA-PSK
       }

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
```

4. To tell your Pi to allow SSH you need to create an empty file called `ssh` in the top directory of your boot partition. So whilst still in the `/boot` directory enter the following into your terminal.

```
$ touch ssh
```

5. If you look at your /boot folder you should now see `ssh` and `wpa_supplicant.conf` files. Note that these will both disappear after the first time you plug in your Pi - they act like one-time configuration instructions, so don't be weirded out.

6. If you're using a Linux development machine, I've found that one extra step is needed to stop SSH hanging. Add the following line to the bottom of both `/etc/ssh/ssh_config` and `/etc/ssh/sshd_config` using nano as sudo: `IPQoS 0x00`

7. Now you're ready to start up your Pi. Insert the SD card into Pi and connect it to power. The red power light should be on, and the green activity light should flash a bit.

8. Give your Pi 15-30 seconds to connect to wifi. Then, with your development machine connected to the same wifi network, ping the Pi from your development machine's terminal to check it's connected. It should return a ping every second or so.

```
$ ping raspberrypi.local
```

8. Stop the pings with CTRL+C. Now you can remotely log in to your Pi via SSH from your development machine. When prompted for a password, the default is *raspberry*.

```
$ ssh pi@raspberrypi.local
```

9. Once logged in immediately change your Pi's password to something secure:

```
$ passwd
```

10. Finally, change the Pi's timezone to match your current location on the Pi's configuration dashboard:

```
$ sudo raspi-config
```

## Installing dependencies
Assuming you installed Raspbian Lite we need to install a bunch of stuff on your Pi.

1. First, whilst logged into your Pi over SSH, install git and create a clone of this git repo:

```
$ sudo apt-get install git
$ git clone https://github.com/misteridiot/humphry.git
```

2. Change directory to `/humphry`, and then create the folders where the audio files, JSON schedule files and logs will be saved:

```
$ cd humphry
$ mkdir audio json logs
```

3. Now install dependencies. Except the requirements file, get_iplayer and omxplayer these are due to weird needs of one module, extruct, so I'll hopefully replace it with something more lightweight in future. I've found the installation of dependencies to be a bit bumpy, with some requiring individual re-installation. Someone smarter than me will no doubt point out why. But some form of the following has always worked eventually.

```
$ sudo apt-get install libxml2-dev libxslt-dev python-dev zlib1g-dev python-pip python3-pip python-lxml python3-lxml omxplayer
$ wget http://packages.hedgerows.org.uk/raspbian/install.sh -O - | sh
$ sudo pip install -r requirements.txt
$ sudo apt-get upgrade
```

## Setting up cron
We want the Pi to automatically download new audio every hour, and for the player script to be running in the background as soon as the Pi boots up. To achieve this we use cron.

1. First you need to change the permissions on the python scripts to allow cron to execute them:

```
$ chmod 755 player.py main.py
```

2. Open your root crontab:

```
$ sudo crontab -e
```

3. At the bottom of the file add the following. Since cron is not context aware you need to tell it where all everything is. Under PYTHONPATH I've included the locations of all my Python packages (don't judge me, I know they're all over the place), you need to edit that to match where yours are (or you know, just try the below). The two cron jobs included run the player script on boot, and the main python script (that cleans up old files and downloads new ones) once an hour. Both processes will send logs to cron.log in your logs folder, using a small shell script to add a timestamp. Once you're done CTRL-X to exit and save.

```
PATH=/usr/sbin:/usr/bin:/sbin:/bin
PYTHONPATH=usr/lib/python2.7:usr/lib/python2.7/plat-arm-linux-gnueabihf:usr/lib/python2.7/lib-tk:/home/pi/.local/lib/python2.7/site-packages

@reboot cd /home/pi/humphry && /home/pi/humphry/player.py 2>&1 | /home/pi/humphry/timestamp.sh >> /home/pi/humphry/logs/cron.log
0 * * * * cd /home/pi/humphry && /home/pi/humphry/main.py  2>&1 | /home/pi/humphry/timestamp.sh >> /home/pi/humphry/logs/cron.log
```

## Setting up hardware
So all that is to get the software running. For the radio to work you'll need your Pi to be connected to two pieces of hardware:

1. **An amp and speaker.** I built my own setup from individual parts but assuming you're using a Pi with a regular 3.5m headphone jack audio output, you can connect any regular powered speaker to it.

2. **A button.** This is to toggle the radio on and off. By default it needs to be connected between GPIO pin 18 and any ground pin (I use one right next to it).

To learn about my personal setup take a look at [this Medium post](https://medium.com/@phames/humphry-bbc-radio-4-synced-to-us-local-time-11354249042).
