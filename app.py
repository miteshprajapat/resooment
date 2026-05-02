import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# -------------------------------
# 🔥 Load data from Google Drive
# -------------------------------
@st.cache_data
def load_data():
    movies_id = "1w8QyLybLhpvpozDAul1EUxE3ToCeI5Dn"
    similarity_id = "12ModJDrtMinOzAR7c1rKpWxZ8f5Xwk-m"

    if not os.path.exists("movies.pkl"):
        gdown.download(f"https://drive.google.com/uc?id={movies_id}", "movies.pkl", quiet=False)

    if not os.path.exists("similarity.pkl"):
        gdown.download(f"https://drive.google.com/uc?id={similarity_id}", "similarity.pkl", quiet=False)

    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))

    return movies, similarity


movies, similarity = load_data()


# -------------------------------
# 🎬 Fetch poster
# -------------------------------
@st.cache_data
def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key=a6088a23520cb3e8fb9bf59583b650f1&query={movie_name}"
        data = requests.get(url, timeout=5).json()

        if data['results'] and data['results'][0]['poster_path']:
            poster_path = data['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# -------------------------------
# 🤖 Recommendation logic
# -------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_movies_poster = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommend_movies.append(title)
        recommend_movies_poster.append(fetch_poster(title))

    return recommend_movies, recommend_movies_poster


# -------------------------------
# 🎨 UI
# -------------------------------
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie_name)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.caption(names[0])

    with col2:
        st.image(posters[1], use_container_width=True)
        st.caption(names[1])

    with col3:
        st.image(posters[2], use_container_width=True)
        st.caption(names[2])

    col4, col5 = st.columns(2)

    with col4:
        st.image(posters[3], use_container_width=True)
        st.caption(names[3])

    with col5:
        st.image(posters[4], use_container_width=True)
        st.caption(names[4])