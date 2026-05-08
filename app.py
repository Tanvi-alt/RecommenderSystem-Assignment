import streamlit as st

from recommender import recommend_movies
from recommender import movies

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🎬 Movie Recommendation System")

st.write(
    "Get movie recommendations instantly!"
)

# ==========================================
# MOVIE LIST
# ==========================================

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

# ==========================================
# BUTTON
# ==========================================

if st.button("Recommend"):

    recommendations = recommend_movies(
        selected_movie
    )

    st.subheader("Recommended Movies")

    for movie in recommendations:

        st.write("✅", movie)