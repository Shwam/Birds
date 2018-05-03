#!/usr/bin/env python
import os, sys
import csv
import urllib.parse
import subprocess
import re
from html_table_parser import HTMLTableParser

meta = []
files = set()

headers = "file_id","genus","species","common","who_provided_recording","country","location","remarks","type"

curl = b"""curl -i -s -k  -X $'GET' \
    -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0' -H $'DNT: 1' -H $'Upgrade-Insecure-Requests: 1' \
    $'https://www.xeno-canto.org/explore"""

def get_name(name):
    common, scientific = name.split("(")
    common = common.strip()
    scientific = scientific[:-1].strip().split(" ")
    genus, species = scientific[0], scientific[1]
    return genus, species, commmon

def scrape(data):
    # Get the tables
    p = HTMLTableParser()
    html_table = re.search(r'<table class="results">(.|\n)*</table>', data).group(0)
    p.feed(html_table)
    table = p.tables[0]
    print("found {} items".format(len(table)))


    with open('metadata.csv', 'a') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for item in table[1:]:
            file_id = item[-1][2:]
            if file_id in files or "?" in item[1]:
                continue
            files.add(file_id)
            genus, species, common = get_name(item[1])
            wr.writerow( (file_id,genus,species,common,item[3], item[6], item[7], item[10], item[9]) )

if __name__ == "__main__":
    meta = []
    if os.path.exists('metadata.csv'):
        with open('metadata.csv', 'r') as f:
            reader = csv.reader(f)
            meta = list(reader)
        files = set(i[0] for i in meta)
    else:
        with open('metadata.csv', 'w') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(headers)

    if len(sys.argv) > 1:
        for page in range(1, 4):
            query = " ".join(sys.argv[1:])
            request = curl + b"?query=" + urllib.parse.quote_plus(query).encode("utf8") + b"&pg=" + str(page).encode("utf8") + b"'"
            print(request)
            data = subprocess.check_output(request, shell=True).decode("utf8")
            scrape(data)
