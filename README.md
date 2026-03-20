# Movie Recommendation System

A content-based movie recommendation system built with Streamlit. Select a movie from the dataset and the app suggests 5 similar movies using a precomputed similarity matrix. The interface also fetches poster images from TMDB for a more visual browsing experience.

## Features

- Content-based movie recommendations
- Streamlit UI for selecting a title and viewing results
- Poster images fetched from TMDB
- Top 5 similar movies returned for each selection

## Project Files

- `app.py` - main Streamlit application
- `movies.pkl` - movie metadata used by the recommender
- `similarities.joblib` - precomputed similarity scores
- `requirements.txt` - project dependencies

## Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your TMDB API key:

```powershell
$env:TMDB_API_KEY="your_tmdb_api_key"
```

3. Start the application:

```bash
streamlit run app.py
```

## How It Works

The recommender uses a precomputed similarity matrix for the movies in `movies.pkl`. After a user selects a movie, the app finds the closest matches by similarity score and displays the top 5 recommendations. Poster images are retrieved live from TMDB using the movie titles.

## Note

If `TMDB_API_KEY` is not set, the recommendation flow still works, but poster images fall back to a placeholder.
