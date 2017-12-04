# scraper.py - scraping the BBC R4 schedule to fuel the downloader and player modules of the bbc_r4_ca project

import urllib.request
import datetime as dt
from bs4 import BeautifulSoup
import json

def set_date():
# Get current year, month & day // used to define URL to be scraped and name resulting JSON file 

    year = str(dt.date.today().year)
    month = "{0:0=2d}".format(dt.date.today().month)
    day = "{0:0=2d}".format(dt.date.today().day)

    return year, month, day

def read_html(url):
# Open BBC R4 schedule URL, read into variable

    with urllib.request.urlopen(url) as f:
        html_doc = str(f.read())
    soup = BeautifulSoup(html_doc)
    return soup

def build_schedule_dict(soup):
# Create a schedule dictionary // for each chunk of HTML relating to an individual radio program, find key information & add to the schedule dictionary
# NB Datetimes kept in XSD format, need to be converted to datetime() objects when JSON is read.

    schedule_dict = {}
    i=1

    for parent_tag in soup.find_all(typeof = 'BroadcastEvent'):
        start_time = parent_tag.find(property = 'startDate')['content']
        end_time = parent_tag.find(property = 'endDate')['content']
        pid = str(parent_tag.find(typeof = 'RadioEpisode')['data-pid'])
        prog_name = str(parent_tag.find(class_ = 'programme__title ').string)
        schedule_dict[i] = {'PID': pid, 'NAME': prog_name, 'START_TIME': start_time, 'END_TIME': end_time}
        i=i+1

    return schedule_dict

def save_json(schedule_dict, year, month, day):
# Dump schedule dict as a JSON file named with today's date

    with open('/media/pi/Samsung USB/json/' + year + '-' + month + '-' + day + '.json', 'w') as file:
        json.dump(schedule_dict, file, indent=4, sort_keys=True, separators=(',',': '))

# Main -->
year, month, day = set_date()
url = 'https://www.bbc.co.uk/schedules/p00fzl7j/' + year + '/' + month + '/' + day
print(url)
soup = read_html(url)
print('HTML parsed')
schedule_dict = build_schedule_dict(soup)
print('Dict complete:',len(schedule_dict), 'records')
save_json(schedule_dict, year, month, day)
print('JSON file saved')
