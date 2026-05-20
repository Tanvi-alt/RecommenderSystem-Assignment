import streamlit as st
import base64
import requests
import re
from recommender import recommend_movies, movies
from utils.auth import signup, login

# Make sure to import the remove_history function!
from utils.database import save_history, get_history, remove_history 

# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# Tracks which movie the user clicked in the sidebar
if "active_base_movie" not in st.session_state:
    st.session_state.active_base_movie = None

# PERSISTENT STORAGE FOR DISCOVER SEARCH TO EMIT REALTIME SIDEBAR UPDATES
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "last_searched_movie" not in st.session_state:
    st.session_state.last_searched_movie = None
if "last_searched_genre" not in st.session_state:
    st.session_state.last_searched_genre = None

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# GLOBAL CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: white;
}

/* Base App Background with Smooth Fade-In Transition */
.stApp {
    background: #070b14;
    min-height: 100vh;
    animation: fadeInPage 0.6s ease-out forwards;
}

@keyframes fadeInPage {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Hide sidebar toggle & default header */
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"]   { background: transparent !important; }

/* ── Sidebar (logged-in only) ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1422 0%, #0a1020 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* Sidebar History Buttons styling */
div[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    color: rgba(255,255,255,0.7) !important;
    text-align: left !important;
    padding: 4px 0 !important;
    font-size: 14px !important;
    box-shadow: none !important;
    justify-content: flex-start !important;
    transition: color 0.2s;
}
div[data-testid="stSidebar"] button[kind="secondary"]:hover {
    color: #e63946 !important;
}

/* ── Inputs ── */
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    transition: border 0.2s, box-shadow 0.2s;
    position: relative;
    z-index: 10;
}
.stTextInput input:focus {
    border-color: #e63946 !important;
    box-shadow: 0 0 0 3px rgba(230,57,70,0.18) !important;
}
.stTextInput label { 
    color: rgba(255,255,255,0.9) !important; 
    font-size: 14px !important; 
    margin-bottom: 4px;
    font-weight: 500;
}

/* ── Selectbox ── */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* ── Tabs Styling ── */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: rgba(255,255,255,0.6) !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: white !important;
    border-bottom: 2px solid #e63946 !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #e63946 0%, #c1121f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 20px rgba(230,57,70,0.35) !important;
    width: 100%;
    position: relative;
    z-index: 10;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(230,57,70,0.55) !important;
}

/* ── PERFECTLY ALIGNED MOVIE CARDS ── */
.movie-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 24px;
    transition: transform 0.25s, background 0.25s, box-shadow 0.25s;
    display: flex;
    flex-direction: column;
    height: 380px; 
}
.movie-card:hover {
    transform: translateY(-4px);
    background: rgba(255,255,255,0.07);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}
.movie-poster {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 14px;
    background: rgba(0,0,0,0.5); 
    border: 1px solid rgba(255,255,255,0.05);
}
.movie-card-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1; 
}
.movie-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
    line-height: 1.3;
}
.movie-card-body {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    line-height: 1.5;
    overflow: hidden;
}

/* Disabled/Enabled Already Watched Button Overrides */
div.stButton > button[key^="watched_"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px dashed rgba(255, 255, 255, 0.1) !important;
    color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: none !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    margin-top: 10px;
}
div.stButton > button[key^="watch_"] {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: rgba(255, 255, 255, 0.8) !important;
    box-shadow: none !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    margin-top: 10px;
}
div.stButton > button[key^="watch_"]:hover {
    background: #e63946 !important;
    color: white !important;
    border-color: #e63946 !important;
    transform: translateY(-1px) !important;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 900;
    color: white;
    text-align: center;
    margin: 48px 0 10px;
}
.section-subheading {
    text-align: center;
    color: rgba(255,255,255,0.5);
    margin-bottom: 30px;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# OMDB API FETCHING FUNCTION
# ==========================================

# ⚠️ PUT YOUR OMDB API KEY HERE ⚠️
OMDB_API_KEY = "3e3d4b7f"

def fetch_movie_details(movie_title):
    clean_title = re.sub(r'\s*\(\d{4}\)', '', movie_title).strip()
    default_poster = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=400&auto=format&fit=crop"
    default_desc = "Matched using AI-powered content similarity and collaborative filtering."
    default_genres = ""

    if OMDB_API_KEY == "PASTE_YOUR_API_KEY_HERE" or OMDB_API_KEY == "YOUR_OMDB_KEY_HERE":
        return default_poster, "⚠️ API Key missing.", default_genres

    try:
        url = f"http://www.omdbapi.com/?t={clean_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url).json()
        
        if response.get("Response") == "True":
            poster_url = response.get("Poster", default_poster)
            if poster_url == "N/A":
                poster_url = default_poster
                
            overview = response.get("Plot", default_desc)
            if overview == "N/A":
                overview = default_desc
            elif len(overview) > 100:
                overview = overview[:97] + "..."
                
            genres = response.get("Genre", default_genres)
            return poster_url, overview, genres
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return default_poster, default_desc, default_genres


# ==========================================
# AUTH PAGE
# ==========================================

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

def render_auth_page():
    video_base64 = get_base64_of_bin_file('background.mp4')
    
    if video_base64:
        st.markdown(f"""
        <style>
            .stApp {{ background: transparent !important; }}
            [data-testid="stAppViewContainer"] {{ background: transparent !important; }}
            [data-testid="stHeader"] {{ background: transparent !important; }}
            #myVideo {{
                position: fixed; top: 50%; left: 50%; min-width: 100%; min-height: 100%;
                width: auto; height: auto; z-index: -10; transform: translateX(-50%) translateY(-50%);
                object-fit: cover; filter: brightness(0.35) contrast(1.2);
            }}
            [data-testid="stTabs"] {{
                background: rgba(12, 20, 34, 0.75); border: 1px solid rgba(255,255,255,0.08);
                border-radius: 28px; padding: 32px 32px 40px 32px;
                box-shadow: 0 32px 80px rgba(0,0,0,0.8); backdrop-filter: blur(10px);
            }}
        </style>
        <video autoplay muted loop playsinline id="myVideo">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 'background.mp4' not found in root folder.")

    st.markdown('<div style="margin-top: 12vh;"></div>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])

    with center_col:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 900; color: white; margin: 0; letter-spacing: -0.5px; text-shadow: 0 4px 20px rgba(0,0,0,0.8);">🎬 CineMatch<span style="color: #e63946;"> AI</span></h2>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            username_in = st.text_input("Username", key="login_user")
            password_in = st.text_input("Password", type="password", key="login_pass")
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", key="login_btn", type="primary"):
                if login(username_in, password_in):
                    st.session_state.logged_in = True
                    st.session_state.username = username_in
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab2:
            new_user = st.text_input("Choose a username", key="signup_user")
            new_pass = st.text_input("Create password", type="password", key="signup_pass")
            st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", key="signup_btn", type="primary"):
                if signup(new_user, new_pass):
                    st.success("Account created! Switch to Sign In.")
                else:
                    st.error("Username already taken.")


# ==========================================
# MAIN APP
# ==========================================

def render_main_app():
    # Fetch latest history at the start of rendering
    history = get_history(st.session_state.username)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 8px 0 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                <div style="width:40px;height:40px;background:linear-gradient(135deg,#e63946,#c1121f);
                    border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;
                    box-shadow:0 4px 14px rgba(230,57,70,0.4);">🎬</div>
                <span style="font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:white;">
                    CineMatch <span style="color:#e63946;">AI</span>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);
            border-radius:16px;padding:18px 16px;text-align:center;margin-bottom:8px;">
            <div style="font-size:32px;margin-bottom:8px;">👤</div>
            <div style="font-size:16px;font-weight:600;color:white;">{st.session_state.username}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.35);margin-top:4px;">CineMatch Explorer</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<p style='color:rgba(255,255,255,0.5);font-size:13px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>Your Watch History</p>", unsafe_allow_html=True)
        
        if not history:
            st.markdown("<p style='color:rgba(255,255,255,0.25);font-size:13px;'>Nothing yet — go explore!</p>", unsafe_allow_html=True)
        else:
            # Scrollable container for history entries
            with st.container(height=350, border=False):
                for idx, movie in enumerate(reversed(history)):
                    col_movie, col_del = st.columns([5, 1])
                    with col_movie:
                        if st.button(f"🎞 {movie}", key=f"hist_btn_{idx}_{movie}", use_container_width=True):
                            st.session_state.active_base_movie = movie
                            st.rerun()
                    with col_del:
                        if st.button("×", key=f"hist_del_{idx}_{movie}", help="Remove movie"):
                            try:
                                remove_history(st.session_state.username, movie)
                                if st.session_state.active_base_movie == movie:
                                    st.session_state.active_base_movie = None
                                # Reset search results if active search is deleted
                                if st.session_state.last_searched_movie == movie:
                                    st.session_state.search_results = None
                                st.rerun()
                            except NameError:
                                st.error("Add 'remove_history' to database.py!")

        st.markdown("---")
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.active_base_movie = None
            st.session_state.search_results = None
            st.rerun()

    # ── Hero Section ──
    st.markdown(f"""
    <div style="
        border-radius: 28px; overflow: hidden; padding: 60px 24px; text-align: center;
        background: linear-gradient(rgba(7,11,20,0.65), rgba(7,11,20,0.85)), url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2050') center/cover;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.06); margin-bottom: 20px;
    ">
        <div style="display: inline-block; background: rgba(230,57,70,0.2); border: 1px solid rgba(230,57,70,0.45); color: #e63946; border-radius: 999px; padding: 5px 16px; font-size: 12px; font-weight: 600; letter-spacing: 1.4px; text-transform: uppercase; margin-bottom: 20px;">✦ Powered by AI</div>
        <div style="font-family: 'Playfair Display', serif; font-size: 58px; font-weight: 900; color: white; line-height: 1.08; letter-spacing: -1px; margin-bottom: 16px; text-shadow: 0 4px 30px rgba(0,0,0,0.5);">Find Your Next<br>Favourite Film</div>
        <div style="font-size: 17px; color: rgba(255,255,255,0.6); max-width: 500px; margin: 0 auto; line-height: 1.7;">
            Welcome back, <strong style="color:white;">{st.session_state.username}</strong> —
            pick a movie you love and we'll surface what to watch next.
        </div>
    </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # SECTION 1: BASED ON WATCH HISTORY
    # ==========================================
    st.markdown("""<div class="section-heading" style="margin-top:40px;">✨ Based on Watch History</div>""", unsafe_allow_html=True)

    if history:
        if st.session_state.active_base_movie and st.session_state.active_base_movie in history:
            target_movie = st.session_state.active_base_movie
        else:
            target_movie = history[-1]
        
        st.markdown(f"""
        <div class="section-subheading">
            Generating matches for: <strong style="color:#e63946; font-size: 18px;">{target_movie}</strong>
            <br><span style="font-size: 12px; opacity: 0.7;">(Click any movie in your sidebar history to change this)</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Curating your personal picks... 🍿"):
            personal_recs = recommend_movies(target_movie)
            
        cols_personal = st.columns(3)
        for idx, movie in enumerate(personal_recs[:3]):
            poster_url, description, movie_genres = fetch_movie_details(movie)
            
            with cols_personal[idx]:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster_url}" class="movie-poster" alt="Movie Poster">
                    <div class="movie-card-content">
                        <div style="font-size:11px;font-weight:600;letter-spacing:1.2px; text-transform:uppercase;color:#e63946;margin-bottom:10px;">
                            ✦ Top Pick
                        </div>
                        <div class="movie-card-title">{movie}</div>
                        <div class="movie-card-body">{description}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Check toggling layout states
                if movie in history:
                    st.button("✅ Already Watched", key=f"watched_personal_{movie}_{idx}", disabled=True)
                else:
                    if st.button("🍿 Mark as Watched", key=f"watch_personal_{movie}_{idx}"):
                        save_history(st.session_state.username, movie)
                        st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 30px; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1); margin-bottom: 40px;">
            <div style="font-size: 24px; margin-bottom: 10px;">🍿</div>
            <div style="color: rgba(255,255,255,0.8); font-weight: 500;">No watch history yet!</div>
            <div style="color: rgba(255,255,255,0.4); font-size: 14px; margin-top: 5px;">Use the search below to log your first movie and unlock personal recommendations here.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Divider ──
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 50px 0;'>", unsafe_allow_html=True)


    # ==========================================
    # SECTION 2: DISCOVER & FILTER
    # ==========================================
    st.markdown("""
    <div class="section-heading" style="margin-top:0px;">%s Discover & Filter</div>
    <div class="section-subheading">
        Pick a base movie and a target genre to filter your recommendations.
    </div>
    """ % "🎭", unsafe_allow_html=True)

    movie_list = movies['title'].values
    genre_options = ["All Genres", "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]

    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        selected_movie = st.selectbox("Base Movie", movie_list, label_visibility="collapsed")
    with col2:
        selected_genre = st.selectbox("Target Genre", genre_options, label_visibility="collapsed")
    with col3:
        recommend_btn = st.button("Recommend →", type="primary")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # PROCESS RECOMMENDATION TRIGGERS AND COMMIT IMMEDIATELY TO REALTIME HISTORIES
    if recommend_btn:
        # LOGS SEARCH TARGET TO WATCH HISTORY AND TRIGGER REALTIME RENDERING
        save_history(st.session_state.username, selected_movie)
        
        with st.spinner("Analysing cinematic DNA and filtering genres… 🍿"):
            raw_recommendations = recommend_movies(selected_movie)

        filtered_recommendations = []
        for movie in raw_recommendations:
            poster_url, description, movie_genres = fetch_movie_details(movie)
            if selected_genre == "All Genres" or selected_genre.lower() in movie_genres.lower():
                filtered_recommendations.append((movie, poster_url, description))

        # COMMIT EVERYTHING INTO SESSION STATE TRACKERS
        st.session_state.search_results = filtered_recommendations
        st.session_state.last_searched_movie = selected_movie
        st.session_state.last_searched_genre = selected_genre
        st.rerun()

    # PERMANENTLY DISPLAY COMMITTED SESSION SEARCH MATRIX ELEMENTS
    if st.session_state.search_results is not None:
        st.markdown(f"""
        <div style="text-align:center; color:rgba(255,255,255,0.7); margin-bottom: 24px; font-weight: 500;">
            Showing <strong style="color:#e63946;">{st.session_state.last_searched_genre}</strong> matches based on <em>{st.session_state.last_searched_movie}</em>:
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.search_results:
            # Renders items dynamically across columns over any amount of results without truncation
            for idx, (movie, poster_url, description) in enumerate(st.session_state.search_results):
                if idx % 3 == 0:
                    cols = st.columns(3)
                
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{poster_url}" class="movie-poster" alt="Movie Poster">
                        <div class="movie-card-content">
                            <div style="font-size:11px;font-weight:600;letter-spacing:1.2px; text-transform:uppercase;color:#e63946;margin-bottom:10px;">
                                ✦ Genre Match
                            </div>
                            <div class="movie-card-title">{movie}</div>
                            <div class="movie-card-body">{description}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if movie in history:
                        st.button("✅ Already Watched", key=f"watched_discover_{movie}_{idx}", disabled=True)
                    else:
                        if st.button("🍿 Mark as Watched", key=f"watch_discover_{movie}_{idx}"):
                            save_history(st.session_state.username, movie)
                            st.rerun()
        else:
            st.info(f"No match found for genre '{st.session_state.last_searched_genre}' within these recommendations. Try selecting another genre!")

    # ── Footer ──
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.2); font-size: 13px; padding: 32px 0 16px; letter-spacing: 0.4px;">
        CineMatch AI &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Made with ❤️
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# ROUTER
# ==========================================

if st.session_state.logged_in:
    render_main_app()
else:
    render_auth_page()