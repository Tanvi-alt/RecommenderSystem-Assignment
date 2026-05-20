import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# ==========================================
# LOAD MOVIES DATA
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

movies_path = os.path.join(
    BASE_DIR,
    "models",
    "processed_movies.csv"
)

movies = pd.read_csv(movies_path)

# ==========================================
# HANDLE NULL VALUES
# ==========================================

movies['genres'] = movies['genres'].fillna('')

# ==========================================
# TF-IDF VECTORIZATION
# ==========================================

cosine_sim = pickle.load(
    open(
        os.path.join(
            BASE_DIR,
            "models",
            "similarity.pkl"
        ),
        "rb"
    )
)

# ==========================================
# INDEX MAPPING
# ==========================================

indices = pd.Series(
    movies.index,
    index=movies['title']
).drop_duplicates()

# ==========================================
# RECOMMENDATION FUNCTION
# ==========================================

def recommend_movies(title):

    if title not in indices:
        return ["Movie Not Found"]

    idx = indices[title]

    similarity_scores = list(
        enumerate(cosine_sim[idx])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[1:11]

    movie_indices = [
        i[0]
        for i in similarity_scores
    ]

    recommendations = movies.iloc[
        movie_indices
    ]['title'].tolist()

    return recommendations