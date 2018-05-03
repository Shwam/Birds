#!/usr/bin/env python2
import csv, pickle
import os, sys, subprocess
import threading
from Queue import Queue
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import util

def main():
    metadata = util.get_metadata()
    
    # Exctract mel spectrum features
    F = audioFeatureExtraction.dirWavFeatureExtraction("songs", 1.0, 1.0, 0.025, 0.025)
    with open("F", "wb") as f:
        pickle.dump(F, f)

if __name__ == "__main__":
    main()
