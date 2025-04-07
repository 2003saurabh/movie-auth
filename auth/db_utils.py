import pymongo
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["user_db"]
users = db["users"]
attempts = db["attempts"]
otps = db["otps"]

def create_user(username, email, hashed_password):
    if users.find_one({"email": email}):
        return False
    users.insert_one({"username": username, "email": email, "password": hashed_password})
    return True

def get_user(email):
    return users.find_one({"email": email})

def update_password(email, hashed_password):
    users.update_one({"email": email}, {"$set": {"password": hashed_password}})

def get_attempts(email):
    record = attempts.find_one({"email": email})
    return record["count"] if record else 0

def increment_attempts(email):
    attempts.update_one({"email": email}, {"$inc": {"count": 1}}, upsert=True)

def reset_attempts(email):
    attempts.delete_one({"email": email})

def store_otp(email, otp):
    otps.update_one({"email": email}, {"$set": {"otp": otp, "timestamp": time.time()}}, upsert=True)

def get_otp_record(email):
    return otps.find_one({"email": email})

def delete_otp(email):
    otps.delete_one({"email": email})

def log_selected_movie(email, movie_title):
    users.update_one(
        {"email": email},
        {"$addToSet": {"selected_movies": movie_title}}  # avoids duplicates
    )
