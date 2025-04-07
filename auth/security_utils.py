import bcrypt
from auth.db_utils import get_attempts, increment_attempts, reset_attempts as ra

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    if isinstance(hashed, str):  # If stored as string, convert to bytes
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)

def brute_force_protection(email, limit=5):
    if get_attempts(email) >= limit:
        return False
    increment_attempts(email)
    return True

def reset_attempts(email):
    ra(email)
