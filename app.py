import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
load_dotenv()


POSTER_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")  # from .env or set manually

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_TOKEN}",
    "accept": "application/json"
}

def fetchPosterPath(movie_id: int) -> str:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        res.raise_for_status()
        data = res.json()
        return POSTER_BASE + data.get("poster_path", "")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch poster for movie_id {movie_id}: {e}")
        return ""


def recommend(movie: str):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in dataset.")
        return [], [], []

    similarity_vector = list(enumerate(similarity[index])) # provide index to each movie distance
    top_similar = sorted(similarity_vector, key=lambda x: x[1], reverse=True)[1:9]

    recommend_ids = []
    recommend_titles = []
    recommend_posters = []

    for idx, _ in top_similar:
        movie_id = int(movies.iloc[idx].movie_id)
        title = movies.iloc[idx].title
        poster = fetchPosterPath(movie_id)

        recommend_ids.append(movie_id)
        recommend_titles.append(title)
        recommend_posters.append(poster)

    return recommend_ids, recommend_titles, recommend_posters


def show_recommendations(titles, posters):
    counter = 0
    for row in range(0, len(titles), 4):   # 4 posters per row
        cols = st.columns(4)
        for i, col in enumerate(cols):
            if row + i < len(titles):
                with col:
                    st.image(posters[counter], use_container_width=True)
                    st.caption(titles[row + i])
                    counter += 1

st.header("Movie Recommendation System", divider=True)

with st.form("movie_form"):
    title = st.text_input("Enter movie title", "Avatar")
    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    st.write("Recommended Movies:")
    ids, titles, posters = recommend(title)
    show_recommendations(titles, posters)
