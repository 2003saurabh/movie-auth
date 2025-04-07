# 🎬 Movie Recommendation Web App

A personalized movie recommendation system with authentication, AI chatbot feedback, MongoDB integration, and Streamlit frontend — fully Dockerized and ready for deployment.

---

## 🚀 Features

- 🔐 User authentication (Signup/Login with Email OTP)
- 🎥 Movie recommendations using cosine similarity
- 🌆 Poster images fetched via TMDb API
- 💬 AI chatbot using LangChain & Hugging Face
- 🧠 Sentiment analysis on feedback
- 📧 Personalized email replies based on feedback
- 🧱 MongoDB backend for users, movies, and feedback
- 🐳 Dockerized for easy deployment
- ⚙️ Secure handling of secrets via `.env` file

---

## 📁 Project Structure

```bash
movie-app/
│
├── auth/                    # Handles login, signup, OTP, email utils, security
│   ├── db_utils.py
│   ├── email_utils.py
│   ├── otp_utils.py
│   └── security_utils.py
│
├── recommender/             # Movie recommendation logic
│   └── recommender_utils.py (optional/custom logic)
│
├── models/                  # Pre-trained data/models
│   ├── movies.pkl           # ~2MB
│   └── similarity.pkl       # ~176MB
│
├── logs/                    # Logging folder (optional)
│
├── .env                     # 🔒 Not committed — stores secrets
├── .gitignore
├── requirements.txt
├── Dockerfile
├── main.py                  # Main Streamlit app
├── main1.py                 # Backup or alt version of app
└── README.md
