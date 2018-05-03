# Bird Vocalization Classifier
## Requirements
This project uses python3 for most code, with the exception of python2 for Mel spectrum feature extraction. 
The following python3 libraries are required:
- numpy
- scipy
- scikit-learn 
- matplotlib
- librosa

Most of these should be available using `pip install`.

For Mel spectrum feature extraction, the following python2 library is required:
- pyAudioAnalysis

## Web Scraper
The webscraper is a standalone tool which can be used to create datasets from https://xeno-canto.org.

`./scraper/scraper.py <query>` will query the website for a species of bird and gather the metadata for the resulting recordings into the `metadata.csv` file. 

`./scraper/download.py` will attempt to download the audio recording associated with each entry in the metadata and place them in the `./scraper/songs/` directory.

## Feature Extraction
`./preprocess.py` performs feature extraction on the metadata.csv present in the same directory. There should also be a `./songs/` directory in the same location with recordings corresponding to each item in the metadata. The extracted features are pickled and placed in `./features`
`./pyAudioPreprocess` extracts Mel spectrum features us pyAudioAnalysis, and pickles them to `F`.

## Classifier
`./train.py [name]` trains the model on 5 different algorithms and tests them using 5-fold cross-validation. There must be files named `[name]_features` and `[name]_metadata` in the same directory for this to work. If no name is provided, it defaults to using `metadata.csv` and `features`. Currently it always defaults to `F` for the mel spectrum features.

A few datasets are provided for classification:
- `bbs` : The British Bird Song dataset found at https://www.kaggle.com/rtatman/british-birdsong-dataset
- `dataset1` : 6 species of birds, 512 samples, from https://xeno-canto.org
- `dataset2` : A slightly trimmed down version of dataset1; 306 samples


## Clustering
The current clustering method does not tend to provide particularly interesting results, so this section can be mostly ignored.

`./cluster.py [name]` performs hierarchical clustering on each audio recording sample in the dataset and produces a dendrogram. The dendrogram tends to be quite difficult to read for large datasets, so sampling the population is advised.

`./similarity.py [name]` performs hierarchical clustering on the bird species.

