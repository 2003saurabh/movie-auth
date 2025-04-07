import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from auth.db_utils import create_user, get_user, update_password, log_selected_movie
from auth.email_utils import send_otp_email
from auth.otp_utils import generate_otp, verify_otp, is_otp_expired
from auth.security_utils import hash_password, verify_password, brute_force_protection, reset_attempts

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Load movie data
movies = pickle.load(open('models/movies.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))
movie_titles = movies['title'].values

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Session state
for key in ['authenticated', 'username', 'email']:
    if key not in st.session_state:
        st.session_state[key] = False if key == 'authenticated' else ""

# Sidebar auth panel
if not st.session_state.authenticated:
    with st.sidebar:
        st.title("🔐 Login / Signup")
        mode = st.radio("Select Mode", ["Login", "Signup", "Forgot Password"])

        if mode == "Signup":
            st.subheader("Create a New Account")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Send OTP"):
                if not username or not email or not password or not confirm_password:
                    st.error("All fields are required.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif get_user(email):
                    st.error("User already exists.")
                else:
                    otp = generate_otp(email)
                    send_otp_email(email, otp)
                    st.success("OTP sent to your email.")

            otp_input = st.text_input("Enter OTP")
            if st.button("Verify & Signup"):
                if is_otp_expired(email):
                    st.error("OTP expired. Please try again.")
                elif not verify_otp(email, otp_input):
                    st.error("Invalid OTP.")
                else:
                    hashed = hash_password(password)
                    if create_user(username, email, hashed):
                        st.success("Account created successfully!")

        elif mode == "Login":
            st.subheader("Login to Your Account")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                user = get_user(email)
                if not user:
                    st.error("User not found.")
                elif not brute_force_protection(email):
                    st.error("Too many failed attempts.")
                elif not verify_password(password, user["password"]):
                    st.error("Incorrect password.")
                else:
                    reset_attempts(email)
                    st.session_state.authenticated = True
                    st.session_state.username = user["username"]
                    st.session_state.email = user["email"]
                    st.success(f"Welcome, {user['username']}!")
                    st.rerun()

        elif mode == "Forgot Password":
            st.subheader("Reset Password")
            email = st.text_input("Registered Email")

            if st.button("Send OTP"):
                user = get_user(email)
                if not user:
                    st.error("User not found.")
                else:
                    otp = generate_otp(email)
                    send_otp_email(email, otp)
                    st.success("OTP sent to your email.")

            otp_input = st.text_input("Enter OTP")
            new_password = st.text_input("New Password", type="password")

            if st.button("Reset Password"):
                if is_otp_expired(email):
                    st.error("OTP expired.")
                elif not verify_otp(email, otp_input):
                    st.error("Invalid OTP.")
                else:
                    hashed = hash_password(new_password)
                    update_password(email, hashed)
                    st.success("Password updated successfully!")

# Movie recommendation system
if st.session_state.authenticated:
    # Header with logout button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🎬 Movie Recommender System")
        st.markdown(f"#### 👋 Welcome, **{st.session_state.username}**")
    with col2:
        st.write("")  # Spacer for alignment
        st.write("")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.email = ""
            st.success("Logged out successfully.")
            st.rerun()

    def fetch_movie_details(movie_id):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
            movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
            return poster_url, movie_link
        except:
            return "https://via.placeholder.com/500x750?text=No+Image", "#"

    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        recommended_movies_links = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            title = movies.iloc[i[0]].title
            recommended_movies.append(title)
            poster_url, movie_link = fetch_movie_details(movie_id)
            recommended_movies_posters.append(poster_url)
            recommended_movies_links.append(movie_link)

        return recommended_movies, recommended_movies_posters, recommended_movies_links

    selected_movie = st.selectbox("Choose a movie", movie_titles)
    if st.button("Recommend"):
        names, posters, links = recommend(selected_movie)
        log_selected_movie(st.session_state.email, selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_container_width=True)
                st.markdown(f"**[{names[i]}]({links[i]})**", unsafe_allow_html=True)
