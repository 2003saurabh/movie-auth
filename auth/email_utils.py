import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from auth.logger import logger

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def send_otp_email(to_email, otp):
    try:
        msg = MIMEText(f"Your OTP is {otp}. It expires in 5 minutes.")
        msg['Subject'] = "Your OTP Code"
        msg['From'] = os.getenv("EMAIL_USER")
        msg['To'] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        logger.info(f"OTP sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send OTP: {e}")


