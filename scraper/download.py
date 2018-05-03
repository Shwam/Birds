#!/usr/bin/env python
import re
import subprocess
import sys, os
from html_table_parser import HTMLTableParser
import csv
import threading
from queue import Queue

def download(file_id, q):
    try:
        url = 'https://www.xeno-canto.org/{}/download'.format(file_id[2:]).encode("utf8")
        curl = b"""curl -i -s -k  -X $'GET' \
            -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0' -H $'DNT: 1' -H $'Upgrade-Insecure-Requests: 1' \
            $'""" + url + b"'"

        data = subprocess.check_output(curl, shell=True).decode("utf8")
        redirect = "https:" + re.search(r'(?<=<a href=").*(?=">)', data).group()
        
        curl = b"""curl -i -s -k  -X $'GET' \
            -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0' -H $'DNT: 1' -H $'Upgrade-Insecure-Requests: 1' \
            $'""" + redirect.encode("utf8") + b"'"
        fname = file_id + "." + redirect.split(".")[-1].lower()
        print("Downloading {} as {}".format(redirect, fname))
        data = subprocess.check_output(curl, shell=True)
        with open(os.path.join("songs", fname), "wb") as f:
            f.write(data)
    except Exception as err:
        print(err)
    q.get()

meta = []
with open('metadata.csv', 'r') as f:
    reader = csv.reader(f)
    meta = list(reader)
files = ["XC" + item[0] for item in meta[1:]] 

songs = [song.split(".")[0] for song in os.listdir("songs")]
q = Queue(maxsize=15)
for file_id in files:
    if file_id not in songs:
        print("Downloading {}".format(file_id))
        songs.append(file_id)
        q.put(1)
        t = threading.Thread(target=download, args=(file_id,q))
        t.start()
