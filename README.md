
# 🎬 Movie Recommender System

A personalized movie recommendation web app built with [Streamlit](https://streamlit.io/), allowing users to sign up, log in, and receive intelligent movie suggestions based on a selected title. The app fetches real-time poster images and movie details from the [TMDB API](https://www.themoviedb.org/documentation/api), and supports OTP-based email verification for user signup and password recovery.

---

## 🚀 Features

- 🔐 **User Authentication** (Signup, Login, Password Reset)
- ✉️ OTP-based email verification (via SMTP)
- 🔒 Password hashing with `bcrypt` and brute-force protection
- 🎥 Intelligent Movie Recommendations (Top 5 similar movies)
- 🖼️ Real-time posters and links using TMDB API
- 📜 Logs user's selected movies
- 📂 Modular project structure for easy maintenance

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **Data**: Precomputed similarity matrix (`pickle`), TMDB API
- **Authentication**: Custom with email OTP, bcrypt
- **Database**: MongoDB (via `auth/db_utils.py`)
- **Environment Variables**: Managed via `python-dotenv`

---

## 📁 Project Structure

```
movie-recommender/
├── app.py                     # Main Streamlit application
├── models/
│   ├── movies.pkl             # Movie metadata
│   └── similarity.pkl         # Similarity matrix
├── auth/
│   ├── db_utils.py            # User DB interactions
│   ├── email_utils.py         # Email sending logic
│   ├── otp_utils.py           # OTP generation & validation
│   └── security_utils.py      # Password hashing and login security
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
└── README.md                  # You're here!
```

---

## 🧪 Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
TMDB_API_KEY=your_tmdb_api_key
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password_or_app_token
MONGO_URI=your_mongodb_connection_uri
```

> 💡 Use a secure app password if you're using Gmail or any 2FA-enabled email service.

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🧠 Recommendation Logic

1. User selects a movie.
2. The app finds its index and fetches the top 5 similar movies using the precomputed cosine similarity matrix.
3. For each movie, poster and metadata are fetched from TMDB API.
4. Results are displayed with images and links.

---

## 📦 Dependencies

Major libraries used:

- `streamlit`
- `pandas`
- `pickle`
- `requests`
- `dotenv`
- `bcrypt`
- `pymongo` (if using MongoDB for user storage)

---

## 🛡️ Security Notes

- Passwords are never stored in plain text — hashed securely with `bcrypt`.
- OTPs are time-bound (expire after a few minutes).
- Login attempts are rate-limited to prevent brute-force attacks.

---

## 📌 TODO / Ideas for Future

- View search history in dashboard
- Add logout confirmation modal
- Show recommendations automatically post-login
- Add user profile settings
- Theme toggle (Dark/Light)

---

## 📸 Screenshot

![Screenshot](https://via.placeholder.com/1000x600.png?text=Screenshot+of+Movie+Recommender+App)

---

## 📄 License

MIT License. Feel free to use, modify, and share.

---

## 💡 Credits

- Movie Data: [TMDB](https://www.themoviedb.org/)
- Inspired by recommendation system tutorials and enhanced with full user authentication.

---

### 🧑‍💻 Built with ❤️ by [Your Name]
