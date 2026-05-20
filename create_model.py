import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# LOAD DATASET
# ==========================================

movies = pd.read_csv('models/processed_movies.csv')

# ==========================================
# KEEP REQUIRED COLUMNS
# ==========================================

movies = movies[['title', 'genres']]

# Remove null values
movies.dropna(inplace=True)

# ==========================================
# CONVERT GENRES TO VECTORS
# ==========================================

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(
    movies['genres']
).toarray()

# ==========================================
# CALCULATE SIMILARITY
# ==========================================

similarity = cosine_similarity(vectors)

# ==========================================
# SAVE movie_dict.pkl
# ==========================================

pickle.dump(
    movies.to_dict(),
    open('models/movie_dict.pkl', 'wb')
)

# ==========================================
# SAVE similarity.pkl
# ==========================================

pickle.dump(
    similarity,
    open('models/similarity.pkl', 'wb')
)

print("✅ movie_dict.pkl created")
print("✅ similarity.pkl created")
