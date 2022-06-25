import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=fcb06c587941e4961a1e48b99112a8a4&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[movie_index]))
    movie_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Enter the Movie Name', movies['title'].values)

if st.button('Recommend'):
    titles, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(titles[0])
        st.image(posters[0])
    with col2:
        st.text(titles[1])
        st.image(posters[1])
    with col3:
        st.text(titles[2])
        st.image(posters[2])
    with col4:
        st.text(titles[3])
        st.image(posters[3])
    with col5:
        st.text(titles[4])
        st.image(posters[4])
