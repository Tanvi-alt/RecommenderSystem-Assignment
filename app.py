import streamlit as st
from recommender import recommend_movies, movies

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton>button {
    width: 100%;
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #ff1e2d;
    color: white;
}

.movie-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.02);
    background-color: #262730;
}

.big-font {
    font-size: 22px !important;
    font-weight: bold;
    color: #ffffff;
}

.small-font {
    color: #b3b3b3;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎥 About")

    st.write("""
    This Movie Recommendation System suggests movies 
    similar to your selected movie using Machine Learning.
    """)

    st.markdown("---")

    st.subheader("⚡ Features")

    st.write("""
    ✅ Smart Recommendations  
    ✅ Fast Search  
    ✅ Modern UI  
    ✅ Interactive Layout  
    """)

    st.markdown("---")

    st.info("Built using Streamlit + ML")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1 style='text-align: center; color: #E50914;'>
🎬 Movie Recommendation System
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; font-size:18px;'>
Discover movies you'll love instantly 🍿
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# SEARCH SECTION
# ==========================================

movie_list = movies['title'].values

col1, col2 = st.columns([4, 1])

with col1:

    selected_movie = st.selectbox(
        "🔍 Search or Select a Movie",
        movie_list
    )

with col2:

    st.write("")
    st.write("")

    recommend_btn = st.button("Recommend")

# ==========================================
# RECOMMENDATION SECTION
# ==========================================

if recommend_btn:

    with st.spinner("Finding best recommendations for you... 🍿"):

        recommendations = recommend_movies(selected_movie)

    st.success(f"Top recommendations based on '{selected_movie}'")

    st.markdown("## 🎯 Recommended Movies")

    cols = st.columns(3)

    for idx, movie in enumerate(recommendations):

        with cols[idx % 3]:

            st.markdown(f"""
            <div class="movie-card">
                <p class="big-font">🎬 {movie}</p>
                <p class="small-font">
                    Similar taste match for you
                </p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<p style='text-align: center; color: gray;'>
Made with ❤️ using Streamlit
</p>
""", unsafe_allow_html=True)