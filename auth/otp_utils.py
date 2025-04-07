import random, time
from auth.db_utils import store_otp, get_otp_record, delete_otp

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    store_otp(email, otp)
    return otp

def verify_otp(email, user_otp):
    record = get_otp_record(email)
    if not record:
        return False
    return record["otp"] == user_otp

def is_otp_expired(email, expiry=300):
    record = get_otp_record(email)
    if not record:
        return True
    return time.time() - record.get("timestamp", 0) > expiry
