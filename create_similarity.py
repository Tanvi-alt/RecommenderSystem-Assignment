import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# LOAD DATA
movies = pd.read_csv(
    'models/processed_movies.csv'
)

movies['genres'] = movies['genres'].fillna('')

# TF-IDF
tfidf = TfidfVectorizer(
    stop_words='english'
)

tfidf_matrix = tfidf.fit_transform(
    movies['genres']
)

# COSINE SIMILARITY
cosine_sim = cosine_similarity(
    tfidf_matrix,
    tfidf_matrix
)

# SAVE FILE
pickle.dump(
    cosine_sim,
    open('models/similarity.pkl', 'wb')
)

print("similarity.pkl created successfully")