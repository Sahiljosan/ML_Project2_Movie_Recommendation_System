import streamlit as st
import pandas as pd
import pickle
import requests
import bz2
import os

movies_list = pickle.load(open('recommended_movies.pkl','rb'))

st.title('Movie Recommender System')
st.text('By Sahil Josan')

selected_movie_name = st.selectbox(
'Select movie from drop down list',
movies_list['title'].values)

# similarity = pickle.load(open("similarity.pkl",'rb'))
ifile = open("similarity.pkl","rb")
similarity = pickle.loads(bz2.decompress(ifile.read()))
ifile.close()


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list2= sorted(list(enumerate(distances)), reverse= True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list2:
        movie_id = movies_list.iloc[i[0]].movie_id
      
        recommended_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])