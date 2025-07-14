import streamlit as st
import pickle


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    similarity_vector = similarity[index]
    similarity_vector = list(enumerate(similarity_vector))    # provide index to each movie distance
    movies_list = sorted(similarity_vector, reverse=True, key=lambda x: x[1])[1:9]

    recommend_moviesId = []
    recommend_moviesTitle = []
    for item in movies_list:
        recommend_moviesId.append(movies.iloc[item[0]].movie_id)
        recommend_moviesTitle.append(movies.iloc[item[0]].title)

    return recommend_moviesId, recommend_moviesTitle

st.header("Movie Recommendation System", divider=True)

with st.form("movie_form"):
    title = st.text_input("Enter movie title", "Avatar")
    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    st.write("The current movie title is:", recommend(title))
