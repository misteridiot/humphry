#!/usr/bin/env python

import scraper
import downloader
import shared as sh
import datetime as dt
import logging

audio_dir = 'audio/'
json_dir = 'json/'
download_hours_ahead = 4
audio_hours_retain = 12
json_hours_retain = 48
logging.basicConfig(filename='logging_test.log', format='%(asctime)s %(levelname)s-%(module)s-%(funcName)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def main(audio_dir, json_dir, download_hours_ahead, audio_hours_retain, json_hours_retain):
    scraper.scraper(json_dir)
    logging.info("Scraper complete")
    sh.cleanup(audio_dir, audio_hours_retain)
    logging.info("Audio cleanup complete")
    sh.cleanup(json_dir, json_hours_retain)
    logging.info("JSON cleanup complete")
    downloader.downloader(download_hours_ahead, audio_dir, json_dir)
    logging.info("Downloader complete")

# Main -->
main(audio_dir, json_dir, download_hours_ahead, audio_hours_retain, json_hours_retain)
