import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

movies = pickle.load(open("models/movies.pkl", "rb"))
similarity = pickle.load(open("models/similarity.pkl", "rb"))

def fetch_movie_details(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}'
        )
        data = response.json()
        poster_url = "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')
        movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
        return poster_url, movie_link
    except:
        return "", ""

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    names, posters, links = [], [], []
    for i in recommended_indices:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, link = fetch_movie_details(movie_id)
        names.append(title)
        posters.append(poster)
        links.append(link)

    return names, posters, links
