#!/usr/bin/env python
import pandas as pd
import numpy as np
import csv, pickle
import os, sys, subprocess
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans, dbscan
from sklearn.ensemble import RandomForestClassifier
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import matplotlib
import matplotlib.pyplot as plt
import util
import random

def main():
    dataset = None
    if len(sys.argv) > 1:
        dataset = sys.argv[1]
    metadata = util.get_metadata((dataset + "_metadata") if dataset else None)
    
    mfcc = dict(zip([metadata[i][0] for i in range(1, len(metadata))], util.load_features((dataset + "_features") if dataset else None)))

    # Load pyAudioAnalysis features
    with open("F", "rb") as f:
        feats, files = pickle.load(f, encoding="latin1")
    files = [f.split(".")[0].split("XC")[-1] for f in files]
    F = dict(zip(files, feats))
    full_dataset = True
    for item in metadata[1:]:
        if item[0] not in F:
            full_dataset = False
    X2, X3 = [], []
    if full_dataset:
        X3 = [np.concatenate((F[item[0]], mfcc[item[0]]), axis=0) for item in metadata[1:]]
        X2 = [F[item[0]] for item in metadata[1:]]
    X1 = [mfcc[item[0]] for item in metadata[1:]]

    for X in [X1, X2]:
        NUM_RUNS = 50
        Y = util.load_labels((dataset + "_metadata") if dataset else None)
        samples = range(len(X))#range(1, len(X), 12)#random.sample(range(len(X)), 25)
        samps = samples#range(len(X))#samples 
        x = [X[i] for i in samps]
        y = [Y[i] for i in samples]
        N_ESTIMATORS = 20
        avg_mat = None 

        for run in range(NUM_RUNS): 
            clf = RandomForestClassifier(n_estimators=N_ESTIMATORS, max_features=20, oob_score=True).fit(X, Y)
            similarity = dict()
            for dt in clf.estimators_:
                leaves = dt.apply(X)
                for i in samps:
                    for j in samps:
                        if leaves[i] == leaves[j]:
                            similarity[(i,j)] = similarity.get((i,j), 0) + 1

            mat = np.array([[(1.0 - similarity.get((i,j), 0)/N_ESTIMATORS)**2 for j in samples] for i in samples])
            mat = squareform(mat)
            if avg_mat is None:
                avg_mat = mat
            else:
                avg_mat = np.add(avg_mat, mat)  
        avg_mat = avg_mat / NUM_RUNS
        linkage_matrix = linkage(avg_mat, "single")
        matplotlib.rcParams['lines.linewidth'] = 2.5
        dendrogram(linkage_matrix, color_threshold=0.8, labels=y, show_leaf_counts=True)
        plt.xlabel("label")
        plt.ylabel("distance")
        plt.show()

if __name__ == "__main__":
    main()
