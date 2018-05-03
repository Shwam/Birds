import csv, pickle

def get_metadata(fname=None):
    meta = []
    with open(fname or 'metadata.csv', 'r') as f:
        reader = csv.reader(f)
        meta = list(reader)
    return meta

def load_features(fname=None):
    with open(fname or 'features', 'rb') as f:
        X = pickle.load(f)
    return X

def load_labels(fname=None):
    meta = get_metadata(fname)
    return [item[3] for item in meta[1:]]
