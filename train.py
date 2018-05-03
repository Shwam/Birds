#!/usr/bin/env python
import numpy as np
import csv, pickle
import os, sys, subprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import util

def main():
    dataset = None
    if len(sys.argv) > 1:
        dataset = sys.argv[1]
    metadata = util.get_metadata((dataset + "_metadata") if dataset else None)
    
    mfcc = dict(zip([metadata[i][0] for i in range(1, len(metadata))], util.load_features((dataset + "_features") if dataset else None)))
    feats, files = None,None
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
    Y = util.load_labels((dataset + "_metadata") if dataset else None)#"bbsmd.csv")

    for X in [X1, X2] if full_dataset else [X1,]:
        print("------")
       
        classifiers = [ RandomForestClassifier(n_estimators=50, max_features=15, oob_score=True),
            KNeighborsClassifier(3),
            svm.SVC(kernel='linear', C=1),
            svm.SVC(gamma=2, C=1),
            GaussianNB()
        ]
        for clf in classifiers:
            scores = cross_val_score(clf, X, Y, cv=5)
            score = sum(scores)/len(scores)
            print(type(clf).__name__, "\t", score)
        

if __name__ == "__main__":
    main()
