#!/usr/bin/env python

import scraper
import downloader
import shared as sh
import datetime as dt

audio_dir = 'audio/'
json_dir = 'json/'
hours_ahead = 4

scraper.scraper(json_dir)
print("MAIN: SCRAPER COMPLETE")
sh.cleanup(audio_dir,12)
print("MAIN: AUDIO CLEANUP COMPLETE")
sh.cleanup(json_dir,48)
print("MAIN: JSON CLEANUP COMPLETE")
downloader.downloader(hours_ahead, audio_dir,json_dir)
print("MAIN: DOWNLOADER COMPLETE")
