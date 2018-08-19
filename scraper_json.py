# scraper.py - scraping the BBC R4 schedule to fuel the downloader and player modules of the bbc_r4_ca project

import requests as req
from pyld import jsonld
import extruct
import pprint
import datetime as dt
from bs4 import BeautifulSoup
import json
import shared as sh

json_dir = 'json/'

def extract_json_ld(url):
# Open BBC R4 schedule URL, read into variable

    pp = pprint.PrettyPrinter(indent=1)
    html_doc = req.get(url)
    json_ld = extruct.extract(html_doc.text, url, syntaxes=['json-ld'])
#    soup = BeautifulSoup(html_doc.text, "html.parser")
#    p = str(soup.find('script', {'type':'application/ld+json'}))
#    json_ld = jsonld.expand(json_ld)
    sched_list = json_ld["json-ld"][0]["@graph"]
    pp.pprint(sched_list)
#    with open(json_dir + year + '-' + month + '-' + day + '.json', 'w') as file:
#        json.dump(dict, file, indent=4, sort_keys=True, separators=(',',': '))
#    print (json_ld)
    return sched_list

def build_schedule_dict(sched_list):
# Create a schedule dictionary // for each chunk of HTML relating to an individual radio program, find key information & add to the schedule dictionary
# NB Datetimes kept in XSD format, will be converted to datetime() objects when JSON is read.

    pp = pprint.PrettyPrinter(indent=1)

    schedule_dict = {}
    i=1

    for item in sched_list:
        pid = item['identifier']
        start_time = item['publication']['startDate']
        end_time = item['publication']['endDate']
        if "partOfSeries" in item:
                prog_name = item["partOfSeries"]['name']
        else:
                prog_name = item['name']                
#        prog_name = "progname"
        schedule_dict[i] = {'PID': pid, 'NAME': prog_name, 'START_TIME': start_time, 'END_TIME': end_time}
        i=i+1
     
#    for parent_tag in soup.find_all(typeof = 'BroadcastEvent'):
#        start_time = parent_tag.find(property = 'startDate')['content']
#        end_time = parent_tag.find(property = 'endDate')['content']
#        pid = str(parent_tag.find(typeof = 'RadioEpisode')['data-pid'])
#        prog_name = str(parent_tag.find(class_ = 'programme__title ').string)
#        schedule_dict[i] = {'PID': pid, 'NAME': prog_name, 'START_TIME': start_time, 'END_TIME': end_time}
#        i=i+1
    pp.pprint (schedule_dict)
    return schedule_dict

# Main -->
year, month, day = sh.set_date()
url = 'https://www.bbc.co.uk/schedules/p00fzl7j/' + year + '/' + month + '/' + day
print(url)
sched_list = extract_json_ld(url)
print('JSON-LD extracted as dict')
schedule_dict = build_schedule_dict(sched_list)
print('Dict complete:',len(schedule_dict), 'records')
sh.save_json(schedule_dict, year, month, day)
print('JSON file saved')
