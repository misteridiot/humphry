#!/usr/bin/env python

import scraper
import downloader
import shared as sh
import datetime as dt
import logging

audio_dir = 'audio/'
json_dir = 'json/'
hours_ahead = 4

logging.basicConfig(filename='logging_test.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

scraper.scraper(json_dir)
logging.info("Scraper complete")
sh.cleanup(audio_dir,12)
print("MAIN: AUDIO CLEANUP COMPLETE")
sh.cleanup(json_dir,48)
print("MAIN: JSON CLEANUP COMPLETE")
downloader.downloader(hours_ahead, audio_dir,json_dir)
print("MAIN: DOWNLOADER COMPLETE")
