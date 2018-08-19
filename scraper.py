# scraper.py - scraping the BBC R4 schedule to fuel the downloader and player modules of the bbc_r4_ca project

import urllib.request
import datetime as dt
from bs4 import BeautifulSoup
import json
import shared as sh

def read_html(url):
# Open BBC R4 schedule URL, read into variable

    with urllib.request.urlopen(url) as f:
        html_doc = str(f.read())
    soup = BeautifulSoup(html_doc)
    print (soup)
    return soup

def build_schedule_dict(soup):
# Create a schedule dictionary // for each chunk of HTML relating to an individual radio program, find key information & add to the schedule dictionary
# NB Datetimes kept in XSD format, will be converted to datetime() objects when JSON is read.

    schedule_dict = {}
    i=1

    for parent_tag in soup.find_all(typeof = 'BroadcastEvent'):
        start_time = parent_tag.find(property = 'startDate')['content']
        end_time = parent_tag.find(property = 'endDate')['content']
        pid = str(parent_tag.find(typeof = 'RadioEpisode')['data-pid'])
        prog_name = str(parent_tag.find(class_ = 'programme__title ').string)
        schedule_dict[i] = {'PID': pid, 'NAME': prog_name, 'START_TIME': start_time, 'END_TIME': end_time}
        i=i+1
    print (schedule_dict)
    return schedule_dict

# Main -->
year, month, day = sh.set_date()
url = 'https://www.bbc.co.uk/schedules/p00fzl7j/' + year + '/' + month + '/' + day
print(url)
soup = read_html(url)
print('HTML parsed')
schedule_dict = build_schedule_dict(soup)
print('Dict complete:',len(schedule_dict), 'records')
sh.save_json(schedule_dict, year, month, day)
print('JSON file saved')
