#!/usr/bin/env python
import os
import csv
import urllib.parse
import subprocess
"""import scrape"""

meta = []

curl = b"""curl -i -s -k  -X $'GET' \
    -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0' -H $'DNT: 1' -H $'Upgrade-Insecure-Requests: 1' \
    $'https://www.xeno-canto.org/explore?query='"""

with open('metadata.csv', 'r') as f:
    reader = csv.reader(f)
    meta = list(reader)
files = ["XC" + item[0] for item in meta[1:]] 

songs = [song.split(".")[0] for song in os.listdir("songs")]

species = dict()
for item in meta[1:]:
    if "XC" + item[0] not in songs:
        continue
    #species[item[1] + " " + item[2]] = species.get(item[1] + " " + item[2], 0) + 1
    species[item[3]] = species.get(item[3], 0) + 1

def get_more(spec):
    try:
        data = subprocess.check_output(curl + urllib.parse.quote_plus(spec).encode("utf8"), shell=True).decode("utf8")
        scrape.scrape(data)
    except Exception as err:
        pass
"""for spec in species:
    if species[spec] < 3:
        print(spec, species[spec])
        get_more(spec)"""

#downloader.__main__()     

with open('metadata.csv', 'r') as f:
    reader = csv.reader(f)
    meta = list(reader)

removals = []
for item in meta[1:]:
    if "call" not in item[8].lower():#species.get(item[3], 0) < 3 or "?" in item[3]:
        removals.append(item[0])

with open('metadata.csv', 'w') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    for item in meta:
        if item[0] not in removals:
            wr.writerow(item)
