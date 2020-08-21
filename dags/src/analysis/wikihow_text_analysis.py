import os
import random
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer



def clean_dataframe(df):
    nltk.download('punkt')
    nltk.download('stopwords')
    # 0- concat title and description since we use just them 
    df['text'] = df['title'] + df['description']

    # 1. tokenize description and description
    df['text'] = df['text'].apply(word_tokenize)

    # 2- convet upper case to lower case
    df['text'] = df['text'].apply(lambda token: [w.lower() for w in token])

    # 3- remove punctuation
    table = str.maketrans('','', string.punctuation)
    df['text'] = df['text'].apply(lambda token: [w.translate(table) for w in token])

    # 4- remian just alphabet tockens
    df['text'] = df['text'].apply(lambda token: [w for w in token if w.isalpha()])

    # 5- remove stop words
    stop_words = set(stopwords.words('english'))
    stop_words.update({'make', 'steps', 'step', 'easy', 'ways', 'way', 'wikihow', 'also'})
    df['text'] = df['text'].apply(lambda token: [w for w in token if not w in stop_words]) 

    # 6- Normalize text 
    porter = PorterStemmer()
    df['text'] = df['text'].apply(lambda token: [porter.stem(w) for w in token])

def get_top_n_features(df, n=30):
    # TFidf identifier
    tfidf = TfidfVectorizer()
    df['text'] = df['text'].apply(lambda token: " ".join(token))
    features_vector = tfidf.fit_transform(df['text'])
    
    feature_array = np.array(tfidf.get_feature_names())
    tfidf_sorting = np.argsort(features_vector.toarray()).flatten()[::-1]

    return feature_array[tfidf_sorting][:n].tolist()


def analyze_posts(ds, processed_data_path, **kwrgs):
    data_path = os.path.join(*[processed_data_path,
         ds,
        "wikihow_trends.csv"])
    # read csv file that should be analyzed
    df = pd.read_csv(data_path, index_col=0)

    clean_dataframe(df)
    print(get_top_n_features(df))
    return True

def save_to_database():
    return True