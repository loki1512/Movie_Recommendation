import streamlit as st
import pandas as pd
import pickle
import requests
movies_list=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies_list)


st.title('Movie Recommendation System')
option=st.selectbox('Select a Movie',movies['title'].values, key='1')
similarity=pickle.load(open('similarity.pkl','rb'))
recommended_movies=[]
recommended_movie_posters=[]
def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f466c051f25e986f64cb029b68f1551c&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(name):
    movie_index = movies[movies['title']==name].index[0]
    distances=similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:5]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters
    
if st.button('Recommend'):
    st.subheader('You selected')
    st.write(option)
    st.header('Recommended Movies')
    movies,images=recommend(option)
    
    col1, col2, col3= st.columns(3)
    lis=[col1,col2,col3]
    for i in range(3):
        with lis[i]:
            st.write(movies[i])
            st.image(images[i])


