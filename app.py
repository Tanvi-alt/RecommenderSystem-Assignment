import streamlit as st
from recommender import recommend_movies, recommend_by_genre, movies

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Advanced Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #0f0f0f, #141414);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #E50914;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #b3b3b3;
    font-size: 20px;
    margin-top: 0;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #E50914, #ff3c4d);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #ff3c4d, #E50914);
}

/* Movie Cards */
.movie-card {
    background: linear-gradient(145deg, #1e1e1e, #252525);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 20px rgba(229,9,20,0.3);
}

.movie-title {
    font-size: 24px;
    font-weight: bold;
    color: white;
}

.movie-desc {
    color: #c7c7c7;
    margin-top: 8px;
}

/* Recommendation Section */
.section-title {
    color: #E50914;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3418/3418886.png",
        width=120
    )

    st.title("🎥 Movie Recommender")

    st.write("""
    Discover movies based on:
    
    ✅ Similar Movies  
    ✅ Genre Selection  
    ✅ Smart ML Recommendations  
    ✅ Beautiful UI Experience
    """)

    st.markdown("---")

    recommendation_type = st.radio(
        "Choose Recommendation Mode",
        [
            "🎬 Similar Movies",
            "🎭 Genre Based"
        ]
    )

    st.markdown("---")

    st.info("Powered by Streamlit + Machine Learning")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1 class='main-title'>
🎬 CineMatch AI
</h1>
<p class='subtitle'>
Find your next favorite movie instantly 🍿
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# SIMILAR MOVIE MODE
# ==========================================

if recommendation_type == "🎬 Similar Movies":

    st.markdown(
        "<p class='section-title'>🔍 Search Similar Movies</p>",
        unsafe_allow_html=True
    )

    movie_list = movies['title'].values

    col1, col2 = st.columns([4, 1])

    with col1:

        selected_movie = st.selectbox(
            "Choose a movie",
            movie_list
        )

    with col2:

        st.write("")
        st.write("")

        recommend_btn = st.button("Recommend")

    if recommend_btn:

        with st.spinner("Finding best recommendations... 🍿"):

            recommendations = recommend_movies(selected_movie)

        st.success(f"Recommendations based on '{selected_movie}'")

        st.markdown(
            "<p class='section-title'>🎯 Recommended Movies</p>",
            unsafe_allow_html=True
        )

        cols = st.columns(3)

        for idx, movie in enumerate(recommendations):

            with cols[idx % 3]:

                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">🎬 {movie}</div>
                    <div class="movie-desc">
                        Perfect match based on your selected movie.
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# GENRE MODE
# ==========================================

else:

    st.markdown(
        "<p class='section-title'>🎭 Genre Based Recommendations</p>",
        unsafe_allow_html=True
    )

    genres = [
        "Action",
        "Comedy",
        "Drama",
        "Romance",
        "Thriller",
        "Horror",
        "Sci-Fi",
        "Adventure",
        "Animation"
    ]

    selected_genre = st.selectbox(
        "Select Genre",
        genres
    )

    genre_btn = st.button("Find Movies")

    if genre_btn:

        with st.spinner("Fetching top movies for you... 🍿"):

            genre_movies = recommend_by_genre(selected_genre)

        st.success(f"Top {selected_genre} Movies")

        st.markdown(
            "<p class='section-title'>🔥 Popular Picks</p>",
            unsafe_allow_html=True
        )

        cols = st.columns(3)

        for idx, movie in enumerate(genre_movies):

            with cols[idx % 3]:

                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">🎥 {movie}</div>
                    <div class="movie-desc">
                        Trending in {selected_genre}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)