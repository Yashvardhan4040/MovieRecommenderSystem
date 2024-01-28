import streamlit as st
import pandas as pd
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        return None

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        st.warning("Movie not found in the dataset.")
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        poster_path = fetch_poster(movie_id)
        
        if poster_path:
            recommended_movie_posters.append(poster_path)
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app
st.header('Movie Recommender System - Made By Yashvardhan Singh')

# Load data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendation button
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for name, poster_path in zip(recommended_movie_names, recommended_movie_posters):
        with col1:
            st.text(name)
            st.image(poster_path)
