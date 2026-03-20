import streamlit as st
import pickle
import joblib
import requests
import pandas as pd
import os

# TMDB API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
    }
    .stTitle {
        color: #00d4ff !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .movie-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 10px;
    }
    .stSelectbox, .stButton {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #00d4ff, #0099cc) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #0099cc, #0077aa) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

if not TMDB_API_KEY:
    st.info("Set the TMDB_API_KEY environment variable to load movie posters.")

with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarities.joblib', 'rb') as f:
    similarity = joblib.load(f)

def get_movie_poster(movie_title):
    """Fetch movie poster from TMDB API"""
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/300x450/333333/ffffff?text=TMDB+Key+Missing"

    try:
        # Search for the movie
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'language': 'en-US',
            'page': 1
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        if data['results']:
            # Get the first result's poster path
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"{POSTER_BASE_URL}{poster_path}"
    except Exception as e:
        st.warning(f"Could not fetch poster for {movie_title}: {str(e)}")

    # Return a placeholder image if poster not found
    return "https://via.placeholder.com/300x450/333333/ffffff?text=No+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_data = movies.iloc[i[0]]
        recommended_movies.append({
            'title': movie_data.title,
            'poster': get_movie_poster(movie_data.title)
        })
    return recommended_movies

movies_list = movies['title'].values

st.markdown("### 🎯 Select a movie to get recommendations")
movie_name = st.selectbox("", movies_list, label_visibility="collapsed")

if st.button("🚀 Get Recommendations", type="primary"):
    st.markdown("---")
    st.markdown("## 🎭 Top 5 Recommended Movies")

    recommended_movies = recommend(movie_name)

    # Create columns for grid layout
    cols = st.columns(5)

    for idx, movie in enumerate(recommended_movies):
        with cols[idx]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{movie['poster']}" style="width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                <div class="movie-title">{movie['title']}</div>
            </div>
            """, unsafe_allow_html=True)
