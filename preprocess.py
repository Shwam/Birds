#!/usr/bin/env python
import librosa.display, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv, pickle
import os, sys, subprocess
import threading
from queue import Queue
import util
import time

def process(item_id, q, oq):
    filename = "songs/XC{}.mp3".format(item_id, q, oq)

    mfccs = None
    try:
        data, sample_rate = librosa.load(filename)
        # Extract Mel Frequency Cepstral Coefficients
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=40).T, axis=0)
    except Exception as err:
        print("Error parsing {}: {}".format(filename, err))
    q.get()
    oq.put((item_id, mfccs))

def main():
    threads = []
    metadata = util.get_metadata()
    q = Queue(maxsize=7)
    oq = Queue()
    X = []
    for item in metadata[1:]:
        q.put(1)
        time.sleep(0.1)
        t = threading.Thread(target=process, args=(item[0], q, oq))
        t.start()
        threads.append(t)
        print("{}/{}".format(oq.qsize(), len(metadata) - 1), end='\r', flush=True)

    for thread in threads:
        print("{}/{}".format(oq.qsize(), len(metadata) - 1), end='\r', flush=True)
        thread.join()

    features = dict()
    while not oq.empty():
        item_id, feature = oq.get() 
        features[item_id] = feature
    for item in metadata[1:]:
        if item[0] in features and features[item[0]] is not None:
            X.append(features[item[0]])
        else:
            # Note: Items with missing features will need to be removed from metadata.csv to preserve (X,Y) order
            print("Error getting features for {}".format(item[0]))
    with open("features", "wb") as f:
         pickle.dump(X, f)

if __name__ == "__main__":
    main()
